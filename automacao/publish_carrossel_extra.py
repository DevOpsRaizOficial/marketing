#!/usr/bin/env python3
"""
Publisher genérico de carrossel EXTRA (fora do calendário XLSX).

Uso:
    python publish_carrossel_extra.py --slug quinta01 [--dry-run]

Slug determina:
- Slides usados: criativos/extra-{slug}-slide-NN.png
- Legenda: dicionário CAPTIONS abaixo

Cada slug é uma série diferente. Atualmente cobertos:
- quinta01 — IA + ManyChat (Sugestão 1: Automatize sua rotina)
- quinta02 — IA + ManyChat (Sugestão 2: Do caos ao automático)
- quinta03 — IA + ManyChat (Sugestão 3: Playbook de automação)
- teaser-k8s — lead magnet PDF K8s (já tem script dedicado)
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from instagram_publisher import IGClient, load_env

BRT = timezone(timedelta(hours=-3))

# Cronograma fixo por data → slug do carrossel a publicar
# Quando a data bate, o cron dispara automaticamente o slug correspondente
QUINTAS_SCHEDULE = {
    date(2026, 5, 7): "quinta01",   # Sugestão 1 - Automatize sua rotina
    date(2026, 5, 14): "quinta02",  # Sugestão 2 - Do caos ao automático
    date(2026, 5, 21): "quinta03",  # Sugestão 3 - Playbook automação
}


def slug_for_today() -> str | None:
    """Retorna o slug agendado pra hoje em BRT, ou None se nada agendado."""
    today_brt = datetime.now(BRT).date()
    return QUINTAS_SCHEDULE.get(today_brt)


def already_published_today(slug: str, log_path: Path) -> bool:
    """Evita publicar o mesmo slug 2x no mesmo dia."""
    if not log_path.exists():
        return False
    today_str = datetime.now(BRT).strftime("%Y-%m-%d")
    target = f"extra-{slug}"
    for line in log_path.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except Exception:
            continue
        if str(entry.get("dia")) != target:
            continue
        pub_at = entry.get("publicado_em", "")
        if pub_at.startswith(today_str):
            return True
    return False

# =============================================================================
# Mapa slug → (qtd slides, legenda completa)
# =============================================================================
HASHTAGS_IA = "#ia #claude #chatgpt #manychat #instagram #automacao #marketingdigital #infoproduto #criadordeconteudo #marketing #devops #devopsraiz #leadmagnet #produtividade"

OFERTA = """━━━━━━━━━━━━━━━━━
🎁 PDF "Prompts de Automação IA" — 15 prompts prontos
💰 R$ 49,90 → 20% OFF com cupom AUTOMACAO20 (R$ 39,92)
🔥 SEGUIDORES: 90% OFF com cupom SIGO (R$ 4,98)
📱 Suporte WhatsApp pra Trilha completa: (11) 96482-3126
━━━━━━━━━━━━━━━━━

💬 Comenta EU QUERO → recebe link com 20% off direto no DM
💬 Comenta SIGO (e me segue) → recebe link com 90% off no DM"""

CAPTIONS = {
    "quinta01": (3, """🤖 AUTOMATIZE SUA ROTINA com Claude + ChatGPT + ManyChat

3 ferramentas. 30 minutos. Uma máquina de leads no Instagram.

→ Claude organiza a estratégia
→ ChatGPT refina os textos
→ ManyChat executa o flow

No carrossel:
✅ Como subir o PDF no ManyChat
✅ Como configurar o flow de boas-vindas + captura de email
✅ Checklist de teste em 7 etapas

Esse é exatamente o pipeline que uso pra capturar leads automaticamente nos posts do @devopsraiz_oficial.

Quer o PDF completo com 15 prompts prontos (5 Claude + 5 ChatGPT + 5 ManyChat) pra montar SUA automação do zero?

""" + OFERTA + """

💾 Salva pra revisar quando for montar a sua.

""" + HASHTAGS_IA),

    "quinta02": (3, """⚡ DO CAOS AO AUTOMÁTICO em 3 etapas

Pensou. Promptou. Publicou. É o ciclo completo.

→ Claude organiza
→ ChatGPT refina
→ ManyChat executa

No carrossel mostro o setup REAL que tá rodando no @devopsraiz_oficial:
✅ Slide 1: trigger no comentário do post → resposta automática
✅ Slide 2: 4 cards do flow (Boas-vindas, Captura email, Link PDF, Follow gate)
✅ Slide 3: teste em 30 segundos pra validar tudo ponta a ponta

O segredo é simples: arquivo certo + mensagem certa + CTA certo.

Quer o PDF com 15 prompts prontos pra usar em Claude e ChatGPT pra montar SUA automação?

""" + OFERTA + """

📌 Salva pra não perder.

""" + HASHTAGS_IA),

    "quinta03": (3, """📚 PLAYBOOK DE AUTOMAÇÃO DIÁRIA

Use Claude + ChatGPT pra tirar tarefas do manual e colocar no automático.

Automatiza hoje. Escala amanhã.

No carrossel:
✅ Etapa 1: setup ManyChat (5 blocos, 30 min)
✅ Etapa 2: arquivo + estrutura do flow (BOAS-VINDAS → CAPTURA → LINK → FOLLOW GATE OFF)
✅ Etapa 3: validar e publicar (checklist de 7 testes)

Esse é o framework que sigo TODA semana pra criar nova automação. Funciona pra creator, infoproduto e rotina diária.

Quer o PDF "Prompts de Automação" com os comandos prontos que uso em Claude e ChatGPT?

""" + OFERTA + """

🔖 Salva esse carrossel — vai precisar quando for montar a sua.

""" + HASHTAGS_IA),
}


def _append_log(entry: dict):
    log_path = Path(__file__).parent / "publish_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Publica carrossel extra no @devopsraiz_oficial")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--slug", help="Slug do carrossel (quinta01, quinta02, quinta03)")
    g.add_argument("--auto", action="store_true",
                   help="Detecta automaticamente o slug pela data de hoje (BRT)")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem publicar")
    parser.add_argument("--force", action="store_true",
                        help="Ignora log de duplicatas (recovery manual)")
    args = parser.parse_args()

    if args.auto:
        slug = slug_for_today()
        if not slug:
            today = datetime.now(BRT).date()
            print(f"ℹ Sem carrossel extra agendado pra hoje ({today}). Saindo.")
            sys.exit(0)
        print(f"✓ Auto-detectado: hoje={datetime.now(BRT).date()} → slug='{slug}'")
    else:
        slug = args.slug

    if slug not in CAPTIONS:
        sys.exit(f"Slug '{slug}' não tem legenda definida. Slugs: {list(CAPTIONS.keys())}")

    # Anti-duplicação: se já foi publicado hoje, não republica
    log_path = Path(__file__).parent / "publish_log.jsonl"
    if not args.force and not args.dry_run and already_published_today(slug, log_path):
        print(f"⏭  Slug '{slug}' já foi publicado hoje. Pulando (use --force pra forçar).")
        sys.exit(0)

    total_slides, legenda = CAPTIONS[slug]
    args.slug = slug  # pra usar mais abaixo

    cfg = load_env(Path(__file__).parent / ".env")
    base = cfg["MEDIA_BASE_URL"].rstrip("/")
    urls = [f"{base}/extra-{args.slug}-slide-{n:02d}.png" for n in range(1, total_slides + 1)]

    print("=" * 60)
    print(f"CARROSSEL EXTRA — slug='{args.slug}' ({total_slides} slides)")
    print("=" * 60)
    for i, u in enumerate(urls, 1):
        print(f"  Slide {i}: {u}")
    print(f"\nLegenda ({len(legenda)} chars):")
    print(legenda[:280] + "...\n")

    if args.dry_run:
        print("[DRY-RUN] Não chamando API.")
        return

    ig = IGClient(cfg["IG_USER_ID"], cfg["META_ACCESS_TOKEN"])
    print("→ Criando containers dos slides + carousel container...")
    container_id = ig.create_carousel_container(urls, legenda)
    print(f"  Carousel container: {container_id}")

    print("→ Aguardando processamento (~1-2 min)...")
    ig.wait_container_ready(container_id)

    print("→ Publicando...")
    media_id = ig.publish(container_id)
    print(f"\n✓ CARROSSEL PUBLICADO! Media ID: {media_id}")

    _append_log({
        "type": "carousel",
        "dia": f"extra-{args.slug}",
        "media_id": media_id,
        "slides": len(urls),
        "publicado_em": datetime.utcnow().isoformat(),
    })


if __name__ == "__main__":
    main()
