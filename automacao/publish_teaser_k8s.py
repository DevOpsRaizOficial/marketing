#!/usr/bin/env python3
"""
Teaser carousel K8S — publica os 5 slides do lead magnet via API.

Standalone porque é um post EXTRA fora do calendário XLSX.
Disparado manualmente via .github/workflows/publish-teaser-k8s.yml

Uso:
    python publish_teaser_k8s.py [--dry-run]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from instagram_publisher import IGClient, load_env

# 5 slides do teaser
SLIDE_FILES = [
    "extra-01-teaser-k8s-slide-01.png",
    "extra-01-teaser-k8s-slide-02.png",
    "extra-01-teaser-k8s-slide-03.png",
    "extra-01-teaser-k8s-slide-04.png",
    "extra-01-teaser-k8s-slide-05.png",
]

# Legenda completa do post
LEGENDA = """TODO dev junior já pegou um desses no kubectl describe pod:

→ CrashLoopBackOff
→ ImagePullBackOff
→ OOMKilled
→ Pending (Unschedulable)
→ Evicted

Cada um tem causa raiz diferente. E uma forma RÁPIDA de diagnosticar.

Eu compilei os 10 erros mais comuns de Kubernetes num PDF gratuito de 7 páginas, com:

✅ O que é cada erro
✅ Por que rola na prática
✅ Como resolver em 5 minutos (com comandos kubectl prontos)

É um recorte do Ebook 2 da Trilha DEVOPSRAIZ.

Quer pegar de graça?

💬 Comenta K8S nesse post que mando o PDF direto no seu DM 📨

Bônus: quem entrar na lista pelo K8S agora ganha cupom FUNDADOR 20% off na Trilha completa (válido só pros 100 primeiros).

#devops #cloud #aws #kubernetes #k8s #docker #terraform #devbrasil #carreiratech #devopsraiz #crashloopbackoff #devsecops"""


def _append_log(entry: dict):
    log_path = Path(__file__).parent / "publish_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Publica teaser K8S no @devopsraiz_oficial")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem publicar")
    args = parser.parse_args()

    cfg = load_env(Path(__file__).parent / ".env")
    base = cfg["MEDIA_BASE_URL"].rstrip("/")
    urls = [f"{base}/{f}" for f in SLIDE_FILES]

    print("=" * 60)
    print("TEASER K8S — Publicação one-shot do lead magnet")
    print("=" * 60)
    print(f"Slides: {len(urls)}")
    for i, u in enumerate(urls, 1):
        print(f"  {i}. {u}")
    print(f"\nLegenda ({len(LEGENDA)} chars):")
    print(LEGENDA[:200] + "...\n")

    if args.dry_run:
        print("[DRY-RUN] Não chamando API.")
        return

    ig = IGClient(cfg["IG_USER_ID"], cfg["META_ACCESS_TOKEN"])
    print("→ Criando containers dos slides + carousel container...")
    container_id = ig.create_carousel_container(urls, LEGENDA)
    print(f"  Carousel container: {container_id}")

    print("→ Aguardando processamento (~1-2 min)...")
    ig.wait_container_ready(container_id)

    print("→ Publicando...")
    media_id = ig.publish(container_id)
    print(f"\n✓ TEASER K8S PUBLICADO! Media ID: {media_id}")

    _append_log({
        "type": "carousel",
        "dia": "extra-teaser-k8s",
        "media_id": media_id,
        "slides": len(urls),
        "publicado_em": datetime.utcnow().isoformat(),
    })


if __name__ == "__main__":
    main()
