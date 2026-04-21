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
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from instagram_publisher import (
    load_env, load_calendar, publish_post, _today_day_offset
)
from reels_publisher import REEL_MAP, generate_video, publish_reel


BRT = timezone(timedelta(hours=-3))
TIME_WINDOW_MINUTES = 120  # janela de ±2h cobre todos os horários do calendário


def _scheduled_today_is_near_now(post: dict) -> tuple[bool, str]:
    """Retorna (True, razão) se o horário programado do post está
    dentro de ±90min do horário atual (BRT). False pro contrário."""
    horario = str(post.get("Horario", "")).strip()
    if not horario or ":" not in horario:
        return True, "post sem horário definido — publica"
    try:
        h, m = [int(x) for x in horario.split(":")[:2]]
    except ValueError:
        return True, f"horário inválido '{horario}' — publica"
    now_brt = datetime.now(BRT)
    scheduled = now_brt.replace(hour=h, minute=m, second=0, microsecond=0)
    delta = abs((now_brt - scheduled).total_seconds()) / 60
    msg = f"agora={now_brt.strftime('%H:%M')} BRT, programado={horario} BRT, delta={delta:.0f}min"
    if delta <= TIME_WINDOW_MINUTES:
        return True, f"dentro da janela ({msg})"
    return False, f"fora da janela ({msg}, limite=±{TIME_WINDOW_MINUTES}min)"


def _already_published_today(day: int, log_path: Path) -> bool:
    """Verifica se esse dia já foi publicado (via publish_log.jsonl)."""
    if not log_path.exists():
        return False
    today_str = datetime.now(BRT).strftime("%Y-%m-%d")
    for line in log_path.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except Exception:
            continue
        if entry.get("dia") != day:
            continue
        pub_at = entry.get("publicado_em") or entry.get("published_at", "")
        if pub_at.startswith(today_str):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Orchestrator diário do @devopsraiz_oficial")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--day", type=int)
    g.add_argument("--today", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="Ignora janela de horário e log de duplicatas")
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

    # Proteção 1: evitar publicação fora da janela de horário programado
    if not args.force and not args.dry_run:
        near, reason = _scheduled_today_is_near_now(post)
        if not near:
            print(f"⏭  Pulando: {reason}")
            print(f"   (use --force pra forçar publicação independente do horário)")
            sys.exit(0)
        print(f"✓ Horário: {reason}")

    # Proteção 2: evitar publicar o mesmo dia 2x
    log_path = Path(__file__).parent / "publish_log.jsonl"
    if not args.force and _already_published_today(day, log_path):
        print(f"⏭  Dia {day} já foi publicado hoje (publish_log.jsonl). Pulando.")
        sys.exit(0)

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
