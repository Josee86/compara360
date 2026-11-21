#!/usr/bin/env python3
"""Convierte un CSV autorizado de ofertas a catalog/offers.json.

Solo usa la biblioteca estándar de Python. No descarga feeds ni utiliza claves.
Ejemplo:
  python scripts/import_catalog.py datos_autorizados.csv --output catalog/offers.json
El CSV debe incluir las columnas del archivo catalog/FORMATO_CSV.md.
"""
import argparse
import csv
import json
import math
import pathlib
import sys
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

MARKETS = {"ES", "FR", "DE", "IT", "NL", "BE", "PT", "IE"}
MAX_AGE = timedelta(days=7)
MAX_ROWS = 50000

def parse_money(raw, optional=False):
    if optional and (raw is None or not raw.strip()):
        return None
    try:
        value = float(raw)
    except (ValueError, TypeError):
        raise ValueError("Precio no numérico")
    if not math.isfinite(value) or value < 0:
        raise ValueError("El precio debe ser finito y no negativo")
    return round(value, 2)

def safe_url(raw):
    parsed = urlparse(raw or "")
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Se requiere enlace HTTPS público sin credenciales")
    if parsed.hostname in {"localhost", "127.0.0.1", "0.0.0.0"} or parsed.hostname.endswith(".local"):
        raise ValueError("Enlace no público")
    return raw

def parse_time(raw):
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        raise ValueError("Fecha ISO 8601 inválida")
    if dt.tzinfo is None:
        raise ValueError("La fecha debe incluir zona horaria")
    now = datetime.now(timezone.utc)
    if dt > now + timedelta(minutes=5) or now - dt > MAX_AGE:
        raise ValueError("Oferta desactualizada o fecha futura")
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

def normalize(row):
    market = (row.get("market") or "").strip().upper()
    if market not in MARKETS:
        raise ValueError("País no soportado")
    if (row.get("currency") or "").strip().upper() != "EUR":
        raise ValueError("Solo EUR en esta fase")
    title = (row.get("product_title") or "").strip()
    merchant = (row.get("merchant") or "").strip()
    source = (row.get("source") or "").strip()
    if not title or not merchant or not source:
        raise ValueError("Faltan producto, tienda o fuente")
    if any(len(x)>300 for x in (title, merchant, source)):
        raise ValueError("Campo de texto demasiado largo")
    affiliate = (row.get("affiliate") or "false").strip().lower()
    if affiliate not in ("true", "false"):
        raise ValueError("affiliate debe ser true o false")
    return {
        "market":market,
        "currency":"EUR",
        "product_title":title,
        "merchant":merchant,
        "source":source,
        "category":(row.get("category") or "").strip()[:100],
        "price":parse_money(row.get("price")),
        "shipping":parse_money(row.get("shipping"), optional=True),
        "url":safe_url((row.get("url") or "").strip()),
        "affiliate":affiliate=="true",
        "updated_at":parse_time((row.get("updated_at") or "").strip()),
        "gtin":(row.get("gtin") or "").strip()[:32] or None,
        "brand":(row.get("brand") or "").strip()[:120] or None,
        "mpn":(row.get("mpn") or "").strip()[:120] or None,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=pathlib.Path, help="Archivo CSV de una fuente autorizada")
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("catalog/offers.json"))
    args = parser.parse_args()
    if not args.csv_file.is_file():
        parser.error("No existe el archivo de entrada")
    offers, errors = [], []
    with args.csv_file.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        for num, row in enumerate(reader, start=2):
            if num-1>MAX_ROWS:
                parser.error(f"Máximo {MAX_ROWS} ofertas por importación")
            try:
                offers.append(normalize(row))
            except ValueError as exc:
                errors.append(f"Fila {num}: {exc}")
    if errors:
        for error in errors[:20]:
            print(error, file=sys.stderr)
        parser.error(f"{len(errors)} filas inválidas. No se ha modificado el catálogo.")
    if not offers:
        parser.error("No se encontraron ofertas; no se sobrescribe el catálogo.")
    # Escritura atómica: nunca dejar un JSON incompleto.
    target=args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary=target.with_suffix(target.suffix+".tmp")
    payload={"schema_version":1,"updated_at":datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),"offers":offers}
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    temporary.replace(target)
    print(f"Importadas {len(offers)} ofertas de un CSV autorizado en {target}")

if __name__=="__main__":
    main()
