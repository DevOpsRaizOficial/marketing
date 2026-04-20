#!/usr/bin/env python3
"""
HeyGen API Client — DEVOPSRAIZ
==============================

Requer plano HeyGen Team ou Enterprise (Creator não tem API).

Fluxo:
  1. Lê script do roteiro (.txt em /roteiros)
  2. Chama POST /v2/video/generate com avatar_id + voice_id + texto
  3. Faz polling em /v1/video_status.get até ficar "completed"
  4. Baixa o MP4 final
  5. Retorna o caminho local do arquivo

Docs oficiais: https://docs.heygen.com/reference/video-generation-api

Uso standalone (testar):
    python heygen_client.py --script ../roteiros/reel-dia-01-apresentacao.txt \
                            --output ../videos_mp4/reel-dia-01.mp4
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests


HEYGEN_API_BASE = "https://api.heygen.com"


class HeyGenError(RuntimeError):
    pass


class HeyGenClient:
    def __init__(self, api_key: str, avatar_id: str, voice_id: str):
        if not api_key:
            raise HeyGenError("HEYGEN_API_KEY não configurado")
        if not avatar_id or not voice_id:
            raise HeyGenError("HEYGEN_AVATAR_ID e HEYGEN_VOICE_ID são obrigatórios")
        self.key = api_key
        self.avatar_id = avatar_id
        self.voice_id = voice_id
        self.session = requests.Session()
        self.session.headers.update({
            "X-Api-Key": self.key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    # ----------------------------------------------------- descoberta --
    def list_avatars(self) -> list[dict]:
        """Lista todos os avatars da conta — útil pra descobrir o avatar_id."""
        r = self.session.get(f"{HEYGEN_API_BASE}/v2/avatars")
        r.raise_for_status()
        return r.json().get("data", {}).get("avatars", [])

    def list_voices(self) -> list[dict]:
        """Lista todas as vozes (inclusive voice clones) — útil pra descobrir o voice_id."""
        r = self.session.get(f"{HEYGEN_API_BASE}/v2/voices")
        r.raise_for_status()
        return r.json().get("data", {}).get("voices", [])

    def remaining_quota(self) -> dict:
        """Retorna minutos restantes no plano."""
        r = self.session.get(f"{HEYGEN_API_BASE}/v1/user/remaining_quota")
        r.raise_for_status()
        return r.json().get("data", {})

    # -------------------------------------------------- geração de vídeo --
    def generate(self, script_text: str, aspect_ratio: str = "9:16",
                 background_color: str = "#0F172A") -> str:
        """
        Dispara a geração de um vídeo com avatar + voice clone.
        Retorna o video_id para polling.
        """
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": self.avatar_id,
                        "avatar_style": "normal",
                    },
                    "voice": {
                        "type": "text",
                        "input_text": script_text,
                        "voice_id": self.voice_id,
                        "speed": 1.0,
                    },
                    "background": {
                        "type": "color",
                        "value": background_color,
                    },
                }
            ],
            "dimension": {"width": 720, "height": 1280}
            if aspect_ratio == "9:16"
            else {"width": 1280, "height": 720},
            "test": False,
            "caption": True,
        }
        r = self.session.post(f"{HEYGEN_API_BASE}/v2/video/generate", json=payload)
        if r.status_code >= 400:
            raise HeyGenError(f"Falha ao iniciar geração ({r.status_code}): {r.text}")
        return r.json()["data"]["video_id"]

    def wait_for_video(self, video_id: str, timeout: int = 900, poll_interval: int = 15) -> str:
        """
        Faz polling até o vídeo ficar pronto. Retorna a URL de download do MP4.
        Timeout padrão: 15 minutos.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            r = self.session.get(
                f"{HEYGEN_API_BASE}/v1/video_status.get",
                params={"video_id": video_id},
            )
            r.raise_for_status()
            d = r.json().get("data", {})
            status = d.get("status")
            if status == "completed":
                url = d.get("video_url")
                if not url:
                    raise HeyGenError(f"Vídeo completo mas sem URL: {d}")
                return url
            if status == "failed":
                raise HeyGenError(f"HeyGen falhou: {d.get('error')}")
            print(f"  … HeyGen status: {status} (aguardando {poll_interval}s)")
            time.sleep(poll_interval)
        raise TimeoutError(f"Vídeo {video_id} não ficou pronto em {timeout}s")

    @staticmethod
    def download(url: str, output_path: str) -> str:
        """Baixa o MP4 do URL público de download."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with requests.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 20):
                    f.write(chunk)
        return output_path


# ------------------------------------------------------------------- cli --
def _load_env(env_path: str = ".env") -> dict:
    cfg = {}
    p = Path(env_path)
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    for k in ["HEYGEN_API_KEY", "HEYGEN_AVATAR_ID", "HEYGEN_VOICE_ID"]:
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("generate", help="Gera um vídeo a partir de um roteiro .txt")
    gen.add_argument("--script", required=True, help="Caminho do .txt com o roteiro")
    gen.add_argument("--output", required=True, help="Caminho do MP4 de saída")

    sub.add_parser("quota", help="Mostra minutos restantes no plano HeyGen")
    sub.add_parser("avatars", help="Lista avatares disponíveis (para achar avatar_id)")
    sub.add_parser("voices", help="Lista vozes disponíveis (para achar voice_id)")

    args = parser.parse_args()
    cfg = _load_env(Path(__file__).parent / ".env")

    if args.cmd in ("quota", "avatars", "voices"):
        api_key = cfg.get("HEYGEN_API_KEY")
        if not api_key:
            sys.exit("HEYGEN_API_KEY não configurado no .env")
        client = HeyGenClient(api_key, "dummy", "dummy")
        if args.cmd == "quota":
            print(json.dumps(client.remaining_quota(), indent=2))
        elif args.cmd == "avatars":
            for a in client.list_avatars():
                print(f"  {a.get('avatar_id')}  —  {a.get('avatar_name')}")
        elif args.cmd == "voices":
            for v in client.list_voices():
                print(f"  {v.get('voice_id')}  —  {v.get('name')}  ({v.get('language')})")
        return

    if args.cmd == "generate":
        script_text = Path(args.script).read_text(encoding="utf-8")
        # Remove cabeçalhos de comentário (linhas antes do divider ====)
        if "==========" in script_text:
            parts = script_text.split("===============================================")
            if len(parts) >= 2:
                script_text = parts[-1].strip()
        # Remove linhas entre colchetes (indicações de direção)
        clean_lines = []
        for line in script_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                continue
            clean_lines.append(line)
        script_text = "\n".join(clean_lines).strip()

        client = HeyGenClient(
            cfg["HEYGEN_API_KEY"],
            cfg["HEYGEN_AVATAR_ID"],
            cfg["HEYGEN_VOICE_ID"],
        )
        print(f"→ Gerando vídeo ({len(script_text)} caracteres de script)")
        video_id = client.generate(script_text)
        print(f"  Video ID: {video_id}")
        print("  Aguardando processamento (~2-8 min)...")
        url = client.wait_for_video(video_id)
        print(f"  MP4 disponível em: {url[:80]}...")
        path = client.download(url, args.output)
        print(f"✓ Baixado em {path}")


if __name__ == "__main__":
    main()
