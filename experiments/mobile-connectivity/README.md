# Prueba temporal de conectividad movil desde GitHub Actions

## Uso
1. Abrir Actions en el repositorio y elegir **Prueba movil sin datos (HTTPS)**.
2. Pulsar **Run workflow**.
3. Abrir el trabajo activo y copiar el enlace temporal de su **Summary**.
4. En el telefono, abrir el enlace con Wi-Fi y pulsar **Probar conexion ahora**.
5. Sin cerrar la pestaña, desactivar Wi-Fi; habilitar datos moviles en la SIM a comprobar y pulsar de nuevo **Probar conexion ahora**.
6. Registrar el resultado y contrastarlo con el estado de datos reportado por la operadora.

El servidor devuelve un desafio aleatorio; la respuesta correcta indica que hubo una solicitud HTTPS real a ese endpoint, no una copia en cache.

Esta prueba **NO usa BHTTP, no establece una VPN y NO demuestra internet gratuito**. Un resultado negativo tampoco descarta otras formas de conexion.

## Limitaciones
- GitHub Actions no proporciona un servidor de entrada TCP publica en el puerto 8880.
- Para comparar BHTTP real hace falta un servidor TCP propio (por ejemplo un VPS) y un cliente compatible.
- Cloudflare Quick Tunnels usa HTTPS 443 y el enlace es publico y temporal; solo desarrollo.
- El proceso termina unos 10 minutos despues de que aparezca el enlace.
- No ingresar credenciales. El servicio no reenvia trafico, y la app de ejemplo no registra IPs.
- GitHub y Cloudflare pueden disponer de registros propios.

Documentacion:
https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/
https://docs.github.com/en/actions/concepts/runners/github-hosted-runners
