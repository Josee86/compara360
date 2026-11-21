#!/usr/bin/env python3
"""COMPARA360: eBay Browse API adapter (Python standard library).

Requires eBay developer credentials and approved production Buy API access.
Default mode ONLY checks connectivity and returns a count. No public data
is saved, and no API credentials are printed.
Export mode is deliberately opt-in after verifying eBay's data usage terms.
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

# Sandbox is the default: safer testing before production authorization.
ENVIRONMENT = os.environ.get("EBAY_ENV", "sandbox").lower()
if ENVIRONMENT not in ("sandbox", "production"):
    raise RuntimeError("EBAY_ENV debe ser sandbox o production.")
API = "https://api.sandbox.ebay.com" if ENVIRONMENT == "sandbox" else "https://api.ebay.com"
MARKETS = {
    "ES": "EBAY_ES", "FR": "EBAY_FR", "DE": "EBAY_DE",
    "IT": "EBAY_IT", "NL": "EBAY_NL", "BE": "EBAY_BE",
    "IE": "EBAY_IE", 
}
# Portugal lacks a distinct eBay marketplace; do not silently substitute ES.
DEFAULT_QUERY = "auriculares inalámbricos"
USER_AGENT = "COMPARA360/0.1 (developer integration; contact via repository)"

def request(url, headers, data=None):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        # Avoid dumping tokens or URLs; include status only.
        raise RuntimeError("La API devolvió HTTP %s. Comprueba permisos, mercado y límites." % e.code) from None
    except urllib.error.URLError:
        raise RuntimeError("No se pudo conectar con eBay.") from None

def access_token():
    prefix = "EBAY_SANDBOX" if ENVIRONMENT == "sandbox" else "EBAY"
    client_id = os.environ.get(prefix + "_CLIENT_ID", "")
    client_secret = os.environ.get(prefix + "_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        raise RuntimeError("Faltan credenciales de " + ENVIRONMENT + " en variables de entorno protegidas.")
    credential = base64.b64encode((client_id + ":" + client_secret).encode()).decode()
    payload = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }).encode()
    response = request(API + "/identity/v1/oauth2/token", {
        "Authorization": "Basic " + credential,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }, data=payload)
    token = response.get("access_token")
    if not token:
        raise RuntimeError("eBay no entregó un token válido.")
    return token

def search(token, market, query, count, campaign_id=None):
    qs = urllib.parse.urlencode({"q": query, "limit": count, "filter": "buyingOptions:{FIXED_PRICE}"})
    headers = {
        "Authorization": "Bearer " + token,
        "X-EBAY-C-MARKETPLACE-ID": MARKETS[market],
        "Accept": "application/json",
        "User-Agent": USER_AGENT
    }
    if campaign_id:
        # Enable only for an approved, valid eBay Partner Network campaign.
        headers["X-EBAY-C-ENDUSERCTX"] = "affiliateCampaignId=" + urllib.parse.quote(campaign_id)
    return request(API + "/buy/browse/v1/item_summary/search?" + qs, headers)

def normalize(item, market, observed):
    value = item.get("price") or {}
    if value.get("currency") != "EUR":
        return None
    try:
        price = float(value["value"])
        if price < 0 or not price < float("inf"): return None
    except (KeyError, ValueError, TypeError):
        return None
    seller = item.get("seller") or {}
    title = item.get("title")
    dest = item.get("itemAffiliateWebUrl") or item.get("itemWebUrl")
    if not isinstance(title, str) or not title.strip() or not isinstance(dest, str) or not dest.startswith("https://"):
        return None
    option = (item.get("shippingOptions") or [{}])[0]
    ship_value = (option.get("shippingCost") or {})
    shipping = None
    if ship_value and ship_value.get("currency") == "EUR":
        try:
            shipping = float(ship_value["value"])
            if shipping < 0 or not shipping < float("inf"): shipping = None
        except (KeyError, TypeError, ValueError):
            pass
    seller_name = seller.get("username") or "Vendedor de eBay"
    return {
        "market": market, "currency": "EUR",
        "product_title": title[:300], "merchant": "eBay · " + str(seller_name)[:100],
        "source": "eBay Browse API",
        "category": "Marketplace", "price": price, "shipping": shipping,
        "url": dest,
        "affiliate": bool(item.get("itemAffiliateWebUrl")),
        "updated_at": observed,
        "gtin": None, "brand": None, "mpn": None,
        "source_item_id": item.get("itemId"),
        "condition": item.get("condition", "Desconocido")
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--market", choices=list(MARKETS), default="ES")
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--export", action="store_true", help="Exportar JSON tras revisar derechos de reutilización.")
    parser.add_argument("--output", default="catalog/ebay-preview.json")
    args = parser.parse_args()
    if not 1 <= args.limit <= 50: parser.error("El límite debe ser de 1 a 50")
    if not 2 <= len(args.query.strip()) <= 100: parser.error("La búsqueda debe tener entre 2 y 100 caracteres")
    if args.export and (ENVIRONMENT != "production" or os.environ.get("EBAY_EXPORT_AUTHORIZED") != "yes"):
        parser.error("Solo se exportan datos reales de producción con EBAY_EXPORT_AUTHORIZED=yes tras verificar las condiciones de eBay.")
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        token = access_token()
        result = search(token, args.market, args.query, args.limit, os.environ.get("EBAY_EPN_CAMPAIGN_ID"))
    except RuntimeError as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1
    items = result.get("itemSummaries", [])
    normalized = [x for i in items if (x := normalize(i, args.market, now))]
    print("Conexión eBay %s correcta: %d resultados, %d precios válidos en %s." % (ENVIRONMENT, len(items), len(normalized), args.market))
    if args.export:
        import pathlib
        path = pathlib.Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "schema_version":1, "updated_at":now, "offers":normalized
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Exportación local completada (no subida a GitHub): " + str(path))
    return 0

if __name__ == "__main__":
    sys.exit(main())
