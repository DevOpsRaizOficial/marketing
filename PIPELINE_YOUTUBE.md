# Pipeline diário YouTube — DEVOPSRAIZ (passo 5)

Esse documento descreve a esteira completa que gera e publica diariamente, de forma automática, **1 aula de ~10 min + 1 short de 10 s** no canal [@DevOpsRaiz](https://www.youtube.com/@DevOpsRaiz) durante 30 dias, e também os posts equivalentes no Instagram.

## Visão geral

```
roteiros/aulas/aula-XX-*.md   ─┐
roteiros/shorts/short-XX-*.md  ├─►  heygen_mateo_pipeline.py   ─►  videos_mp4/*.mp4   ─►  youtube_publisher.py   ─►  YouTube canal
posts_prontos/v2_*/*.md        ─┘    (Mateo + cenas Pixar)            (MP4 com Pixar)        (OAuth API v3)
```

O scheduler é uma GitHub Action que roda diariamente às 9h BRT e calcula automaticamente qual é o "dia atual" da série (com base em `DIA_BASE` no workflow).

## 1) Roteiros gerados

`marketing/roteiros/generate_30_aulas.py` produz 90 arquivos:

- `roteiros/aulas/aula-XX-slug.md` — long-form 10 min, com markers `[PIXAR: …]` em cada segmento
- `roteiros/shorts/short-XX-slug.md` — hooks de 10s alinhados à aula do dia
- `posts_prontos/v2_python_zero_deploy/ig-XX-slug.md` — legenda Instagram + ideias de Stories

Os tópicos seguem essa progressão:

- **Dias 1–7**: mapeiam os 7 dias do ebook gratuito (cliente/servidor → Linux/Git → Python → FastAPI → Postgres → Docker → Deploy Render)
- **Dias 8–15**: trilha intermediária (Kubernetes, Terraform, AWS, CI/CD, observabilidade, OWASP, RAG, SaaS multi-tenant)
- **Dias 16–24**: trilha avançada (Docker otimizado, Helm/Kustomize, EKS, AKS, Cloud Run, FinOps, Prometheus, SLO/SLI, Zero Trust)
- **Dias 25–30**: especialidades + carreira (LGPD, Agents LLM, Kafka, Vault, júnior→sênior, fechamento)

Para regenerar:

```bash
cd marketing/roteiros && python3 generate_30_aulas.py
```

## 2) Markers `[PIXAR: …]` e o estilo

Cada aula tem ~6 markers que descrevem uma cena 3D estilo Pixar. Exemplos reais já gerados:

- "carteiro Pixar 3D entregando pacote 'GET /tarefas' pra prédio chamado SERVIDOR"
- "baleia azul Docker estilo Pixar empilhando contêineres coloridos no porto"
- "elefante azul Postgres guardando arquivinhos numa estante mágica"
- "maestro Pixar regendo uma orquestra de contêineres dançantes"

O `heygen_mateo_pipeline.py` adiciona o prefixo de estilo:

```
Pixar-style 3D animation, cinematic lighting, vibrant saturated colors,
soft global illumination, shallow depth of field, character design
reminiscent of Pixar/Disney studios 2025, no on-screen text,
16:9 cinematic composition, ultra-detailed, hero shot. Subject: ...
```

Depois envia pra um backend de geração de imagem (Replicate SDXL por padrão, ~US$0,003/imagem; ou DALL-E 3 da OpenAI ~US$0,04). Para validar pipeline sem custo: `PIXAR_BACKEND=stub` gera PNGs placeholder laranja.

## 3) Mateo no HeyGen

O Mateo é um avatar HeyGen com voice clone PT-BR. Descobrir os IDs:

```bash
cd marketing/automacao
python3 heygen_client.py avatars   # acha o avatar_id do Mateo
python3 heygen_client.py voices    # acha o voice_id do clone
```

Adicione ao `.env`:

```
HEYGEN_AVATAR_ID_MATEO=...
HEYGEN_VOICE_ID_MATEO=...
```

O `heygen_mateo_pipeline.py` envia a fala completa (extraída automaticamente dos roteiros — tudo MENOS as linhas `[PIXAR: …]` e comentários em parênteses) para a API `/v2/video/generate`. Depois faz polling até completar e baixa o MP4 do Mateo falando.

## 4) Composição final (ffmpeg)

O pipeline junta tudo:

- Cenas Pixar (PNGs) com Ken Burns (zoom in suave) → clipes de 5s
- Vídeo do Mateo (HeyGen) full
- Concat na ordem: pixar_0 → Mateo → pixar_1 → Mateo …
- Logo DEVOPSRAIZ canto superior esquerdo (a fazer — ver TODO em `compose_video`)
- BGM em `-25 dB` se `BGM_PATH` setado

Saídas em `marketing/videos_mp4/`:

- `aula-01-internet-cliente-servidor.mp4` (1920×1080)
- `short-01-internet-cliente-servidor.mp4` (1080×1920)

## 5) Publicação no YouTube

`youtube_publisher.py` faz upload resumível via Google API v3:

```bash
# Setup one-time (autoriza no browser, gera refresh_token)
python3 get_youtube_token.py

# Publicar como private (recomendado pra revisão)
python3 youtube_publisher.py --kind aula --day 1 --privacy private

# Publicar todos os 30 de uma vez
python3 youtube_publisher.py --kind aula --all --privacy private
python3 youtube_publisher.py --kind short --all --privacy private
```

Features:

- Lê título/descrição/tags do bloco `## METADADOS YOUTUBE` no .md
- Sobe thumb customizada se existir `videos_mp4/aula-XX-*.thumb.png`
- Adiciona à playlist (vars `YOUTUBE_PLAYLIST_AULAS` / `YOUTUBE_PLAYLIST_SHORTS`)
- Log idempotente em `automacao/publish_log_youtube.jsonl` (evita publicar 2x)
- Shorts ganham `#Shorts` no início da descrição automaticamente

## 6) Schedule diário (GitHub Actions)

`.github/workflows/publish-youtube-daily.yml` roda às 9h BRT todo dia:

1. Calcula o dia atual da série (hoje − `DIA_BASE`)
2. Gera aula + short via `heygen_mateo_pipeline.py` (se ainda não existirem)
3. Comita os MP4s no repo (pra alimentar Instagram também)
4. Publica os 2 vídeos no YouTube como `private` (revisão manual antes de ir público)
5. Comita o log

### Secrets necessários no repo

Em `Settings → Secrets and variables → Actions`:

| Tipo    | Nome                       | Onde pegar                                              |
| ------- | -------------------------- | ------------------------------------------------------- |
| secret  | `HEYGEN_API_KEY`           | https://app.heygen.com/settings?nav=API                 |
| secret  | `HEYGEN_AVATAR_ID_MATEO`   | output de `heygen_client.py avatars`                    |
| secret  | `HEYGEN_VOICE_ID_MATEO`    | output de `heygen_client.py voices`                     |
| secret  | `REPLICATE_API_TOKEN`      | https://replicate.com/account/api-tokens                |
| secret  | `OPENAI_API_KEY`           | opcional (só se `PIXAR_BACKEND=openai`)                 |
| secret  | `YOUTUBE_CLIENT_ID`        | Google Cloud Console → OAuth 2.0 Client                 |
| secret  | `YOUTUBE_CLIENT_SECRET`    | idem                                                    |
| secret  | `YOUTUBE_REFRESH_TOKEN`    | `python get_youtube_token.py`                           |
| var     | `PIXAR_BACKEND`            | `replicate` (padrão) / `openai` / `stub`                |
| var     | `YOUTUBE_CHANNEL_ID`       | studio.youtube.com → Settings → Channel → Advanced      |
| var     | `YOUTUBE_PLAYLIST_AULAS`   | crie playlist "30 dias DevOpsRaiz" e copie ID           |
| var     | `YOUTUBE_PLAYLIST_SHORTS`  | crie playlist "Shorts DevOpsRaiz" e copie ID            |

## 7) Custos esperados (estimativa)

| Item                            | Por aula | Por 30 dias       |
| ------------------------------- | -------- | ----------------- |
| HeyGen (~10 min de vídeo)       | ~US$ 1   | ~US$ 30 (plano Team) |
| Replicate SDXL (6 imagens)      | US$ 0,02 | US$ 0,60          |
| YouTube upload                  | grátis   | grátis            |
| GitHub Actions (90 min/dia)     | grátis*  | grátis (até 2000 min/mês plano Free) |

\* GitHub Actions free tier dá 2000 min/mês — confortável pros 30 dias.

## 8) Fluxo de revisão

1. Vídeos sobem como **private** pra ninguém ver antes da curadoria
2. Você abre o YouTube Studio, revisa thumb/descrição/conteúdo
3. Aprova manualmente clicando em "Public" (ou agenda `publishAt`)
4. O Instagram já saiu automaticamente pelo `publish-daily.yml` existente

## 9) Próximos passos sugeridos

- **B-roll real** em vez de PNGs estáticos: trocar Replicate por Runway Gen-3 ou Pika 1.5 para clipes de 5s nativos
- **Thumbnails geradas**: script que pega 1 frame da cena Pixar principal + overlay título grande em Helvetica laranja
- **Cards/end-screen**: API do YouTube permite, mas exige fluxo separado pós-publicação
- **Analytics**: cron semanal que puxa views/CTR/retention e gera relatório no Notion ou Slack

---

Documento gerado automaticamente pelo passo 5 da Trilha DevOpsRaiz.
Para o vídeo único Docker → Azure DevOps → AKS, ver o passo 6.
