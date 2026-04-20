# SETUP — Passo-a-passo (uma tarde de 1h30)

Tempo estimado: **1h30** de setup inicial. Depois disso, roda no automático
sem você tocar mais em nada — o GitHub Actions publica sozinho todo dia.

Quem faz cada coisa:
- 👤 **Você** (tudo marcado com `[VOCÊ]`)
- 🤖 **Robô** (GitHub Actions) — roda no automático depois do setup

---

## Pré-requisitos rápidos

- [ ] HeyGen plano **Team ou Enterprise** ativo (você confirmou ✓)
- [ ] Conta Instagram @devopsraiz_oficial pronta
- [ ] Acesso ao painel Hotmart (produto 7537240)
- [ ] Email do Facebook (qualquer um que você já tenha)
- [ ] Cartão de crédito (só pras campanhas pagas — opcional)

---

## PARTE 1 — Instagram Business + Facebook Page  `[VOCÊ]` 15 min

1. **Abra o Instagram no celular** → Perfil → Menu (☰) → Configurações e privacidade.
2. **Conta** → "Mudar para conta profissional" → Escolha **Criador de conteúdo**
   ou **Empresa**. Categoria: "Educação".
3. **Facebook** → [facebook.com/pages/create](https://facebook.com/pages/create) →
   Crie uma Página chamada "DEVOPSRAIZ" (categoria: Educação / Curso online).
4. De volta ao Instagram → Editar perfil → Contato → **Conectar Página do Facebook** →
   selecione a página que acabou de criar.

**Conferência:** no Instagram, em Editar perfil, deve aparecer "Página:
DEVOPSRAIZ".

---

## PARTE 2 — App na Meta for Developers  `[VOCÊ]` 20 min

1. Abra [developers.facebook.com](https://developers.facebook.com/) → **My Apps**
   → **Create App**.
2. Tipo: **Business**. Nome: `devopsraiz-publisher`. Email: o seu.
3. No painel do app, em **Add Product**, adicione:
   - **Instagram** (você vai ver duas opções — adicione "Instagram" clássico).
4. Navegue para **App settings → Basic** e anote:
   - `App ID` (número)
   - `App Secret` (clique em "Show")
5. Navegue para [Graph API Explorer](https://developers.facebook.com/tools/explorer/):
   - Selecione seu app no dropdown.
   - Em "Permissions", adicione:
     - `instagram_basic`
     - `instagram_content_publish`
     - `pages_show_list`
     - `pages_read_engagement`
   - Clique "Generate Access Token" → autorize.
   - Copie o token gerado (curto prazo, 1 hora).

6. **Troque pelo token long-lived** (60 dias). No terminal:
   ```bash
   curl "https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=SEU_APP_ID&client_secret=SEU_APP_SECRET&fb_exchange_token=SEU_TOKEN_CURTO"
   ```
   Copie o `access_token` da resposta. **Esse é o `META_ACCESS_TOKEN`**.

7. **Descubra seu `IG_USER_ID`**:
   ```bash
   curl "https://graph.facebook.com/v21.0/me/accounts?access_token=LONG_LIVED_TOKEN"
   # → pegue o ID da página
   curl "https://graph.facebook.com/v21.0/PAGE_ID?fields=instagram_business_account&access_token=LONG_LIVED_TOKEN"
   # → pegue o ID da conta Instagram Business
   ```

**Guarde os 3 valores:** `META_APP_ID`, `META_APP_SECRET`, `META_ACCESS_TOKEN`, `IG_USER_ID`.

---

## PARTE 3 — HeyGen API  `[VOCÊ]` 10 min

1. Logado no HeyGen (plano Team): [app.heygen.com/settings?nav=API](https://app.heygen.com/settings?nav=API).
2. Clique **Generate API Key** → copie o valor. **Esse é `HEYGEN_API_KEY`**.
3. Você precisa descobrir o `avatar_id` do seu avatar e o `voice_id` da sua
   voice clone. Vou fazer isso pra você com 2 comandos depois que o repo
   estiver rodando (Parte 5, passo 6).

---

## PARTE 4 — Repositório GitHub  `[VOCÊ]` 15 min

1. Crie conta grátis em [github.com](https://github.com) se ainda não tem.
2. Crie **dois** repositórios **privados**:
   - `devopsraiz-publisher` → o código e o calendário (esse aqui)
   - `devopsraiz-instagram-assets` → só pra hospedar os MP4s e PNGs (vazio)
3. **No seu computador**, abra o terminal e rode:
   ```bash
   cd /caminho/para/Ebooks-DevopsRaiz/marketing
   git init
   git remote add origin https://github.com/SEU_USUARIO/devopsraiz-publisher.git
   git add .
   git commit -m "Kit marketing DEVOPSRAIZ"
   git branch -M main
   git push -u origin main
   ```

4. **GitHub Personal Access Token** (pra automação fazer upload de MP4):
   - Vá em [github.com/settings/tokens/new](https://github.com/settings/tokens/new) →
     scope `repo` → Generate → copie o valor. Esse é `GH_ASSETS_TOKEN`.

---

## PARTE 5 — Configurar Secrets no GitHub  `[VOCÊ]` 10 min

1. No repo `devopsraiz-publisher` → **Settings → Secrets and variables → Actions → New repository secret**.
2. Adicione 1 por 1 (copie dos passos anteriores):

| Nome | Valor |
|---|---|
| `META_APP_ID` | App ID da Parte 2 |
| `META_APP_SECRET` | App Secret da Parte 2 |
| `META_ACCESS_TOKEN` | Token long-lived da Parte 2 |
| `IG_USER_ID` | ID Instagram Business da Parte 2 |
| `HEYGEN_API_KEY` | API Key da Parte 3 |
| `HEYGEN_AVATAR_ID` | (descoberto no passo 6 abaixo) |
| `HEYGEN_VOICE_ID` | (descoberto no passo 6 abaixo) |
| `GH_ASSETS_TOKEN` | Token da Parte 4, passo 4 |
| `GH_ASSETS_REPO` | `SEU_USUARIO/devopsraiz-instagram-assets` |
| `MEDIA_BASE_URL` | `https://github.com/SEU_USUARIO/devopsraiz-instagram-assets/releases/download/instagram-assets` |

3. **Descobrir avatar_id e voice_id do HeyGen** (roda 1 vez no seu PC):
   ```bash
   cd marketing/automacao
   cp .env.example .env
   # edite .env preenchendo HEYGEN_API_KEY apenas

   pip install -r requirements.txt
   python heygen_client.py avatars   # mostra todos os avatares
   python heygen_client.py voices    # mostra todas as vozes
   ```

   Copie o `avatar_id` do "Teste1" e o `voice_id` da voice clone, e volte ao
   GitHub pra adicionar `HEYGEN_AVATAR_ID` e `HEYGEN_VOICE_ID` como secrets.

---

## PARTE 6 — Subir o primeiro PNG/MP4 de teste  `[VOCÊ]` 10 min

O workflow só funciona se os PNGs estiverem hospedados publicamente.

Opção mais simples:

1. No repo `devopsraiz-instagram-assets`, crie um **Release** com tag
   `instagram-assets` (pode deixar o release vazio).
2. Upload manual: arraste todos os 11 PNGs de `marketing/criativos/` para o
   release como assets.
3. Os PNGs agora estão em:
   `https://github.com/SEU_USER/devopsraiz-instagram-assets/releases/download/instagram-assets/01-apresentacao-capa.png`

O script de Reels já faz upload automático de MP4 pra esse mesmo release
via token. Então você só precisa subir os PNGs uma vez; MP4s entram sozinhos.

---

## PARTE 7 — Teste seco  `[VOCÊ]` 5 min

No GitHub:

1. Aba **Actions** → workflow "Publicar post do dia" → **Run workflow**.
2. Marque:
   - Day: `1`
   - Dry run: ✅ marcado
3. Clique **Run workflow**.

Aguarde ~2 min. Se terminar verde, significa que tudo está configurado
corretamente (conectou na Meta, leu o calendário, montou a legenda).

Se deu vermelho, clique no job pra ver o erro — normalmente é token
errado ou secret faltando.

---

## PARTE 8 — Publicar o primeiro post de verdade  `[VOCÊ]` 5 min

Mesma tela, mas com:
   - Day: `1`
   - Dry run: ❌ desmarcado

Vai publicar o post/carrossel do Dia 1 agora. Vá no Instagram e veja.

---

## PARTE 9 — Ativar automação diária  ✓ (nada a fazer)

O cron já está ligado no workflow. Todo dia às 08h, 12h e 19h BRT o
GitHub Actions vai:

1. Ler o calendário e pegar o post do dia
2. Se for Reel → chamar HeyGen API → gerar vídeo → upload → publicar
3. Se for post de foto/carrossel → publicar direto com a PNG hospedada
4. Se for Story → te lembrar via log pra postar manualmente (Stories API
   tem limitações)

**Importante:** o cron do GitHub Actions **não é 100% pontual** — pode
atrasar 5-15 min. Pra publicação no exato horário, use o dispatch manual
ou um agendamento próprio no seu VPS/PC.

---

## PARTE 10 — Renovação do token Meta  ✓ (automático)

O token da Meta expira em 60 dias. Criei o workflow `refresh-token.yml`
que roda todo dia 1 do mês e gera um novo token. Você só precisa copiar
o valor do log e atualizar o secret `META_ACCESS_TOKEN` — 2 cliques.

(Infelizmente, o GitHub Actions não consegue atualizar secrets via API
do próprio workflow por questões de segurança. Por isso precisa do seu
toque humano mensal — 1 minuto de trabalho.)

---

## Resumo — quais senhas/tokens você vai manipular

| Local | O que guardar |
|--|--|
| GitHub Secrets (10 secrets) | Tudo criptografado, só o workflow enxerga |
| `.env` local no seu PC | **Nunca comite** — já está no `.gitignore` |
| Hotmart painel | Seu login normal, o pixel Meta vai ser configurado lá |
| Cartão Meta Ads | Só quando começar campanha paga (Parte 3 do `CAMPANHAS_PAGAS.md`) |

---

## Troubleshooting rápido

**Erro "Not a business account"**: Você pulou a Parte 1 ou a conta Instagram
não está conectada à Página Facebook.

**Erro "Invalid OAuth access token"**: Token da Meta expirou. Rode o workflow
`refresh-token.yml` manualmente e atualize o secret.

**Erro "Media container status is ERROR"**: O MP4 está num formato que a
Meta não aceita (codec errado, aspect diferente de 9:16, ou > 90s). O HeyGen
já gera no formato correto, mas se você produziu manualmente, use ffmpeg
pra re-codificar:
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset fast -c:a aac -b:a 128k -movflags +faststart output.mp4
```

**HeyGen "quota exceeded"**: Veja `python heygen_client.py quota` — cada
plano tem seu limite. Team geralmente tem 60+ min/mês.
