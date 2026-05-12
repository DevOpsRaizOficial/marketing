#!/usr/bin/env python3
"""
HeyGen Mateo Pipeline — DEVOPSRAIZ
==================================

Para cada roteiro em ../roteiros/aulas/ (long-form 10 min) e
../roteiros/shorts/ (10 segundos), este pipeline:

  1. Faz parse do markdown e separa em SEGMENTOS por timestamp
  2. Extrai os [PIXAR: ...] markers de cada segmento
  3. Para cada segmento:
       a. Gera o áudio + Mateo falando via HeyGen API
       b. Gera a cena Pixar via Replicate (SDXL com prompt "pixar-style 3D
          animation") ou OpenAI gpt-image-1, salvando como PNG
       c. Anima a cena Pixar para um clipe de 5-8s usando ffmpeg
          (zoom/pan Ken Burns) — se preferir vídeo real, troca por
          Runway/Pika via API
  4. Composição final com ffmpeg:
       - Mateo aparece em picture-in-picture canto inferior direito
       - Cena Pixar ocupa a tela cheia (ou troca pra Mateo full quando
         não há marker no segmento)
       - Legendas burned-in com fonte Helvetica branca
       - Logo DEVOPSRAIZ canto superior esquerdo
       - Música trilha lo-fi tech (arquivo em ../assets/bgm.mp3)
  5. Saída em ../videos_mp4/aula-XX.mp4 (16:9) ou short-XX.mp4 (9:16)

Variáveis de ambiente esperadas (.env):
  HEYGEN_API_KEY
  HEYGEN_AVATAR_ID_MATEO   # avatar do Mateo
  HEYGEN_VOICE_ID_MATEO    # voice clone do Mateo (PT-BR)
  REPLICATE_API_TOKEN       # ou OPENAI_API_KEY se preferir DALL-E
  PIXAR_BACKEND             # "replicate" (padrão) | "openai" | "runway"
  BGM_PATH                  # caminho pro mp3 de fundo (opcional)

Uso:
  # gera 1 aula
  python heygen_mateo_pipeline.py aula --day 1

  # gera 1 short
  python heygen_mateo_pipeline.py short --day 1

  # gera todas as aulas (idempotente, pula MP4 já existente)
  python heygen_mateo_pipeline.py aula --all

  # gera só as cenas pixar (PNG), sem chamar HeyGen — útil pra preview
  python heygen_mateo_pipeline.py aula --day 1 --pixar-only

Pré-requisitos do shell:
  - ffmpeg >= 6.0   (apt install ffmpeg)
  - Python 3.10+   (já requirido pelos outros scripts)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import requests

# ==============================================================================
# Paths
# ==============================================================================
ROOT = Path(__file__).resolve().parent.parent
AULAS_DIR = ROOT / "roteiros" / "aulas"
SHORTS_DIR = ROOT / "roteiros" / "shorts"
VIDEOS_OUT = ROOT / "videos_mp4"
PIXAR_CACHE = ROOT / "videos_mp4" / ".pixar_cache"  # PNGs intermediárias
VIDEOS_OUT.mkdir(parents=True, exist_ok=True)
PIXAR_CACHE.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# Config
# ==============================================================================
HEYGEN_API_BASE = "https://api.heygen.com"
PIXAR_STYLE_PREFIX = (
    "Pixar-style 3D animation, cinematic lighting, vibrant saturated colors, "
    "soft global illumination, shallow depth of field, character design "
    "reminiscent of Pixar/Disney studios 2025, no on-screen text, "
    "16:9 cinematic composition, ultra-detailed, hero shot. Subject: "
)
SHORT_PIXAR_STYLE_PREFIX = (
    "Pixar-style 3D animation, ultra-vibrant saturated colors, dynamic "
    "camera angle, 9:16 vertical composition, energetic short-form video "
    "thumbnail, no on-screen text, character close-up. Subject: "
)


# ==============================================================================
# Helpers
# ==============================================================================
@dataclass
class Segment:
    """Um segmento do roteiro (entre dois ## timestamps)."""
    title: str           # ex "0:30 — PONTO 1: ..."
    speech: str          # texto que o Mateo vai falar
    pixar_prompts: list[str] = field(default_factory=list)


def parse_roteiro(md_path: Path) -> list[Segment]:
    """Parse um arquivo de roteiro markdown e retorna lista de Segments."""
    txt = md_path.read_text(encoding="utf-8")
    # Normaliza: remove leading whitespace de cada linha (deixa o parser robusto
    # a artefatos do textwrap.dedent que sobram quando o template tem
    # interpolações multi-linha).
    txt = "\n".join(line.lstrip() for line in txt.splitlines())

    # Quebra em segmentos por linhas que começam com '## '
    parts = re.split(r"\n## ", txt)
    segs: list[Segment] = []
    for chunk in parts[1:]:
        # primeira linha é o título
        title, _, body = chunk.partition("\n")
        title = title.strip()
        if title.upper().startswith("METADADOS"):
            break  # ignora bloco de metadados YouTube

        # extrai todos os [PIXAR: ...] do segmento
        pixar = re.findall(r"\[PIXAR:\s*([^\]]+?)\s*\]", body, flags=re.DOTALL)

        # speech = tudo MENOS os [PIXAR: ...] e linhas em (parênteses)
        speech_raw = re.sub(r"\[PIXAR:[^\]]*\]", "", body)
        speech_raw = re.sub(r"^\(.*?\)\s*", "", speech_raw,
                             flags=re.MULTILINE | re.DOTALL)
        speech_raw = re.sub(r"\n{3,}", "\n\n", speech_raw).strip()

        # remove markdown leve (bold, italics)
        speech_clean = re.sub(r"[*_`]+", "", speech_raw)
        # remove linhas só com '---' ou bullets
        speech_clean = "\n".join(
            line for line in speech_clean.splitlines()
            if line.strip() and not line.strip().startswith("-")
            and not re.match(r"^[#>]+\s*$", line)
        )

        if speech_clean:
            segs.append(Segment(
                title=title,
                speech=speech_clean.strip(),
                pixar_prompts=pixar,
            ))
    return segs


def assert_ffmpeg():
    if not shutil.which("ffmpeg"):
        sys.exit("ERRO: ffmpeg não encontrado. Instala com: sudo apt install ffmpeg")


# ==============================================================================
# HeyGen — gera o Mateo falando o segmento
# ==============================================================================
class HeyGenMateo:
    def __init__(self, api_key: str, avatar_id: str, voice_id: str):
        if not all([api_key, avatar_id, voice_id]):
            raise RuntimeError(
                "HEYGEN_API_KEY, HEYGEN_AVATAR_ID_MATEO e HEYGEN_VOICE_ID_MATEO "
                "são obrigatórios no .env")
        self.s = requests.Session()
        self.s.headers.update({
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.avatar_id = avatar_id
        self.voice_id = voice_id

    def generate(self, script_text: str, aspect_ratio: str = "16:9",
                 background_color: str = "#020617") -> str:
        """Dispara geração e retorna video_id."""
        # HeyGen v2 generate
        payload = {
            "video_inputs": [{
                "character": {
                    "type": "avatar",
                    "avatar_id": self.avatar_id,
                    "avatar_style": "normal",
                    "talking_style": "expressive",
                    "expression": "happy",
                },
                "voice": {
                    "type": "text",
                    "input_text": script_text[:5500],  # HeyGen limita ~5500 chars
                    "voice_id": self.voice_id,
                },
                "background": {
                    "type": "color",
                    "value": background_color,
                },
            }],
            "dimension": (
                {"width": 1920, "height": 1080} if aspect_ratio == "16:9"
                else {"width": 1080, "height": 1920}
            ),
            "test": False,
        }
        r = self.s.post(f"{HEYGEN_API_BASE}/v2/video/generate", json=payload)
        r.raise_for_status()
        return r.json()["data"]["video_id"]

    def wait(self, video_id: str, timeout_s: int = 900) -> str:
        """Polling até completar; retorna URL do mp4."""
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            r = self.s.get(f"{HEYGEN_API_BASE}/v1/video_status.get",
                            params={"video_id": video_id})
            r.raise_for_status()
            data = r.json().get("data", {})
            st = data.get("status")
            if st == "completed":
                return data["video_url"]
            if st in ("failed", "error"):
                raise RuntimeError(f"HeyGen falhou: {data}")
            time.sleep(8)
        raise TimeoutError(f"HeyGen passou de {timeout_s}s pra {video_id}")

    def download(self, url: str, out_path: Path):
        r = self.s.get(url, stream=True)
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 64):
                f.write(chunk)


# ==============================================================================
# Pixar scene generator (Replicate / OpenAI)
# ==============================================================================
class PixarSceneGen:
    """Gera uma cena estilo Pixar a partir de um prompt textual,
    salvando como PNG. Backends suportados:

      - replicate  (padrão): usa stability-ai/sdxl com prompt Pixar
      - openai     : usa gpt-image-1 (DALL-E 3)
      - stub       : escreve um PNG colorido placeholder (pra testar pipeline)
    """
    def __init__(self, backend: str = "replicate"):
        self.backend = backend.lower()

    def render(self, prompt: str, out_png: Path,
                aspect: str = "16:9") -> Path:
        if out_png.exists():
            return out_png

        full = (
            PIXAR_STYLE_PREFIX if aspect == "16:9"
            else SHORT_PIXAR_STYLE_PREFIX
        ) + prompt

        if self.backend == "replicate":
            self._render_replicate(full, out_png, aspect)
        elif self.backend == "openai":
            self._render_openai(full, out_png, aspect)
        elif self.backend == "stub":
            self._render_stub(full, out_png, aspect)
        else:
            raise ValueError(f"Backend desconhecido: {self.backend}")
        return out_png

    # ------------- Replicate (FLUX schnell — rápido + barato) -------------
    def _render_replicate(self, prompt: str, out_png: Path, aspect: str):
        tok = os.environ.get("REPLICATE_API_TOKEN")
        if not tok:
            raise RuntimeError("REPLICATE_API_TOKEN ausente no .env")
        ar = "16:9" if aspect == "16:9" else "9:16"
        # Endpoint do modelo (não precisa especificar version SHA).
        # FLUX-schnell é US$0.003/imagem, ~6s, e renderiza estilo Pixar
        # com muita qualidade.
        # Retry-loop pra tratar rate-limit (429): Replicate limita
        # burst=1 enquanto saldo < $5 em contas novas, ~6 req/min.
        url = ("https://api.replicate.com/v1/models/black-forest-labs/"
               "flux-schnell/predictions")
        headers = {
            "Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
            "Prefer": "wait",  # bloqueia até 60s aguardando o resultado
        }
        body = {
            "input": {
                "prompt": prompt,
                "aspect_ratio": ar,
                "output_format": "png",
                "num_outputs": 1,
                "num_inference_steps": 4,
            },
        }
        r = None
        for attempt in range(8):
            r = requests.post(url, headers=headers, json=body, timeout=90)
            if r.status_code != 429:
                break
            try:
                wait_s = r.json().get("retry_after", 12)
            except Exception:
                wait_s = 12
            wait_s = max(int(wait_s) + 3, 8)  # margem de segurança
            print(f"    rate-limit Replicate; esperando {wait_s}s "
                  f"(tentativa {attempt+1}/8)")
            time.sleep(wait_s)
        if r is None or r.status_code >= 400:
            raise RuntimeError(
                f"Replicate {r.status_code if r else 'no-resp'}: "
                f"{r.text[:400] if r else ''}")
        pred = r.json()
        # Com 'Prefer: wait' o output costuma vir direto; caso contrário, polling
        status = pred.get("status")
        if status == "succeeded":
            out = pred.get("output")
            img_url = out[0] if isinstance(out, list) else out
        elif status in ("failed", "canceled"):
            raise RuntimeError(f"Replicate falhou: {pred.get('error')}")
        else:
            get_url = pred["urls"]["get"]
            img_url = None
            for _ in range(60):
                time.sleep(2)
                s = requests.get(get_url,
                                  headers={"Authorization": f"Bearer {tok}"}).json()
                if s.get("status") == "succeeded":
                    out = s.get("output")
                    img_url = out[0] if isinstance(out, list) else out
                    break
                if s.get("status") in ("failed", "canceled"):
                    raise RuntimeError(f"Replicate falhou: {s.get('error')}")
            if not img_url:
                raise TimeoutError("Replicate demorou demais")

        img = requests.get(img_url, timeout=60).content
        out_png.write_bytes(img)

    # ------------- OpenAI gpt-image-1 -------------
    def _render_openai(self, prompt: str, out_png: Path, aspect: str):
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY ausente no .env")
        size = "1792x1024" if aspect == "16:9" else "1024x1792"
        r = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "gpt-image-1", "prompt": prompt,
                  "size": size, "n": 1, "response_format": "b64_json"},
            timeout=120,
        )
        r.raise_for_status()
        import base64
        out_png.write_bytes(
            base64.b64decode(r.json()["data"][0]["b64_json"]))

    # ------------- Stub (placeholder) -------------
    def _render_stub(self, prompt: str, out_png: Path, aspect: str):
        # Gera um PNG simples com ffmpeg pra testar pipeline sem custo
        w, h = (1920, 1080) if aspect == "16:9" else (1080, 1920)
        subprocess.run(
            ["ffmpeg", "-f", "lavfi", "-i",
             f"color=c=0xF97316:s={w}x{h}:d=1",
             "-frames:v", "1", "-y", str(out_png)],
            check=True, capture_output=True)


# ==============================================================================
# Compositor: junta Mateo (HeyGen MP4) + cenas Pixar (PNGs) com ffmpeg
# ==============================================================================
def compose_video(mateo_mp4, pixar_pngs, out_mp4, aspect="16:9",
                   bgm_path=None, comandos=None):
    """Mateo full screen. Se houver comandos, overlay caixa terminal
    (fundo dark #020617, texto verde Courier #10B981) no rodape a cada
    1/(N+1) da duracao do video, por 5s."""
    import os as _os
    assert_ffmpeg()
    comandos = comandos or []

    if not comandos:
        subprocess.run(
            ["ffmpeg", "-i", str(mateo_mp4),
             "-c", "copy",
             "-movflags", "+faststart",
             "-y", str(out_mp4)],
            check=True,
        )
        return

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(mateo_mp4)],
        capture_output=True, text=True, check=True,
    )
    dur = float(probe.stdout.strip())

    font = _os.environ.get("FONT_PATH",
                            "C\\:/Windows/Fonts/consola.ttf")
    cmd_dur = 5.0
    n = len(comandos)
    filters = []
    for i, raw in enumerate(comandos):
        cmd = raw.strip().splitlines()[0][:90]
        safe = (cmd
                .replace("\\", "\\\\")
                .replace(":", "\\:")
                .replace("'", "\\'")
                .replace(",", "\\,")
                .replace("=", "\\=")
                .replace("%", "\\%"))
        start = max(1.0, (i + 1) * dur / (n + 1) - cmd_dur / 2)
        end = min(dur - 1.0, start + cmd_dur)
        if end <= start:
            continue
        filters.append(
            f"drawbox=x=40:y=H*0.62:w=W-80:h=H*0.25:"
            f"color=#020617@0.92:t=fill:"
            f"enable='between(t,{start:.2f},{end:.2f})'"
        )
        filters.append(
            f"drawtext=fontfile='{font}':text='$ {safe}':"
            f"fontcolor=#10B981:fontsize=H*0.030:"
            f"x=80:y=H*0.68:"
            f"enable='between(t,{start:.2f},{end:.2f})'"
        )

    if not filters:
        subprocess.run(
            ["ffmpeg", "-i", str(mateo_mp4),
             "-c", "copy", "-movflags", "+faststart",
             "-y", str(out_mp4)],
            check=True,
        )
        return

    vf = ",".join(filters)
    subprocess.run(
        ["ffmpeg", "-i", str(mateo_mp4),
         "-vf", vf,
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
         "-c:a", "copy",
         "-movflags", "+faststart",
         "-y", str(out_mp4)],
        check=True,
    )

def load_env():
    """Lê .env do diretório automacao."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


def render_one(md_path, aspect, out_mp4, pixar_only=False, backend="replicate"):
    """Simplificado: chama HeyGen com Mateo (Pixar 3D) e copia o MP4
    com overlay de comandos terminal nos pontos certos."""
    import re as _re
    print(f"=== {md_path.name} -> {out_mp4.name} ===")
    segs = parse_roteiro(md_path)
    raw_md = md_path.read_text(encoding="utf-8")
    comandos = _re.findall(
        r"\[COMANDO:\s*([^\|\]]+?)\s*(?:\|[^\]]*?)?\s*\]", raw_md
    )
    print(f"  segments: {len(segs)} | comandos: {len(comandos)}")

    full_speech = " ".join(s.speech for s in segs if s.speech.strip())
    print(f"  speech: {len(full_speech)} chars")

    hg = HeyGenMateo(
        api_key=os.environ["HEYGEN_API_KEY"],
        avatar_id=os.environ["HEYGEN_AVATAR_ID_MATEO"],
        voice_id=os.environ["HEYGEN_VOICE_ID_MATEO"],
    )
    vid = hg.generate(full_speech, aspect_ratio=aspect)
    print(f"  heygen video_id: {vid}")
    url = hg.wait(vid)
    print(f"  heygen ready: {url[:80]}...")

    mateo_mp4 = out_mp4.with_suffix(".mateo.mp4")
    hg.download(url, mateo_mp4)

    compose_video(mateo_mp4, [], out_mp4, aspect=aspect, comandos=comandos)
    mateo_mp4.unlink(missing_ok=True)
    print(f"  OK: {out_mp4} ({out_mp4.stat().st_size / 1024 / 1024:.1f} MB)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=["aula", "short"])
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--day", type=int)
    g.add_argument("--all", action="store_true")
    p.add_argument("--pixar-only", action="store_true")
    p.add_argument("--backend", default=os.environ.get("PIXAR_BACKEND", "replicate"),
                    choices=["replicate", "openai", "stub"])
    p.add_argument("--regenerate-pixar", action="store_true",
                    help="apaga PNGs cacheadas do dia antes de rodar")
    args = p.parse_args()

    load_env()
    aspect = "16:9" if args.kind == "aula" else "9:16"
    src_dir = AULAS_DIR if args.kind == "aula" else SHORTS_DIR

    days = list(range(1, 31)) if args.all else [args.day]
    for d in days:
        matches = sorted(src_dir.glob(f"{args.kind}-{d:02d}-*.md"))
        if not matches:
            print(f"sem roteiro pra dia {d}")
            continue
        md = matches[0]
        slug = md.stem.split("-", 2)[2]
        out_mp4 = VIDEOS_OUT / f"{args.kind}-{d:02d}-{slug}.mp4"
        if args.regenerate_pixar:
            for png in PIXAR_CACHE.glob(f"{md.stem}_*.png"):
                png.unlink()
        if out_mp4.exists():
            print(f"dia {d}: ja existe, pulando")
            continue
        try:
            render_one(md, aspect, out_mp4, pixar_only=False, backend=args.backend)
        except Exception as e:
            print(f"dia {d} falhou: {e}")
            continue


if __name__ == "__main__":
    main()
