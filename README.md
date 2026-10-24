# DNSTT — laboratorio de GitHub Actions

Laboratorio **local y efímero** para compilar y comprobar DNSTT en un runner Ubuntu de GitHub Actions. No lanza un proxy público ni un servidor VPN de producción.

## Estado y seguridad

- El workflow corre únicamente con `workflow_dispatch` (activación manual).
- Compila `dnstt-client` y `dnstt-server` desde el repositorio original de David Fifield, fijado a un commit mediante el lock `UPSTREAM_REF`.
- Ejecuta el servidor en `127.0.0.1:15353/udp`, sin exposición externa, y prueba conectividad cliente-servidor con un servicio HTTP local.
- No genera credenciales persistentes; las claves se crean durante el job.
- No reenvía tráfico de terceros, no configura un túnel externo y termina automáticamente.
- GitHub-hosted Actions **no** es un servidor DNSTT accesible desde tu PC: no ofrece UDP 53 entrante ni IP fija. Para hacer la prueba remota usaremos después un servidor con IP pública y DNS delegado, o un runner self-hosted apropiado.

## Ejecución

En GitHub: **Actions → DNSTT loopback smoke test → Run workflow**.

El job publica logs con compilación y la prueba HTTP. Por defecto permanece **sin ejecutar** hasta que lo actives.

## Prueba posterior con tu PC

Cuando decidamos probar tu PC, necesitaremos un host que acepte UDP 53 desde Internet, un dominio bajo tu control y los registros DNS `NS` y `A` de delegación. La guía está en [docs/PC-TEST.md](docs/PC-TEST.md).

## Limitaciones

Este laboratorio verifica una instancia local y no mide rendimiento real de resolvers públicos, multipath, SOCKS5 ni VPN/TUN. Esas etapas requieren pruebas separadas.
