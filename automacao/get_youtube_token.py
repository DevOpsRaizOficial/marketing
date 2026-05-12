#!/usr/bin/env python3
"""
One-time setup pra pegar o YOUTUBE_REFRESH_TOKEN.
Roda local UMA vez, autoriza no browser, copia o refresh_token pro .env.

Pré-requisitos:
  1. Criar projeto em https://console.cloud.google.com
  2. Habilitar YouTube Data API v3
  3. OAuth Consent Screen → External, adicionar seu email como test user
  4. Credentials → OAuth Client ID → Desktop App
  5. Baixar credentials.json e salvar nessa pasta

Uso:
  pip install google-auth-oauthlib
  python get_youtube_token.py
"""

import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

CRED_FILE = Path(__file__).parent / "credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]

if not CRED_FILE.exists():
    print("ERRO: credentials.json não encontrado.")
    print("Baixe em https://console.cloud.google.com/apis/credentials")
    raise SystemExit(1)

flow = InstalledAppFlow.from_client_secrets_file(str(CRED_FILE), SCOPES)
creds = flow.run_local_server(port=0)

data = json.loads(CRED_FILE.read_text())
client = data.get("installed") or data.get("web")
print("\n=== Adicione essas linhas ao seu .env ===\n")
print(f"YOUTUBE_CLIENT_ID={client['client_id']}")
print(f"YOUTUBE_CLIENT_SECRET={client['client_secret']}")
print(f"YOUTUBE_REFRESH_TOKEN={creds.refresh_token}")
print("\n=== Não esqueça de configurar YOUTUBE_PLAYLIST_AULAS e YOUTUBE_PLAYLIST_SHORTS ===\n")
