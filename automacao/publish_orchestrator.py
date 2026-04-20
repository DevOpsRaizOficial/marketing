#!/usr/bin/env python3
"""
Orchestrator — publica o post do dia escolhendo o publisher certo.

Lê a aba "Calendario 30 dias" e, baseado na coluna 'Formato', decide:
  - Se for Reel  → reels_publisher.auto (gera via HeyGen + publica)
  - Se for Story → stories_publisher (se existir MP4 em /videos_mp4)
  - Se for Carrossel/Post único → instagram_publisher.publish_post
                                   (posta PNG de /criativos)

Usado pelo GitHub Actions / cron para disparar o post do dia atual.

Uso:
    python publish_orchestrator.py --today
    python publish_orchestrator.py --day 5
    python publish_orchestrator.py --today --dry-run
"""

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from instagram_publisher import (
    load_env, load_calendar, publish_post, _today_day_offset
)
from reels_publisher import REEL_MAP, generate_video, publish_reel


def main():
    parser = argparse.ArgumentParser(description="Orchestrator diário do @devopsraiz_oficial")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--day", type=int)
    g.add_argument("--today", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    day = args.day if args.day else _today_day_offset()
    if day < 1 or day > 30:
        print(f"ℹ Dia {day} fora do calendário (1-30). Nada a publicar.")
        sys.exit(0)

    cfg = load_env(Path(__file__).parent / ".env")
    cfg["CALENDAR_XLSX_ABS"] = str(
        (Path(__file__).parent / cfg.get(
            "CALENDAR_XLSX", "../calendario-editorial-30-dias.xlsx")).resolve()
    )
    posts = load_calendar(cfg["CALENDAR_XLSX_ABS"])
    post = next((p for p in posts if int(p["Dia"]) == day), None)
    if not post:
        sys.exit(f"Post do dia {day} não encontrado.")

    formato = (post.get("Formato") or "").lower()
    print(f"\n================================================================")
    print(f"Dia {day} ({post['Data (2026)']} {post['Horario']})")
    print(f"Formato: {post['Formato']}")
    print(f"Título:  {post['Titulo / Gancho']}")
    print(f"================================================================\n")

    if "reel" in formato:
        if day not in REEL_MAP:
            print(f"⚠ Reel marcado no calendário mas sem roteiro em REEL_MAP. Pulando.")
            return
        if args.dry_run:
            print("[DRY-RUN] geraria vídeo via HeyGen e publicaria como Reel.")
            return
        mp4 = generate_video(day, cfg)
        publish_reel(day, cfg, mp4)
        return

    if "story" in formato:
        print("ℹ Stories não são publicados automaticamente (use Meta app).")
        print("  Legenda de apoio copiada na tela pra você postar manualmente:")
        print("  ---")
        print(post.get("Legenda Completa"))
        print("  ---")
        return

    # Default: foto/carrossel → usa instagram_publisher.publish_post
    publish_post(post, cfg, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
