#!/usr/bin/env python3
"""
Publica um short da serie de 30 dias DEVOPSRAIZ no Instagram como Reel.

Le caption do bloco METADADOS no .md de roteiros/shorts/short-XX-*.md,
upa o MP4 pro GitHub Releases (ou usa raw URL se VIDEO_BASE_URL configurado)
e publica via Meta Graph API com media_type=REELS.

Uso:
    python publish_short_to_ig.py --day 1
    python publish_short_to_ig.py --day 1 --dry-run
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from instagram_publisher import load_env  # noqa: E402
from reels_publisher import (  # noqa: E402
    upload_mp4, ReelsIGClient, _log,
)

ROOT = Path(__file__).resolve().parent.parent
SHORTS_MD = ROOT / "roteiros" / "shorts"
VIDEOS = ROOT / "videos_mp4"
LOG = Path(__file__).parent / "publish_log_ig_shorts.jsonl"


def find_short_md(day: int) -> Path:
    matches = sorted(SHORTS_MD.glob(f"short-{day:02d}-*.md"))
    if not matches:
        raise FileNotFoundError(f"Roteiro short-{day:02d}-*.md nao encontrado")
    return matches[0]


def find_short_mp4(day: int, slug: str) -> Path:
    p = VIDEOS / f"short-{day:02d}-{slug}.mp4"
    if not p.exists():
        raise FileNotFoundError(
            f"MP4 {p} nao encontrado - rode o pipeline antes")
    return p


def parse_caption(md_path: Path) -> str:
    """Extrai a caption do bloco METADADOS - **Caption:** ... do .md."""
    txt = md_path.read_text(encoding="utf-8")
    txt = "\n".join(line.lstrip() for line in txt.splitlines())
    m = re.search(r"\*\*Caption:\*\*\s*(.+)", txt)
    if m:
        return m.group(1).strip()
    # Fallback: pega o primeiro paragrafo de texto
    for line in txt.splitlines():
        line = line.strip()
        if line and not line.startswith(("#", ">", "-", "*", "|", "[")):
            return line[:2200]
    return "Aula nova no canal @devopsraiz - link na bio. #devopsraiz #devops #cloud #short"


def already_published(day: int) -> bool:
    if not LOG.exists():
        return False
    for line in LOG.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("dia") == day and e.get("media_id"):
            return True
    return False


def log_publish(day: int, media_id: str, video_url: str, caption: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "kind": "reel_short",
            "dia": day,
            "media_id": media_id,
            "video_url": video_url,
            "caption_preview": caption[:120],
            "publicado_em": datetime.now(timezone.utc).isoformat(),
        }, ensure_ascii=False) + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--day", type=int, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true",
                    help="ignora log de duplicatas")
    args = p.parse_args()

    cfg = load_env(Path(__file__).parent / ".env")

    if not args.force and already_published(args.day):
        print(f"  - Short do dia {args.day} ja publicado, pulando")
        return

    md = find_short_md(args.day)
    slug = md.stem.split("-", 2)[2]
    mp4 = find_short_mp4(args.day, slug)
    caption = parse_caption(md)

    print(f"=== Dia {args.day} - Short {slug} ===")
    print(f"  MP4: {mp4}")
    print(f"  Caption: {caption[:120]}...")

    if args.dry_run:
        print("  DRY RUN - nao publica")
        return

    # 1) Determina URL publico do video
    if cfg.get("VIDEO_BASE_URL"):
        video_url = f"{cfg['VIDEO_BASE_URL'].rstrip('/')}/{mp4.name}"
        print(f"  Video URL (raw repo): {video_url}")
    else:
        print("  Upload pro GitHub Releases...")
        video_url = upload_mp4(str(mp4), cfg)
        print(f"  URL: {video_url}")

    # 2) Publica como Reel
    ig = ReelsIGClient(cfg["IG_USER_ID"], cfg["META_ACCESS_TOKEN"])
    print("  Criando container Reel...")
    container_id = ig.create_reel_container(
        video_url, caption, share_to_feed=True)
    print(f"  container: {container_id}")

    print("  Aguardando Meta processar (1-5 min)...")
    ig.wait_container_ready(container_id, timeout=600)

    print("  Publicando...")
    media_id = ig.publish(container_id)
    print(f"  OK media_id={media_id}")

    log_publish(args.day, media_id, video_url, caption)


if __name__ == "__main__":
    main()
