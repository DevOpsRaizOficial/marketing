# SETUP_CHECKLIST — Trilha DEVOPSRAIZ (passos 1-6)

Roteiro objetivo do que precisa ser feito para colocar todos os passos no ar. Cada item está marcado como:

- **[VOCÊ]** = só você consegue fazer (cadastro, login, dinheiro envolvido, credenciais)
- **[CLAUDE]** = peça ao Claude Code (ou roda direto no terminal da pasta) — comandos automatizáveis

---

## 1. Distribuir o ebook gratuito (passo 1) — 15 min

**[VOCÊ]** Subir o PDF para um host público que aguente milhares de downloads:

- Opção A: **Google Drive** → tornar público → encurtar com bit.ly  *(rápido)*
- Opção B: **GitHub Releases** no repo `marketing` → upload do PDF → copiar link  *(estável, grátis)*
- Opção C: **Cloudflare R2** ou **AWS S3** → bucket público + URL custom

Arquivo: `marketing/lead-magnets/ebook-gratuito-python-zero-deploy.pdf`

**[VOCÊ]** Atualizar o link do ebook nos lugares:

- `linktr.ee` ou bio do `@devopsraiz_oficial`
- ManyChat keyword `PYTHON` (template em `lead-magnets/MANYCHAT_K8S_SETUP.md`)
- Página de vendas Hotmart (na descrição como "bônus de boas-vindas")

---

## 2. Cadastros e credenciais (passos 5-6) — 1 hora

### 2.1 HeyGen — vídeo com avatar Mateo

**[VOCÊ]** Necessário plano **Team ou Enterprise** (Creator não tem API):

1. Criar conta em https://app.heygen.com
2. Criar um avatar com o nome **Mateo** (Photo Avatar ou Instant Avatar)
3. Criar voice clone PT-BR (você fala 1-2 minutos)
4. Pegar a API key em https://app.heygen.com/settings?nav=API
5. **[CLAUDE]** Descobrir os IDs (com a API key no .env):
   ```bash
   cd marketing/automacao
   python3 heygen_client.py avatars   # acha avatar_id do Mateo
   python3 heygen_client.py voices    # acha voice_id do clone
   ```

### 2.2 Replicate — cenas Pixar (US$ 0,003 por imagem)

**[VOCÊ]**

1. Criar conta em https://replicate.com (login com GitHub)
2. Adicionar US$ 10 de crédito (dá pra mais de 3.000 cenas — sobra)
3. Copiar o token em https://replicate.com/account/api-tokens

> **Alternativa sem custo pra testar pipeline**: deixa `PIXAR_BACKEND=stub` no .env — gera PNGs laranja placeholder, útil para validar o fluxo antes de gastar.

### 2.3 YouTube Data API v3

**[VOCÊ]** Setup one-time (~20 minutos no console):

1. Entra em https://console.cloud.google.com e cria um projeto novo (ex: `devopsraiz-yt`)
2. Em **APIs & Services → Library**: habilitar **YouTube Data API v3**
3. Em **APIs & Services → OAuth consent screen**:
   - User Type: External
   - App name: `devopsraiz-publisher`
   - Adiciona seu email como Test user (sem isso, refresh_token expira em 7 dias)
4. Em **APIs & Services → Credentials**:
   - Create credentials → OAuth Client ID → Desktop App
   - Download JSON → salva como `marketing/automacao/credentials.json`

**[CLAUDE]** Autorizar uma vez no browser e pegar o refresh_token:

```bash
cd marketing/automacao
pip install google-auth-oauthlib
python3 get_youtube_token.py
# Abre browser, você autoriza com a conta do canal @DevOpsRaiz
# Output mostra YOUTUBE_CLIENT_ID, _SECRET, _REFRESH_TOKEN — copia pro .env
```

**[VOCÊ]** Criar 2 playlists vazias em https://studio.youtube.com (Settings → Playlists):

- "30 dias DevOpsRaiz" → ID vai em `YOUTUBE_PLAYLIST_AULAS`
- "Shorts DevOpsRaiz" → ID vai em `YOUTUBE_PLAYLIST_SHORTS`

---

## 3. Preencher o .env local (passos 5-6) — 10 min

**[CLAUDE]** Criar o arquivo a partir do template:

```bash
cd marketing/automacao
cp .env.example .env
```

**[VOCÊ]** Editar `.env` preenchendo com tudo que coletou em (2). Variáveis novas a preencher:

```
HEYGEN_AVATAR_ID_MATEO=...        # da seção 2.1
HEYGEN_VOICE_ID_MATEO=...
REPLICATE_API_TOKEN=r8_...        # da seção 2.2
PIXAR_BACKEND=replicate           # ou stub pra testar
YOUTUBE_CLIENT_ID=...             # da seção 2.3
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...
YOUTUBE_CHANNEL_ID=UC...
YOUTUBE_PLAYLIST_AULAS=PL...
YOUTUBE_PLAYLIST_SHORTS=PL...
```

> O resto (`HEYGEN_API_KEY`, `IG_USER_ID`, `META_ACCESS_TOKEN`, etc) você já tem do passo de Instagram que existia.

---

## 4. Validar o pipeline localmente (passo 5) — 10 min

**[CLAUDE]** Rodar com backend `stub` (zero custo) pra validar fluxo:

```bash
cd marketing/automacao
# Instala deps Python
pip install -r requirements.txt
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2

# Garante que tem ffmpeg
sudo apt install -y ffmpeg   # Linux/WSL
# ou: brew install ffmpeg    # Mac
# ou: choco install ffmpeg   # Windows

# Gera só as PNGs Pixar de 1 short (sem HeyGen, sem custo)
python3 heygen_mateo_pipeline.py short --day 1 --pixar-only --backend stub

# Vê o resultado em marketing/videos_mp4/.pixar_cache/
ls -la ../videos_mp4/.pixar_cache/
```

Se isso rodar limpo, o parser e a composição estão OK. Agora pode trocar pra backend real:

```bash
# Gera short de verdade (HeyGen + Replicate)
python3 heygen_mateo_pipeline.py short --day 1 --backend replicate

# Aula completa (toma ~5 min, custa ~US$ 1 + US$ 0,03)
python3 heygen_mateo_pipeline.py aula --day 1 --backend replicate
```

---

## 5. Subir credenciais no GitHub Actions (passo 5) — 15 min

**[VOCÊ]** Em `Settings → Secrets and variables → Actions` do repo `marketing`:

**Secrets** (criar cada um):
- `HEYGEN_API_KEY`
- `HEYGEN_AVATAR_ID_MATEO`
- `HEYGEN_VOICE_ID_MATEO`
- `REPLICATE_API_TOKEN`
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

**Variables** (criar cada um):
- `PIXAR_BACKEND` = `replicate`
- `YOUTUBE_CHANNEL_ID` = `UC...`
- `YOUTUBE_PLAYLIST_AULAS` = `PL...`
- `YOUTUBE_PLAYLIST_SHORTS` = `PL...`

---

## 6. Disparar o pipeline (passo 5) — 1 min

### Manual (você decide quando publicar)

**[VOCÊ]** Em `Actions → Publicar aula + short do dia no YouTube → Run workflow`:
- `day`: escolha um dia 1-30
- `privacy`: `private` (recomendado nas primeiras vezes pra revisar antes)
- `kind`: `both` (aula + short)

### Automático (todo dia 9h BRT)

**[VOCÊ]** Editar uma única linha em `marketing/.github/workflows/publish-youtube-daily.yml`:

```yaml
env:
  DIA_BASE: "2026-05-12"   # ← troca pela data que você quer começar o dia 1
```

Comita. A partir dali, o workflow roda sozinho todo dia 9h BRT, calcula o dia atual e publica.

---

## 7. Publicar a aula bônus Azure DevOps + AKS (passo 6) — 30 min

**Opção A — Gravar manualmente** (recomendado pra primeira vez, mais polido):

**[VOCÊ]**
1. OBS Studio ou Loom gravando 1080p
2. Abrir os 5 arquivos do bundle no VS Code: `marketing/roteiros/bonus_azuredevops_aks/*.{yml,yaml,md}`
3. Seguir o roteiro `aula-bonus-azuredevops-aks.md` linha por linha
4. Quando o roteiro tiver `[PIXAR: ...]`, mostrar `arquitetura.png` ou `pipeline-flow.png` em tela cheia
5. Exportar MP4
6. Upload manual no YouTube Studio usando os metadados do bloco `## METADADOS YOUTUBE` do .md

**Opção B — Usar o pipeline HeyGen Mateo**:

**[CLAUDE]**
```bash
cd marketing/automacao

# Copia o roteiro pra pasta de aulas com número 99 (bônus)
cp ../roteiros/bonus_azuredevops_aks/aula-bonus-azuredevops-aks.md \
   ../roteiros/aulas/aula-99-azuredevops-aks.md

# Gera vídeo (HeyGen + Pixar real)
python3 heygen_mateo_pipeline.py aula --day 99 --backend replicate

# Publica como unlisted pra revisar antes
python3 youtube_publisher.py --kind aula --day 99 --privacy unlisted
```

---

## 8. Cole isso no Claude Code

Cole o bloco abaixo no Claude Code (CLI) dentro da pasta `marketing/`:

```
Tô no projeto DEVOPSRAIZ. Leia marketing/SETUP_CHECKLIST.md e me ajude a executar os passos marcados [CLAUDE] em ordem. Para cada passo:
  1. Confirma comigo se já fiz a parte [VOCÊ] anterior
  2. Roda o comando e me mostra o output
  3. Se der erro, propõe o fix
  4. Não passa pro próximo passo até o atual estar verde

Começa pelo passo 4 (validar pipeline com backend stub), depois 3 (preencher .env quando eu confirmar), depois 6 (rodar o pipeline pra dia 1 com privacy=private).
```

---

## Resumo executivo: ordem de execução

| # | O que                                       | Quem    | Tempo |
|---|----------------------------------------------|---------|-------|
| 1 | Subir PDF do ebook gratuito em host público  | VOCÊ    | 15min |
| 2 | Cadastrar HeyGen + criar avatar Mateo        | VOCÊ    | 30min |
| 3 | Cadastrar Replicate + adicionar US$10 crédito| VOCÊ    | 5min  |
| 4 | Setup OAuth Google YouTube                   | VOCÊ    | 20min |
| 5 | Rodar `get_youtube_token.py`                 | CLAUDE  | 2min  |
| 6 | Preencher `.env` local                       | VOCÊ    | 10min |
| 7 | Testar pipeline com `--backend stub`         | CLAUDE  | 5min  |
| 8 | Testar pipeline real com `--day 1`           | CLAUDE  | 10min |
| 9 | Subir secrets no GitHub Actions              | VOCÊ    | 15min |
|10 | Disparar workflow manual (1 dia)             | VOCÊ    | 1min  |
|11 | Ativar cron diário (editar DIA_BASE)         | VOCÊ    | 1min  |
|12 | Aula bônus AzureDevOps+AKS                   | VOCÊ    | 30min |

**Total: ~2h30 de setup, depois roda automático todo dia.**

---

## Custos mensais estimados

| Item                            | Custo/mês  |
|---------------------------------|------------|
| HeyGen plano Team               | ~US$ 40-90 |
| Replicate (~180 imagens/mês)    | ~US$ 0,60  |
| GitHub Actions (Free tier 2000min) | grátis  |
| YouTube uploads                 | grátis     |
| Hosting do ebook PDF (Releases) | grátis     |
| **Total mensal**                | **~US$ 45-90** |

> Se precisar economizar: `PIXAR_BACKEND=stub` zera o Replicate; HeyGen Creator plan (US$ 29) também funciona, mas API é só Team+.
