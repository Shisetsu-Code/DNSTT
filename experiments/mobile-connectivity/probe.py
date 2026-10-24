"""Temporary reachability diagnostics only. No VPN or proxy."""
import json, re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

HTML = """<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Conectividad movil</title>
<style>body{font-family:system-ui;max-width:650px;margin:3rem auto;padding:0 1rem;line-height:1.5}button{padding:12px;font-size:1rem}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eee;color:#111;padding:12px}</style>
</head><body><h2>Diagnostico HTTPS</h2><p>No es una VPN y no prueba BHTTP ni facturacion de datos.</p><p>Proba con Wi-Fi; luego apaga Wi-Fi y usa la SIM sin paquete.</p>
<button id="b">Probar conexion ahora</button><pre id="out">Sin iniciar</pre>
<script>
document.getElementById('b').onclick=async()=>{
const out=document.getElementById('out');
const nonce=Array.from(crypto.getRandomValues(new Uint8Array(12)),x=>x.toString(16).padStart(2,'0')).join('');
out.textContent='Consultando servidor...';const c=new AbortController();const timer=setTimeout(()=>c.abort(),12000);const t=performance.now();
try{const r=await fetch('/probe?nonce='+nonce+'&nocache='+Date.now(),{cache:'no-store',signal:c.signal});if(!r.ok)throw Error('HTTP '+r.status);
const d=await r.json();if(!d.ok||d.nonce!==nonce)throw Error('Desafio distinto');
out.textContent='HTTPS VERIFICADO\\nTiempo: '+Math.round(performance.now()-t)+' ms\\nHora servidor: '+d.server_utc+'\\nDesafio: '+nonce+'\\nNo demuestra datos gratuitos.';
}catch(e){out.textContent='SIN CONFIRMACION\\n'+String(e)+'\\nNo determina si BHTTP funciona.'}finally{clearTimeout(timer)}
};
</script></body></html>"""

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, fmt, *args):
        pass
    def respond(self, status, body, mime):
        self.send_response(status)
        self.send_header("Content-Type",mime)
        self.send_header("Content-Length",str(len(body)))
        self.send_header("Cache-Control","no-store, max-age=0")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Connection","close")
        self.end_headers()
        self.wfile.write(body)
        self.close_connection=True
    def do_GET(self):
        p=urlsplit(self.path)
        if p.path in ("/","/index.html"):
            return self.respond(200,HTML.encode(),"text/html; charset=utf-8")
        if p.path=="/health":
            return self.respond(200,b"OK\n","text/plain")
        if p.path=="/probe":
            vals=parse_qs(p.query).get("nonce",[])
            nonce=vals[0] if len(vals)==1 else ""
            if not re.fullmatch("[A-Za-z0-9_-]{8,64}",nonce):
                return self.respond(400,b"Bad challenge","text/plain")
            body=json.dumps({"ok":True,"nonce":nonce,"kind":"https_reachability","server_utc":datetime.now(timezone.utc).isoformat()}).encode()
            return self.respond(200,body,"application/json")
        return self.respond(404,b"Not found","text/plain")

if __name__=="__main__":
    print("Listening on 127.0.0.1:8080",flush=True)
    ThreadingHTTPServer(("127.0.0.1",8080),Handler).serve_forever()
