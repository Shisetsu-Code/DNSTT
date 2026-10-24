# Prueba desde una PC — plan de ejecución posterior

**No activar la prueba remota hasta que el usuario lo solicite.**

1. Elegir un servidor propio o VPS con UDP 53 entrante y una IP pública estable.
2. Crear `ns.ejemplo.com A <IP>` y delegar `t.ejemplo.com NS ns.ejemplo.com` (DNS only en Cloudflare).
3. Compilar ambos binarios desde una revisión fijada de DNSTT y generar claves exclusivas del servidor. Compartir **solo** la clave pública.
4. Iniciar un servicio TCP local de pruebas en el servidor y ejecutar `dnstt-server -udp :53 -privkey-file server.key t.ejemplo.com 127.0.0.1:8000`.
5. Desde la PC ejecutar `dnstt-client -udp <resolver>:53 -pubkey-file server.pub t.ejemplo.com 127.0.0.1:7000`. Abrir `http://127.0.0.1:7000/` y comprobar la respuesta.
6. Tras comprobar conexión, medir latencia, throughput y pérdida; luego evaluar integración con proxy SOCKS5 y TUN/VPN.

> Usar comandos y puertos concretos según el sistema operativo, firewall y configuración DNS observados en la prueba.
> GitHub Actions alojado por GitHub solo sirve en este repositorio para pruebas de loopback, no como endpoint remoto.
