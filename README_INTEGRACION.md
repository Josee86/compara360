# COMPARA360 — Preparación de integración de catálogos y afiliación

## Estado real de esta entrega
Esta carpeta incluye:
- La interfaz MVP de COMPARA360.
- Esquema SQL inicial para productos, tiendas, ofertas, historial y alertas.
- Contrato normalizado para importar ofertas desde redes autorizadas.
- Plantilla de variables de entorno y guía de activación.

**No hay credenciales ni conexiones activas todavía.** Los proveedores requieren que el titular cree cuentas, sea aceptado en programas y obtenga tokens/feed URLs. Los datos de demostración de `index.html` siguen siendo ficticios.

## Proveedores priorizados

### 1) Awin — primer conector recomendado
- Registro como publisher y aprobación en programas de anunciantes.
- Los feeds disponibles dependen de los anunciantes a los que estés conectado o que permitan acceso previo.
- El feed puede contener nombre, descripción, precio/descuentos, envío, imagen y deep link.
- Descarga mediante Product Data Feeds / Create-a-Feed. La clave de feeds es distinta de la Publisher API key.
- Documentación:
  - https://help.awin.com/developers/docs/product-feed-publisher-guide-intro
  - https://success.awin.com/s/article/How-can-I-access-a-Product-Feed?language=en_US

### 2) TradeDoubler — segundo conector
- Crear cuenta publisher y conectar con anunciantes concretos.
- Products API permite consultar datos de anunciantes conectados y requiere token publisher.
- Documentación: https://dev.tradedoubler.com/products/publisher/

### 3) Amazon Associates / Creators API — fase posterior
- Registrarse por marketplace (España, Francia, Alemania, Italia, etc.) y cumplir las condiciones locales.
- La documentación de Creators API indica que se requieren al menos 10 ventas cualificadas en los últimos 30 días para acceder a la API, además de aceptación y registro.
- Cada marketplace requiere su Partner Tag válido.
- Documentación:
  - https://affiliate-program.amazon.com/creatorsapi/docs/
  - https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding/sign-up-as-an-amazon-associate

## Modelo de datos
`schema.sql` crea tablas para:
- `products`: identidad canónica por GTIN/EAN o marca + MPN.
- `merchants`: tiendas y país/mercado.
- `offers`: precio, envío, moneda, stock, URL afiliada, fecha de actualización y fuente.
- `price_history`: observaciones fechadas para historial.
- `price_alerts`: objetivos de usuarios (requiere autenticación en producción).

## Contrato de importación
Cada conector debe transformar su feed a este formato JSON antes de insertarlo:
```json
{
  "source": "awin",
  "merchant_name": "Nombre de tienda",
  "market": "ES",
  "currency": "EUR",
  "product": {
    "gtin": "0000000000000",
    "brand": "Marca",
    "mpn": "MODELO-123",
    "title": "Nombre exacto del producto",
    "category": "Electrónica"
  },
  "offer": {
    "price": 99.99,
    "shipping": 4.99,
    "availability": "in_stock",
    "product_url": "https://tienda.example/producto",
    "affiliate_url": "https://tracking.example/click",
    "last_seen_at": "2026-11-20T12:00:00Z"
  }
}
```
No comparar productos si no hay coincidencia fiable de GTIN o marca+MPN. Si el envío no está informado, mostrarlo como "no disponible" y no asumir que es gratis.

## Seguridad y cumplimiento
- No poner tokens/API keys en `index.html` ni en código enviado al navegador.
- Guardar secretos solo en variables de entorno del backend.
- Respetar términos, frecuencia de actualización, atribución y políticas de cada programa.
- Identificar enlaces patrocinados/afiliados y publicar aviso de afiliación.
- Mostrar "última actualización" y país/moneda de cada oferta.
- Evitar scraping no autorizado.
- Para alertas reales hace falta backend programado y proveedor de correo; la versión actual guarda alertas solo en el navegador.

## Presupuesto
Con 50 €: dominio + hosting/base de datos de nivel gratuito, sujeto a límites y condiciones. No comprar feeds ni APIs de pago hasta validar tráfico y monetización. Las redes pueden ser gratuitas para registrarse, pero aprobación no está garantizada y el tiempo de revisión no depende de nosotros.

## Siguiente paso que necesita al titular
1. Crear cuenta Publisher en Awin.
2. Solicitar programas de anunciantes que acepten comparadores/precios y seleccionar feeds en ES (después FR/DE/IT).
3. Crear cuenta Publisher en TradeDoubler y solicitar anunciantes relevantes.
4. Guardar claves en un backend seguro, nunca enviarlas por chat.
5. Compartir únicamente los nombres de los programas aprobados y los campos disponibles del feed (sin secretos) para completar el adaptador exacto.
