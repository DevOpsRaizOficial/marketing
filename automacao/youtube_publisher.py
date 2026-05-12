#!/usr/bin/env python3
"""
YouTube Publisher — DEVOPSRAIZ
==============================

Sobe vídeos pra um canal YouTube via API v3 do Google.
Suporta vídeos públicos, unlisted e privados, com schedule (publishAt),
playlist e thumb customizada.

Fluxo:
  1. Lê metadados do roteiro .md (linha de YAML frontmatter ou bloco METADADOS)
  2. Faz upload resumível do MP4 em ../videos_mp4/
  3. (Opcional) sobe thumb customizada
  4. (Opcional) adiciona à playlist da série "30 dias DEVOPSRAIZ"
  5. Loga em ../publish_log_youtube.jsonl

Credenciais (.env):
  YOUTUBE_CHANNEL_ID
  YOUTUBE_CLIENT_ID
  YOUTUBE_CLIENT_SECRET
  YOUTUBE_REFRESH_TOKEN   # obter via get_youtube_token.py (one-time setup)
  YOUTUBE_PLAYLIST_AULAS  # opcional
  YOUTUBE_PLAYLIST_SHORTS # opcional

Uso:
  # publicar aula 1
  python youtube_publisher.py --kind aula --day 1

  # publicar short 1
  python youtube_publisher.py --kind short --day 1

  # publicar todos como "private" (revisão antes de publicar)
  python youtube_publisher.py --kind aula --all --privacy private

Pré-requisitos:
  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    sys.exit("Dependências ausentes. Roda:\n"
              "  pip install google-api-python-client google-auth-oauthlib "
              "google-auth-httplib2")

# ==============================================================================
# Paths
# ==============================================================================
ROOT = Path(__file__).resolve().parent.parent
VIDEOS = ROOT / "videos_mp4"
AULAS_MD = ROOT / "roteiros" / "aulas"
SHORTS_MD = ROOT / "roteiros" / "shorts"
LOG = ROOT / "automacao" / "publish_log_youtube.jsonl"


# ==============================================================================
# YouTube auth (OAuth refresh token flow — sem precisar abrir browser na CI)
# ==============================================================================
def get_youtube_client():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube"],
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


# ==============================================================================
# Metadados parser
# ==============================================================================
def parse_metadata(md_path: Path) -> dict:
    """Extrai título, descrição, tags, etc. do bloco METADADOS no .md."""
    txt = md_path.read_text(encoding="utf-8")
    block = re.search(r"## METADADOS YOUTUBE\n(.*?)(?=\n## |\Z)",
                       txt, re.DOTALL)
    out = {
        "title": md_path.stem.replace("-", " ").title()[:95],
        "description": "",
        "tags": ["devopsraiz"],
        "category_id": "27",  # Education
    }
    if not block:
        # tenta extrair só o título da primeira linha h1
        h1 = re.search(r"^#\s+(.+)$", txt, re.MULTILINE)
        if h1:
            out["title"] = h1.group(1).strip()[:95]
        return out

    body = block.group(1)
    t = re.search(r"\*\*Título:\*\*\s*(.+)", body)
    if t:
        out["title"] = t.group(1).strip()[:95]
    d = re.search(r"\*\*Descrição:\*\*\s*\n(.*?)(?=\n\s*-\s*\*\*|\Z)",
                   body, re.DOTALL)
    if d:
        out["description"] = re.sub(r"^\s{4,}", "", d.group(1),
                                      flags=re.MULTILINE).strip()
    tg = re.search(r"\*\*Tags:\*\*\s*(.+)", body)
    if tg:
        out["tags"] = [t.strip() for t in tg.group(1).split(",")][:30]
    return out


# ==============================================================================
# Upload
# ==============================================================================
def upload_video(yt, mp4_path: Path, meta: dict, privacy: str,
                  publish_at: Optional[str] = None,
                  is_short: bool = False) -> dict:
    """Upload resumível. Retorna o resource do vídeo."""
    body = {
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId": meta.get("category_id", "27"),
            "defaultLanguage": "pt-BR",
            "defaultAudioLanguage": "pt-BR",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }
    if publish_at and privacy == "private":
        # Schedule pra ficar público no horário
        body["status"]["publishAt"] = publish_at
    if is_short:
        # YouTube identifica Short pelo aspect + duração, mas adicionamos hashtag
        body["snippet"]["description"] = "#Shorts\n\n" + body["snippet"]["description"]

    media = MediaFileUpload(str(mp4_path), chunksize=8 * 1024 * 1024,
                              resumable=True, mimetype="video/mp4")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    print(f"  uploading {mp4_path.name} ({mp4_path.stat().st_size / 1024 / 1024:.1f} MB)...")
    res = None
    while res is None:
        status, res = req.next_chunk()
        if status:
            print(f"    progress: {int(status.progress() * 100)}%")
    return res


def upload_thumb(yt, video_id: str, thumb_path: Path):
    if not thumb_path.exists():
        return
    media = MediaFileUpload(str(thumb_path), mimetype="image/png")
    yt.thumbnails().set(videoId=video_id, media_body=media).execute()


def add_to_playlist(yt, video_id: str, playlist_id: str):
    if not playlist_id:
        return
    yt.playlistItems().insert(
        part="snippet",
        body={"snippet": {"playlistId": playlist_id,
                          "resourceId": {"kind": "youtube#video",
                                          "videoId": video_id}}},
    ).execute()


# ==============================================================================
# Log
# ==============================================================================
def log_publish(kind: str, day: int, video_id: str, mp4: str,
                  title: str, privacy: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "kind": kind, "dia": day, "video_id": video_id,
            "url": f"https://youtu.be/{video_id}",
            "mp4": mp4, "title": title, "privacy": privacy,
            "publicado_em": datetime.now(timezone.utc).isoformat(),
        }, ensure_ascii=False) + "\n")


def already_published(kind: str, day: int) -> bool:
    if not LOG.exists():
        return False
    for line in LOG.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("kind") == kind and e.get("dia") == day:
            return True
    return False


# ==============================================================================
# Main
# ==============================================================================
def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kind", choices=["aula", "short"], required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--day", type=int)
    g.add_argument("--all", action="store_true")
    p.add_argument("--privacy", choices=["private", "unlisted", "public"],
                    default="private",
                    help="private (padrão, recomendado pra revisar antes)")
    p.add_argument("--publish-at",
                    help="ISO 8601 UTC pra schedule (ex: 2026-05-12T14:00:00Z). "
                         "Se setado, --privacy fica 'private'.")
    p.add_argument("--force", action="store_true",
                    help="ignora log de duplicatas")
    args = p.parse_args()

    load_env()
    yt = get_youtube_client()

    src_dir = AULAS_MD if args.kind == "aula" else SHORTS_MD
    playlist_env = (
        "YOUTUBE_PLAYLIST_AULAS" if args.kind == "aula"
        else "YOUTUBE_PLAYLIST_SHORTS"
    )
    playlist = os.environ.get(playlist_env, "")

    days = list(range(1, 31)) if args.all else [args.day]
    for d in days:
        if not args.force and already_published(args.kind, d):
            print(f"  ✓ Dia {d} {args.kind} já publicado, pulando")
            continue
        md_matches = sorted(src_dir.glob(f"{args.kind}-{d:02d}-*.md"))
        if not md_matches:
            print(f"  ⚠ Sem roteiro pra dia {d}")
            continue
        md = md_matches[0]
        slug = md.stem.split("-", 2)[2]
        mp4 = VIDEOS / f"{args.kind}-{d:02d}-{slug}.mp4"
        if not mp4.exists():
            print(f"  ⚠ Dia {d}: MP4 ainda não gerado em {mp4}")
            continue
        thumb = VIDEOS / f"{args.kind}-{d:02d}-{slug}.thumb.png"

        meta = parse_metadata(md)
        try:
            res = upload_video(yt, mp4, meta, args.privacy,
                                publish_at=args.publish_at,
                                is_short=(args.kind == "short"))
            vid = res["id"]
            if thumb.exists():
                upload_thumb(yt, vid, thumb)
            if playlist:
                add_to_playlist(yt, vid, playlist)
            log_publish(args.kind, d, vid, str(mp4), meta["title"],
                         args.privacy)
            print(f"  ✓ Dia {d}: https://youtu.be/{vid}")
        except HttpError as e:
            print(f"  ❌ Dia {d}: {e}")
        except Exception as e:
            print(f"  ❌ Dia {d}: {e}")


if __name__ == "__main__":
    main()
