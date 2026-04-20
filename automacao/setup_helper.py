#!/usr/bin/env python3
"""
Setup Helper — DEVOPSRAIZ
=========================

Automatiza as partes chatas do SETUP.md:
  - Testa credenciais da Meta
  - Descobre o IG_USER_ID automaticamente
  - Troca token curto por long-lived (60 dias)
  - Lista avatares e vozes do HeyGen
  - Gera o .env final pronto

Como usar:
    python setup_helper.py meta-token SHORT_LIVED_TOKEN APP_ID APP_SECRET
    python setup_helper.py meta-discover LONG_LIVED_TOKEN
    python setup_helper.py heygen-discover HEYGEN_API_KEY
    python setup_helper.py write-env
"""

import argparse
import json
import sys
from pathlib import Path

import requests

GRAPH = "https://graph.facebook.com/v21.0"
HEYGEN = "https://api.heygen.com"


def cmd_meta_token(args):
    """Troca token de curta duração por long-lived (60 dias)."""
    r = requests.get(
        f"{GRAPH}/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": args.app_id,
            "client_secret": args.app_secret,
            "fb_exchange_token": args.short_token,
        },
        timeout=30,
    )
    if r.status_code >= 400:
        sys.exit(f"❌ Erro Meta ({r.status_code}): {r.text}")
    data = r.json()
    print("✓ Token long-lived gerado com sucesso!")
    print(f"\nCopie esse valor e guarde em local seguro:\n")
    print(f"META_ACCESS_TOKEN={data['access_token']}")
    print(f"\nValidade: ~60 dias (expira em ~{data.get('expires_in', 5184000) // 86400} dias)")


def cmd_meta_discover(args):
    """Descobre IG_USER_ID a partir do token long-lived."""
    print("→ Buscando páginas do Facebook vinculadas ao seu token...")
    r = requests.get(f"{GRAPH}/me/accounts",
                     params={"access_token": args.token}, timeout=30)
    r.raise_for_status()
    pages = r.json().get("data", [])
    if not pages:
        sys.exit("❌ Nenhuma Página Facebook encontrada. Você criou a Página DEVOPSRAIZ?")

    print(f"✓ {len(pages)} página(s) encontrada(s):\n")
    for i, p in enumerate(pages, 1):
        print(f"  {i}. {p['name']} (ID: {p['id']})")

    if len(pages) == 1:
        page = pages[0]
    else:
        escolha = input("\nQual página usar? (número): ")
        page = pages[int(escolha) - 1]

    print(f"\n→ Buscando conta Instagram Business vinculada à '{page['name']}'...")
    r = requests.get(
        f"{GRAPH}/{page['id']}",
        params={"fields": "instagram_business_account", "access_token": args.token},
        timeout=30,
    )
    r.raise_for_status()
    ig = r.json().get("instagram_business_account")
    if not ig:
        sys.exit(
            "❌ Nenhuma conta Instagram Business conectada a essa página.\n"
            "   Conecte em Instagram → Perfil → Editar perfil → Conectar Página do Facebook."
        )

    ig_id = ig["id"]
    print(f"✓ Instagram Business ID: {ig_id}")

    # Bônus: testa se o token já consegue ler a conta
    r = requests.get(f"{GRAPH}/{ig_id}",
                     params={"fields": "id,username,followers_count,media_count",
                             "access_token": args.token}, timeout=30)
    if r.ok:
        d = r.json()
        print(f"  @{d.get('username')} — {d.get('followers_count')} seguidores, {d.get('media_count')} posts")

    print(f"\nCopie pros seus secrets:\n")
    print(f"IG_USER_ID={ig_id}")


def cmd_heygen_discover(args):
    """Lista avatars e voice clones da conta HeyGen."""
    headers = {"X-Api-Key": args.api_key, "Accept": "application/json"}

    print("→ Buscando avatares...")
    r = requests.get(f"{HEYGEN}/v2/avatars", headers=headers, timeout=30)
    r.raise_for_status()
    avatars = r.json().get("data", {}).get("avatars", [])
    if avatars:
        print(f"✓ {len(avatars)} avatar(es) encontrado(s):\n")
        for a in avatars:
            name = a.get("avatar_name", "?")
            aid = a.get("avatar_id", "?")
            print(f"  • {name:<25} → avatar_id: {aid}")

    print("\n→ Buscando vozes (inclusive voice clones)...")
    r = requests.get(f"{HEYGEN}/v2/voices", headers=headers, timeout=30)
    r.raise_for_status()
    voices = r.json().get("data", {}).get("voices", [])
    # Filtra por "cloned" ou português
    cloned = [v for v in voices if v.get("emotion_support") or "clone" in str(v).lower()]
    pt = [v for v in voices if "pt" in (v.get("language") or "").lower()
          or "portuguese" in (v.get("language") or "").lower()]
    destaque = cloned[:10] + pt[:5]
    if not destaque:
        destaque = voices[:20]

    print(f"\n✓ Vozes mais relevantes (procure 'Teste1' ou sua voice clone):\n")
    for v in destaque:
        name = v.get("name", "?")
        vid = v.get("voice_id", "?")
        lang = v.get("language", "?")
        print(f"  • {name:<30} ({lang:<20}) → voice_id: {vid}")

    print(f"\nPra ver a lista completa: python heygen_client.py voices")
    print(f"\nUma vez achado, copie pros seus secrets:")
    print(f"HEYGEN_AVATAR_ID=<avatar_id_do_Teste1>")
    print(f"HEYGEN_VOICE_ID=<voice_id_da_voice_clone>")


def cmd_write_env(args):
    """Gera o .env final interativamente."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        resp = input(f".env já existe. Sobrescrever? (s/N): ")
        if resp.lower() != "s":
            sys.exit("Cancelado.")

    print("Cole os valores (deixe vazio se já tiver preenchido antes):\n")
    fields = [
        ("IG_USER_ID", "ID Instagram Business (17-18 dígitos)"),
        ("META_ACCESS_TOKEN", "Token long-lived da Meta"),
        ("HEYGEN_API_KEY", "API Key HeyGen"),
        ("HEYGEN_AVATAR_ID", "avatar_id do seu Teste1"),
        ("HEYGEN_VOICE_ID", "voice_id da voice clone"),
        ("GITHUB_TOKEN", "Personal Access Token GitHub (scope: repo)"),
        ("GITHUB_REPO", "Ex: seu-usuario/devopsraiz-instagram-assets"),
        ("MEDIA_BASE_URL", "URL pública onde ficam os PNGs (GitHub Releases)"),
    ]
    values = {}
    for key, desc in fields:
        values[key] = input(f"  {key} ({desc}): ").strip()

    content = f"""# Gerado por setup_helper.py — {env_path.parent.name}

IG_USER_ID={values['IG_USER_ID']}
META_ACCESS_TOKEN={values['META_ACCESS_TOKEN']}
MEDIA_BASE_URL={values['MEDIA_BASE_URL']}
CALENDAR_XLSX=../calendario-editorial-30-dias.xlsx
CREATIVES_DIR=../criativos

HEYGEN_API_KEY={values['HEYGEN_API_KEY']}
HEYGEN_AVATAR_ID={values['HEYGEN_AVATAR_ID']}
HEYGEN_VOICE_ID={values['HEYGEN_VOICE_ID']}

VIDEO_HOSTING=github
GITHUB_TOKEN={values['GITHUB_TOKEN']}
GITHUB_REPO={values['GITHUB_REPO']}
REGENERATE=false
"""
    env_path.write_text(content, encoding="utf-8")
    print(f"\n✓ .env gravado em {env_path}")
    print("Agora rode:  python instagram_publisher.py check")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("meta-token", help="Troca token curto por long-lived")
    t.add_argument("short_token")
    t.add_argument("app_id")
    t.add_argument("app_secret")
    t.set_defaults(func=cmd_meta_token)

    d = sub.add_parser("meta-discover", help="Descobre IG_USER_ID")
    d.add_argument("token")
    d.set_defaults(func=cmd_meta_discover)

    h = sub.add_parser("heygen-discover", help="Lista avatars + voice clones HeyGen")
    h.add_argument("api_key")
    h.set_defaults(func=cmd_heygen_discover)

    w = sub.add_parser("write-env", help="Gera .env interativamente")
    w.set_defaults(func=cmd_write_env)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
