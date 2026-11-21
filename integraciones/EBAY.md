# Conexión oficial eBay · COMPARA360

## Estado
**Preparada, pero no activada.** No tenemos claves de desarrollador ni confirmación de aprobación para Buy APIs en producción. No hay consulta real realizada y no hemos publicado ningún precio de eBay.

Referencias oficiales:
- [Crear cuenta de desarrollador](https://developer.ebay.com/)
- [Requisitos de Buy APIs en producción](https://developer.ebay.com/api-docs/buy/static/buy-requirements.html)
- [Browse API](https://developer.ebay.com/develop/api/buy/browse_api)
- [OAuth client credentials](https://developer.ebay.com/api-docs/static/oauth-client-credentials-grant.html)

## Seguridad y coste
El cliente obtiene un token de aplicación en backend, nunca en el navegador. Se han preparado los nombres de secretos:
- `EBAY_CLIENT_ID`
- `EBAY_CLIENT_SECRET`
- `EBAY_EPN_CAMPAIGN_ID` (opcional; **solo** si existe campaña afiliada aprobada)

No pongas estas claves en archivos del repositorio, chats, capturas o páginas públicas. Para introducirlas, usa **Settings → Secrets and variables → Actions → New repository secret** en GitHub. La creación de credenciales de desarrollador es gratuita según eBay, pero el acceso a Buy APIs de producción depende de aprobaciones adicionales.

## Prueba de conexión
Una vez aprobados los permisos, desde **Actions → Probar conexión eBay (sin publicar ofertas) → Run workflow** selecciona mercado y búsqueda. La prueba solo imprime un número de resultados; no guarda ni publica precios.

El script funciona también localmente desde `scripts/ebay_browse.py` con variables de entorno protegidas. Usa exclusivamente módulos estándar de Python.

## Antes de mostrar precios reales
1. Verificar la autorización para utilizar Browse API en producción, las condiciones de uso y las condiciones concretas de persistencia/republicación.
2. Comprobar país, impuestos, envíos, caducidad y condiciones de los productos.
3. Si se activa afiliación EPN, mostrar y usar la URL de afiliación que entrega eBay.
4. Mantener los productos como **anuncios de vendedores**; no agrupar variantes diferentes como productos idénticos.
5. Solo si se permite legalmente almacenar/publicar, activar una exportación y normalización revisada; en el repositorio actual no se automatiza la publicación.

## Mercados
El adaptador soporta ES, FR, DE, IT, NL, BE, IE como mercados eBay identificados. No usa PT directamente porque no hay un identificador de marketplace eBay Portugal equivalente. En COMPARA360 Portugal seguirá preparado para otras fuentes.

## Datos abiertos alternativos
[Open Prices](https://openfoodfacts.github.io/open-prices/) ofrece datos abiertos de alimentación, pero tienen condiciones de licencia OdBL y atribución; los registros son contribuciones históricas, no precios verificados en directo. Su uso necesita diseño/atribución adecuados y es independiente de eBay. No se mezclará automáticamente con ofertas de comercio electrónico.
