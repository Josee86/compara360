# COMPARA360 — catálogo de ofertas reales

El archivo `offers.json` empieza **vacío** porque todavía no existe una fuente autorizada conectada. No introducir precios inventados.

## Formato de cada oferta

```json
{
  "market": "ES",
  "currency": "EUR",
  "product_title": "Título exacto del producto y variante",
  "merchant": "Nombre legal o comercial de la tienda",
  "category": "Electrónica",
  "price": 99.99,
  "shipping": null,
  "url": "https://tienda.example/producto",
  "affiliate": false,
  "updated_at": "2026-11-21T10:00:00Z",
  "gtin": null,
  "brand": null,
  "mpn": null
}
```

`shipping: null` significa que el precio del envío es desconocido. **No** equivale a envío gratis. Cada oferta necesita URL de tienda válida, fecha real de observación, moneda y país. Los datos deben venir de un anunciante/afiliación con permisos para esta finalidad. No mezclar países ni variantes; cotejar GTIN o marca+MPN.

Antes de importar datos al repositorio público:
- Obtener permiso y respetar condiciones de la red/feed.
- Confirmar que está permitida la republicación en una página pública y no exponer URL privadas, tokens ni claves.
- Actualizar en servidor, nunca usando credenciales en `index.html`.
- Verificar envío, impuestos, disponibilidad, mercado y fecha de cada oferta.
- Identificar los enlaces de afiliación y separar claramente cualquier publicidad.
- Establecer controles para retirar ofertas caducadas. La interfaz actual exige fecha válida, pero aún **no** elimina automáticamente las ofertas por antigüedad.

## Países preparados

ES, FR, DE, IT, NL, BE, PT, IE (EUR). La disponibilidad de catálogos autorizados no está garantizada para ninguno de ellos.

## Estado

Interfaz de lectura del catálogo implementada; **sin** importación automatizada de feeds, **sin** programas de afiliación aprobados y **sin** anuncios activados.
