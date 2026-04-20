# Agendando no Meta Business Suite — passo-a-passo

O Meta Business Suite (business.facebook.com) tem um agendador nativo
chamado **Planner** que posta foto, carrossel, Reel e Story no Instagram
e Facebook ao mesmo tempo, **sem precisar de API, sem precisar de token**.

Você pode agendar até **75 dias de antecedência**. Perfeito pro nosso
calendário de 30 dias.

---

## O que você vai usar

1. **Meta Business Suite** no desktop → [business.facebook.com](https://business.facebook.com)
2. Pasta `marketing/posts_prontos/` → textos prontos de cada post (30 arquivos)
3. Pasta `marketing/criativos/` → 11 PNGs já prontos
4. Pasta `marketing/roteiros/` → roteiros HeyGen pra gravar os 4 Reels

---

## Passo 1 — Abrir o Planner

1. Entre em [business.facebook.com](https://business.facebook.com)
2. Confirme no topo esquerdo que a conta selecionada é **Devopsraiz**
3. Na sidebar esquerda, clique em **Planner** (ou "Planejador" se
   estiver em PT-BR). Ícone de calendário.

Se não aparecer "Planner", clique em **Conteúdo** primeiro — deve ter um
botão "Agendar publicação".

---

## Passo 2 — Criar o primeiro post (Dia 1)

1. No Planner, clique no botão **"Criar publicação"** (canto superior direito)
2. **Marca os canais** onde quer postar:
   - ☑ Instagram — conta @devopsraiz_oficial
   - ☑ Facebook — página DEVOPSRAIZ (opcional, mas recomendado)
3. **Tipo de publicação**: escolha conforme o formato do post:
   - Dia 1 = **Carrossel** (8 slides)
4. **Mídia**: clique em "Adicionar foto/vídeo" e selecione os 8 PNGs do
   carrossel. Para o Dia 1, a capa é `criativos/01-apresentacao-capa.png`
   — para os outros slides, você vai criar no Canva seguindo a sugestão
   visual do arquivo `posts_prontos/dia-01-carrossel.txt`.
5. **Legenda**: abra `posts_prontos/dia-01-carrossel.txt`, selecione tudo
   da seção "LEGENDA", copia (Ctrl+A → Ctrl+C) e cola no campo legenda
   do Business Suite.
6. **Agendamento**:
   - Clica em **"Agendar publicação"** (em vez de "Publicar agora")
   - Data: **21/04/2026** (amanhã)
   - Horário: **19:00** (conforme calendário)
7. Clica **Agendar**.

Pronto. Dia 1 está na agenda. Vai aparecer no Planner com ícone de relógio.

---

## Passo 3 — Repita pros outros 29 dias

É repetitivo, mas é eficiente. Você **pode fazer os 30 de uma vez em
~1h30**, ou 5 por dia durante 6 dias, como preferir.

### Regra geral por tipo de post

**Carrossel** (20 dos 30 posts):
- Precisa de múltiplas imagens (2 a 10)
- No calendário, o número aparece no formato "Carrossel (8 slides)"
- Para os que não têm PNG pronto em `criativos/`, use o Canva:
  - Template recomendado: [Canva Post Instagram 1080x1350](https://canva.com/create/instagram-posts/)
  - Copie a estética dos PNGs já prontos (fundo escuro, cor do ebook,
    hook gigante, footer com @handle)

**Reel** (5 dos 30 posts — dias 3, 9, 16, 21, 26):
- Precisa de um MP4 vertical 9:16
- Gere no HeyGen com o roteiro correspondente em `roteiros/`
- Salve o MP4 e faça upload direto no Business Suite

**Post único / Foto** (4 dos 30 posts — dias 6, 11, 18, 23, 28):
- Uma imagem só
- Use o PNG correspondente em `criativos/` (dia 18 tem), ou crie no Canva

**Story** (1 dos 30 — dia 12):
- Business Suite agenda Story também (Instagram Business)
- Use `criativos/10-story-cta-link-bio.png` como base

### Checklist pra cada post

- [ ] Tipo de publicação correto
- [ ] Mídia (foto/carrossel/vídeo) carregada
- [ ] Legenda colada (com CTA + hashtags)
- [ ] Canais marcados (Instagram obrigatório, Facebook opcional)
- [ ] Data e hora corretos (abra `01-RESUMO-30-DIAS.txt` pra conferir)
- [ ] Clica Agendar

---

## Passo 4 — Ver todos os agendamentos

Depois de agendar vários, volte na tela Planner → visão de **calendário**.
Você vai ver todos os 30 posts distribuídos nos dias corretos. Pode:

- Arrastar pra mudar de dia
- Clicar num post pra editar
- Deletar
- Duplicar (útil se quiser replicar estrutura)

---

## Passo 5 — Resposta a comentários

O Business Suite também centraliza DM e comentários do Instagram + Facebook
numa **Caixa de Entrada** única. **Responder em < 4h** é o fator #1 do
algoritmo no primeiro mês.

Ativa notificações no desktop em:
- Configurações → Notificações → Desktop → tudo ligado

Ou use o **Meta Business Suite app** no celular pra responder na rua.

---

## Dicas pra acelerar

### 1) Cria todos os carrosséis no Canva em batch

Em vez de fazer um carrossel por vez, separa **1h no sábado**:
- Cria 1 pasta no Canva "DEVOPSRAIZ - Carrosseis"
- Duplica um template bom (copia a estética do `03-aws-custos-queimando.png`)
- Gera os 15-20 carrosséis de uma vez
- Exporta tudo em PNG

### 2) Reels HeyGen em batch também

- 1h no domingo
- Grava os 5 Reels (roteiros estão em `roteiros/`)
- Exporta MP4
- Salva em `videos_mp4/`
- Aí na hora de agendar é só arrastar

### 3) Legendas já estão prontas

Tudo em `posts_prontos/` — 30 arquivos, um por dia. É literalmente Ctrl+C, Ctrl+V.

### 4) Primeiro link clicável

Agenda o **Dia 1** pra 19:00 de hoje (ou amanhã) mesmo antes de fazer
os outros. Começar gera momentum. Os outros dias você vai completando
durante a semana.

---

## Se o Business Suite estiver instável

Às vezes (raramente) o Planner não aceita agendamento. Alternativas:

1. **App Meta Business Suite no celular** — funciona idêntico
2. **Instagram app direto** → Perfil → menu ☰ → "Publicações agendadas" →
   Criar. Permite agendar direto pelo Insta.
3. **Creator Studio (legado)** — ainda funciona: [business.facebook.com/creatorstudio](https://business.facebook.com/creatorstudio)

---

## E a automação automática? (volta do API no futuro)

Quando você tiver paciência e ~1h de tempo livre, podemos retomar o SETUP.md
da API. O código Python já tá todo pronto:

- `automacao/instagram_publisher.py` — publica posts/carrossel
- `automacao/reels_publisher.py` — gera Reel via HeyGen API + publica
- `.github/workflows/publish-daily.yml` — agenda cron 3x por dia

Só precisamos destravar o token Meta (que foi onde paramos hoje).
O Instagram API evolui rápido — daqui a 3 meses o fluxo pode estar mais
simples. Não tem pressa de fazer AGORA.

---

## Prioridade pra essa semana

Foca em:
1. ✅ Agendar Dia 1 hoje mesmo no Business Suite (MAIS IMPORTANTE)
2. 📅 Agendar os dias 2-7 (primeira semana) até domingo
3. 🎨 Gerar os criativos faltantes do Canva (sábado)
4. 🎥 Gravar os 5 Reels no HeyGen (domingo)
5. 📅 Agendar os dias 8-30 aos poucos

Não precisa ter tudo pronto no dia 1. O importante é **começar**.

Uma vez que os posts estão no ar, volte em `CAMPANHAS_PAGAS.md` pra plano
de tráfego pago das semanas 2, 3, 4.
