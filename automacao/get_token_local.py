#!/usr/bin/env python3
"""
OAuth Token Grabber — DEVOPSRAIZ
================================

Inicia um mini-servidor HTTP em localhost:8080 e abre o browser
na página de autorização da Meta. Depois que você autoriza, a Meta
redireciona pro localhost e este script captura o token automaticamente.

Como usar:
    1. Adicione no app Meta o redirect URI:  http://localhost:8080/callback
       (em Login do Facebook → Configurações → URIs válidos)
    2. Rode:  python get_token_local.py
    3. Seu navegador abre na página de autorização
    4. Autorize
    5. O token é capturado automaticamente e salvo em .env

Requisitos: pacotes padrão do Python (nenhuma instalação extra).
"""

import http.server
import socketserver
import webbrowser
import urllib.parse
import threading
import sys
import os
from pathlib import Path

APP_ID = "931502926470156"
CONFIG_ID = "933143862823401"
REDIRECT_URI = "http://localhost:8080/callback"
PORT = 8080

SCOPES = ",".join([
    "instagram_business_basic",
    "instagram_business_content_publish",
    "pages_show_list",
    "pages_read_engagement",
    "business_management",
])

OAUTH_URL = (
    f"https://www.facebook.com/v21.0/dialog/oauth?"
    f"client_id={APP_ID}&"
    f"redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}&"
    f"response_type=token&"
    f"scope={urllib.parse.quote(SCOPES, safe=',')}"
)

# Como o response_type=token coloca o token no FRAGMENT (#) que não chega ao servidor,
# servimos uma página HTML que pega o fragment via JavaScript e posta via fetch.
HTML_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>DEVOPSRAIZ OAuth</title>
<style>
  body { font-family: system-ui; background: #0F172A; color: #E2E8F0;
         display: flex; align-items: center; justify-content: center;
         height: 100vh; margin: 0; }
  .box { text-align: center; padding: 40px; background: #1E293B;
         border-radius: 12px; max-width: 500px; }
  .ok { color: #10B981; font-size: 48px; margin-bottom: 16px; }
  .err { color: #EF4444; font-size: 48px; margin-bottom: 16px; }
  code { background: #0F172A; padding: 8px 12px; border-radius: 4px;
         display: block; margin: 16px 0; word-break: break-all; font-size: 12px; }
</style></head>
<body><div class="box" id="status">
  <div class="ok">✓</div>
  <h1>Aguarde...</h1>
  <p>Processando autorização do Facebook.</p>
</div>
<script>
  const fragment = window.location.hash.substring(1);
  if (!fragment) {
    document.getElementById('status').innerHTML =
      '<div class="err">✗</div><h1>Sem token na URL</h1><p>Fragment vazio. Tente novamente.</p>';
  } else {
    const params = new URLSearchParams(fragment);
    const token = params.get('access_token');
    if (token) {
      fetch('/save?token=' + encodeURIComponent(token))
        .then(r => r.text())
        .then(msg => {
          document.getElementById('status').innerHTML =
            '<div class="ok">✓</div><h1>Token capturado!</h1>' +
            '<p>Pode fechar esta janela e voltar ao terminal.</p>' +
            '<code>' + token.substring(0, 40) + '...</code>';
        });
    } else {
      document.getElementById('status').innerHTML =
        '<div class="err">✗</div><h1>Erro</h1><pre>' + fragment + '</pre>';
    }
  }
</script>
</body></html>"""

captured_token = {"value": None}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/callback"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path.startswith("/save"):
            q = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(q)
            token = params.get("token", [""])[0]
            captured_token["value"] = token
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
            # Desliga o servidor depois de capturar
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Silencia logs do servidor


def main():
    print("=" * 60)
    print("DEVOPSRAIZ — OAuth Token Grabber")
    print("=" * 60)
    print(f"\nIniciando servidor em http://localhost:{PORT}")
    print(f"Abrindo navegador para autorização...\n")

    # Inicia servidor em thread separada
    httpd = socketserver.TCPServer(("localhost", PORT), Handler)

    # Abre navegador
    webbrowser.open(OAUTH_URL)

    print("Aguardando você autorizar no navegador...")
    print("(se não abrir sozinho, cole esta URL manualmente:)\n")
    print(OAUTH_URL)
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nCancelado pelo usuário.")
        sys.exit(1)

    if not captured_token["value"]:
        print("\n❌ Nenhum token capturado. Tente de novo.")
        sys.exit(1)

    token = captured_token["value"]
    print(f"\n✓ Token short-lived capturado: {token[:40]}...")

    # Salva num arquivo temporário pra o próximo passo pegar
    Path("token_short.txt").write_text(token, encoding="utf-8")
    print(f"✓ Salvo em {Path('token_short.txt').absolute()}")
    print("\nPróximo passo: enviar esse token ao Claude no chat do Cowork.")
    print("Ele vai trocar por um long-lived (60 dias) e descobrir o IG_USER_ID.\n")


if __name__ == "__main__":
    main()
