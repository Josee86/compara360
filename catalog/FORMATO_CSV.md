# Importar ofertas reales de forma gratuita

El comparador **no recopila precios automáticamente** ni tiene autorización de ninguna tienda todavía. Esta herramienta opcional sirve para importar un CSV legítimamente obtenido de un programa o comercio que **autorice publicar sus precios y enlaces**.

## Formato CSV

Cabeceras obligatorias:

`market,currency,product_title,merchant,source,category,price,shipping,url,affiliate,updated_at,gtin,brand,mpn`

- `market`: ES, FR, DE, IT, NL, BE, PT, IE.
- `currency`: EUR.
- `product_title`: nombre y variante específicos, sin confundir tamaños, capacidades, colores, etc.
- `merchant`: tienda que ofrece el artículo.
- `source`: plataforma o feed autorizado, no una credencial.
- `price`: número decimal con punto (`99.90`).
- `shipping`: coste del envío, **vacío** si se desconoce; `0` solo si se ha verificado que es gratis.
- `url`: URL pública HTTPS de destino, enlazada al producto. No incluyas claves o tokens.
- `affiliate`: `true` si es un enlace afiliado, `false` si no.
- `updated_at`: fecha real observada, ISO8601 con zona horaria (`2026-11-21T12:00:00Z`).
- `gtin`, `brand`, `mpn`: identificadores cuando estén disponibles. Ayudan a evitar mezclar variantes.
- `category`: categoría real. No es obligatorio rellenarla.

## Pasos cuando tengamos acceso autorizado

1. Descarga o exporta el feed autorizado **en tu ordenador**, sin publicar credenciales.
2. Convierte las columnas al formato anterior. Usa solo datos que permitan republicación pública.
3. Ejecuta localmente, con Python 3: `python scripts/import_catalog.py ofertas.csv --output catalog/offers.json`.
4. Revisa y sube **solo** el archivo `catalog/offers.json` al repositorio público. No subas el CSV privado.
5. GitHub Pages publicará la página automáticamente. El catálogo visible solo muestra ofertas con una fecha de actualización de los últimos 7 días.

## Limitaciones actuales

No hay conectores de feeds automatizados, alertas por correo, red de anuncios activa, ni programas de afiliación aprobados. Los productos de la demo son ficticios. El CSV es una vía manual inicial, no garantía de datos en tiempo real. No se deben añadir ofertas sin permiso. Antes de automatizar, revisaremos condiciones de cada feed, límites y almacenamiento seguro de credenciales.
