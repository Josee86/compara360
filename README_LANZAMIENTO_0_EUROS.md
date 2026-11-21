# COMPARA360 — Lanzamiento con 0 €

## Qué contiene esta versión
- Interfaz web estática basada en el MVP.
- Selector de ocho mercados de la zona euro: ES, FR, DE, IT, NL, BE, PT e IE.
- Preparación para publicar gratuitamente con GitHub Pages.
- Workflow de despliegue automático al subir cambios a la rama `main`.
- Esquema SQL, contrato de importación y plantilla de configuración heredados de la preparación técnica.

## Aviso esencial sobre los datos
Los productos, comercios, precios y series históricas que aparecen en el MVP son **ficticios**. El selector de país solo permite seleccionar el mercado de demostración; no significa que haya catálogos reales conectados en esos países. No publiques ni promociones esos datos como ofertas reales. Antes de una beta pública de comparación, sustituye el catálogo de ejemplo por feeds autorizados y aprobados.

## Publicar gratis con GitHub Pages
1. Crea una cuenta gratuita en https://github.com/
2. Crea un repositorio público llamado `compara360`.
3. Sube el contenido de esta carpeta a la raíz del repositorio, incluida la carpeta `.github`.
4. En GitHub, abre **Settings → Pages**.
5. En **Build and deployment**, selecciona **GitHub Actions**.
6. Comprueba la pestaña **Actions**. Cuando termine el flujo, GitHub mostrará la URL pública, normalmente `https://TU-USUARIO.github.io/compara360/`.
7. Si haces cambios en la rama `main`, se volverán a publicar automáticamente.

GitHub puede cambiar los límites o condiciones de su plan gratuito. Comprueba sus condiciones antes de depender comercialmente del servicio.

## Dominio propio sin pagar
Un dominio `.com` registrado a tu nombre normalmente tiene un coste anual. No hay una vía fiable para garantizar un `.com` permanente por 0 €. La publicación inicial usa un subdominio gratuito de GitHub Pages. Si más adelante consigues un dominio gratuito legítimo, se podrá conectar desde **Settings → Pages → Custom domain**, siguiendo las instrucciones DNS del registrador. No introduzcas datos de pago ni aceptes pruebas que se conviertan automáticamente en suscripciones.

## Mercados y monedas
Esta primera preparación contempla ocho mercados con EUR. La selección de mercado no convierte precios ni garantiza que una tienda opere en ese país. Antes de habilitar ofertas reales en cada país, hay que comprobar:
- que el anunciante acepta tráfico/comparadores desde ese mercado;
- que el feed incluye productos destinados a ese país;
- moneda, impuestos, envío y disponibilidad;
- URL de destino y enlace afiliado válidos para ese mercado;
- idioma y condiciones de devolución.

Reino Unido, Suiza, Polonia y otros mercados con moneda distinta se incorporarán cuando tengamos una fuente de cambio fiable y feeds específicos. No se deben convertir precios manualmente ni mezclar ofertas de mercados distintos.

## Afiliación y transparencia
Antes de activar enlaces comerciales, añade un aviso visible de enlaces afiliados, publica política de privacidad y cookies conforme a los servicios realmente usados, y revisa las condiciones de cada programa. No uses scraping que infrinja los términos de las tiendas o redes.

## Arquitectura de coste cero
- Frontend: HTML/CSS/JS estático en GitHub Pages.
- Catálogo: feeds de redes de afiliación que autoricen su uso, sujeto a aprobación.
- Backend/alertas: no activados en esta versión. Supabase Free u otro plan gratuito puede evaluarse más adelante, revisando límites y privacidad.
- Automatización: GitHub Actions para despliegue. La actualización de feeds necesitará conectores autorizados y ejecución dentro de límites gratuitos.

## Próximo paso
Publica el repositorio y comparte únicamente la URL pública de la web. No compartas contraseñas, tokens, claves API ni URLs privadas de feeds.
