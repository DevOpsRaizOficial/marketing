#!/usr/bin/env python3
"""Teste end-to-end: publica o post do Dia 1 no @devopsraiz_oficial.
Usa o .env já configurado com token e IG_USER_ID.
"""
import json
import sys
import time
from pathlib import Path

import requests

# Lê config do .env local
cfg = {}
for line in Path(__file__).with_name(".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip().strip('"').strip("'")

IG_ID = cfg["IG_USER_ID"]
TOKEN = cfg["META_ACCESS_TOKEN"]
BASE = "https://graph.instagram.com/v21.0"
IMG_URL = f"{cfg['MEDIA_BASE_URL']}/01-apresentacao-capa.png"

CAPTION = """Muito prazer, eu sou o Tiago e acabei de lançar a Trilha DEVOPSRAIZ — 6 ebooks que levam você do ZERO à produção em Cloud Native, IA e DevOps.

Por que isso importa?

Porque 90% dos cursos de DevOps no Brasil ensinam conceitos soltos. Você aprende Docker aqui, Kubernetes ali, Terraform acolá — mas nunca monta um projeto COMPLETO, de ponta a ponta, do jeito que uma empresa de verdade usa.

A Trilha DEVOPSRAIZ é diferente:
→ Ebook 1: Plataforma Multi-Cloud com IA (FinOps)
→ Ebook 2: Docker, Kubernetes e Terraform
→ Ebook 3: De Projeto a SaaS (Multi-Tenant + Billing)
→ Ebook 4: IA Avançada (RAG, Agents, LLMs)
→ Ebook 5: Observabilidade e SRE
→ Ebook 6: Segurança Cloud e Compliance

Tudo integrado. Tudo com código funcional. Tudo em português.

Me segue aqui que nos próximos 30 dias vou soltar muito conteúdo útil de verdade.

👉 Link da trilha na bio.

✨ Seguir o perfil + salvar o post

#devops #cloud #aws #azure #gcp #kubernetes #docker #terraform #sre #devsecops #programacao #desenvolvimento #techbrasil #devbrasil #carreiratech #devopsraiz"""


def ok_or_die(r, ctx):
    if r.status_code >= 400:
        print(f"\n❌ Erro em {ctx} ({r.status_code}):")
        print(r.text)
        sys.exit(1)
    return r.json()


print(f"→ IG User ID: {IG_ID}")
print(f"→ Image URL:  {IMG_URL}")
print(f"→ Caption:    {len(CAPTION)} caracteres")
print()

# 1) Criar container
print("[1/3] Criando media container...")
r = requests.post(f"{BASE}/{IG_ID}/media",
                  data={"image_url": IMG_URL, "caption": CAPTION, "access_token": TOKEN},
                  timeout=60)
container = ok_or_die(r, "criar container")
container_id = container["id"]
print(f"      container_id: {container_id}")

# 2) Aguardar status FINISHED
print("\n[2/3] Aguardando Instagram processar a imagem...")
for i in range(20):
    r = requests.get(f"{BASE}/{container_id}",
                     params={"fields": "status_code", "access_token": TOKEN}, timeout=30)
    s = r.json().get("status_code")
    print(f"      tentativa {i+1}: {s}")
    if s == "FINISHED":
        break
    if s in ("ERROR", "EXPIRED"):
        print(f"❌ Container falhou: {r.json()}")
        sys.exit(1)
    time.sleep(4)
else:
    print("❌ Timeout aguardando container ficar pronto")
    sys.exit(1)

# 3) Publicar
print("\n[3/3] Publicando post...")
r = requests.post(f"{BASE}/{IG_ID}/media_publish",
                  data={"creation_id": container_id, "access_token": TOKEN}, timeout=60)
media = ok_or_die(r, "publicar")
media_id = media["id"]
print(f"\n🎉 POST PUBLICADO! media_id = {media_id}")
print(f"   Verifica em: https://www.instagram.com/devopsraiz_oficial/")

# Log
log = Path(__file__).with_name("publish_log.jsonl")
with log.open("a", encoding="utf-8") as f:
    f.write(json.dumps({
        "type": "foto", "dia": 1, "media_id": media_id,
        "container_id": container_id, "image_url": IMG_URL,
        "published_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }) + "\n")
print(f"   Log salvo em {log}")
