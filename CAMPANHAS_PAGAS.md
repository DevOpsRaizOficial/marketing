# Campanhas de Tráfego Pago — Meta Ads  (R$ 300/mês)

Aqui você faz sozinho porque envolve o seu cartão. Eu te guio clique a
clique e você só aperta os botões.

**Princípios-chave:**

1. Não impulsione nada na Semana 1 — deixe o algoritmo "aprender".
2. Toda campanha precisa do **Pixel da Meta** instalado na Hotmart, senão
   você queima o retargeting da Semana 4.
3. Públicos-frios precisam de **criativo que pare o scroll** (hook nos 3
   primeiros segundos) — os Reels gerados pela automação servem pra isso.
4. **Não misture compra e tráfego** na mesma campanha — separe.

---

## PARTE 1 — Pixel da Meta na Hotmart (antes de qualquer campanha)

Faça isso **antes de rodar o primeiro real em ads**. Sem isso, o
retargeting da Semana 4 não funciona.

1. Acesse [business.facebook.com/events_manager2](https://business.facebook.com/events_manager2)
   → **Conectar fontes de dados** → **Web** → **Pixel da Meta**.
2. Dê um nome: `devopsraiz-pixel`. Copie o **Pixel ID** (número).
3. Vá no [painel Hotmart](https://app.hotmart.com) → **Meu Produto 7537240** →
   **Analytics & Dados** → **Pixel e Rastreamento**.
4. Cole o Pixel ID em **Meta Pixel**. Ative os eventos:
   - `ViewContent` → quando alguém vê a página
   - `InitiateCheckout` → quando clica "comprar"
   - `Purchase` → compra concluída
5. Salve. Aguarde 10-20 min.
6. No Events Manager da Meta, use **Test Events** e entre no link do produto
   pra ver se dispara os eventos.

---

## PARTE 2 — Cartão e conta de anúncios

1. Em [business.facebook.com/settings](https://business.facebook.com/settings)
   → **Contas de anúncios** → Criar conta de anúncios.
   - Nome: `DEVOPSRAIZ`
   - Fuso: São Paulo
   - Moeda: BRL
2. Conecte a Página do Facebook (a DEVOPSRAIZ que você criou no SETUP).
3. **Pagamento**: adicione cartão de crédito. Meta cobra conforme você
   gasta; não é débito automático antecipado.
4. **Limite da conta**: defina limite mensal de R$ 500 (margem de segurança).
   Settings → Billing → Spending limit.

---

## SEMANA 1 (R$ 0) — Só orgânico

**Nada de ads.** Publique os 7 posts do calendário. O papel dessa semana é
achar o "post-que-mais-engaja" naturalmente. Esse vai ser seu criativo
vencedor na Semana 2.

**O que fazer:**
- Responda 100% dos comentários em até 4 horas (sinal mais forte pro algoritmo).
- Entre no DM de quem salvou seu post 2+ vezes (Instagram mostra em "Insights").
- Compartilhe seus posts em 2-3 grupos de Telegram/Discord de DevOps BR.
- Faça comentários úteis em 20+ posts de outros criadores DevOps/Cloud BR
  (Lucas Montano, Código Fonte TV, Rocketseat, etc). Não spam — comentário
  técnico. O perfil aparece pros seguidores deles.

**Métrica que importa:** qual dos 7 posts teve mais **salvamentos**?
(Insights → aba do post → Saves)

---

## SEMANA 2 (R$ 50) — Impulsionar o post vencedor

Orçamento diário: **R$ 7 por dia, 7 dias**.

**Passo a passo:**

1. Abra o post mais salvo da Semana 1 no próprio app Instagram.
2. Toque em **Impulsionar post** (botão abaixo do post).
3. **Objetivo**: "Mais interações do seu post" (NÃO escolha "mais visitas ao
   perfil" ou "mais mensagens" — quer reach com engajamento).
4. **Público**:
   - Escolha **Criar novo**.
   - Idade: 22 a 40.
   - Localização: Brasil (todas as regiões).
   - Interesses (adicione TODOS): AWS, Microsoft Azure, Kubernetes, Docker,
     DevOps, Programação, Desenvolvimento de software, Linux, Engenharia
     de software, Cloud computing.
   - **Retire** interesses muito amplos (ex: "Tecnologia") — diluem.
5. **Orçamento e duração**:
   - R$ 7 por dia, **duração 7 dias**.
6. **Criativo**: use o próprio post que já está publicado.
7. **Revisar e publicar**.
8. No dia seguinte, confira em Insights:
   - Se CPM (custo por mil impressões) > R$ 25, **pause e troque público**.
   - Se CPM < R$ 15 e saves crescendo, **deixe rodar os 7 dias**.

**Meta realista Semana 2:** +150 a +300 seguidores, +20 saves no post.

---

## SEMANA 3 (R$ 100) — Campanha de Tráfego pro Hotmart

Agora sim, pela primeira vez, você manda gente direto pro checkout.

**Onde:** [business.facebook.com/adsmanager](https://business.facebook.com/adsmanager)
→ **Criar campanha**.

**Configuração da campanha:**

- **Objetivo da campanha**: "Vendas" (ou "Tráfego" se Vendas estiver
  bloqueado pela falta de histórico de pixel).
- **Tipo de Campanha**: **Advantage+ Shopping Campaigns** (deixa a Meta
  otimizar sozinha — ideal pra quem tá começando).
- **Orçamento da campanha**: R$ 14 por dia (7 dias = ~R$ 100).

**Configuração do conjunto de anúncios:**

- **Otimização**: "Conversões" → evento `Purchase` (do pixel).
  - Se você ainda não teve 20 compras pra Meta aprender, use `InitiateCheckout`
    por enquanto.
- **Públicos**:
  - Primário (50% do budget): **Advantage+ automatic audience** (deixa a
    Meta decidir).
  - Secundário (50% do budget): **Lookalike 1%** baseado em quem SALVOU
    3+ posts seus no Instagram (crie em Públicos → Lookalike → fonte:
    "Engajadores do Instagram últimos 60 dias").
- **Posicionamentos**: "Posicionamentos automáticos" (deixe a Meta escolher
  Feed, Reels, Stories, Explore).

**Criativo do anúncio:**

- Use o **Reel Dia 1 de apresentação** (gerado pela automação HeyGen) OU
  o criativo `09-fechamento-trilha-completa.png`.
- **Copy** (texto do anúncio) — copie da legenda do Dia 30 do calendário.
- **Call to action**: "Saiba mais".
- **URL de destino**: link direto do produto na Hotmart
  (`pay.hotmart.com/...`).

**Métrica que importa:**
- **ROAS** (Retorno sobre investimento em ads) = receita gerada ÷ gasto.
  ROAS > 2.0 é saudável pra infoproduto.
- **CPM** < R$ 30.
- **CTR** > 1.5%.

Se em 3 dias o ROAS tiver < 1.0, **pause** e reveja o público ou o
criativo.

---

## SEMANA 4 (R$ 150) — Retargeting (a parte mais lucrativa)

Agora o pixel já tem gente "marcada" (visitou a página Hotmart ou iniciou
checkout). Essa audiência converte 5-10x mais que frio.

**Passo a passo:**

1. **Criar público custom** em [business.facebook.com/audiences](https://business.facebook.com/audiences):
   - Público 1: **"Visitou checkout mas não comprou"**
     - Fonte: Pixel → `InitiateCheckout` nos últimos 30 dias
     - Excluir: `Purchase` nos últimos 30 dias
   - Público 2: **"Visitou landing page"**
     - Fonte: Pixel → `ViewContent` nos últimos 14 dias
   - Público 3: **"Engajadores Instagram 60 dias"**
     - Fonte: Instagram → pessoas que interagiram

2. **Criar campanha retargeting**:
   - Objetivo: Vendas
   - Orçamento: R$ 21/dia, 7 dias (~R$ 150)
   - Públicos: use os 3 criados acima (Meta combina).
   - Criativo: **Oferta de "último dia"** — use o post do Dia 30 com um
     selo de "Oferta de lançamento termina HOJE".
   - Copy mais curto e direto: "Você viu a Trilha DEVOPSRAIZ e saiu. Se
     tá em dúvida, tem 7 dias de garantia Hotmart. Link na bio."

3. **Exclusão obrigatória**: exclua quem já comprou (evita queimar budget).

**Meta realista Semana 4:** se tudo alinhou, 2-8 vendas atribuídas.
Receita: R$ 200-800. **ROAS alvo: 2-5x.**

---

## Quando escalar

Se o ROAS ficar > 3.0 por 2 semanas seguidas:
- **Mês 2**: dobre o orçamento pra R$ 600/mês.
- **Mês 3**: R$ 1.200-2.000/mês e abra campanhas separadas por ebook.

Se o ROAS < 1.0 em 2 semanas:
- Pause ads. Volte a focar em orgânico por 2 semanas (mais posts,
  mais engajamento nos DMs).
- Reavalie se o preço do produto Hotmart tá atrativo.

---

## Perguntas frequentes

**"Preciso fazer anúncio no Google também?"** — Não no começo. Meta Ads
converte mais rápido pra infoproduto em 2026 que Google Ads. Deixe
Google/YouTube pra Mês 3+.

**"E TikTok Ads?"** — Não com orçamento de R$ 300/mês. TikTok Ads precisa
de no mínimo R$ 50/dia pra Meta aprender. Foque Meta por enquanto.

**"Posso usar só Reels na Meta?"** — Sim, e aliás é recomendado. A Meta
tá priorizando Reels pra competir com TikTok. O Reel Dia 1 da automação
é seu criativo principal.

**"Quanto tempo até ter retorno?"** — Realista: Mês 1 pode ficar no
zero a zero (empata). Lucro consistente começa Mês 2-3. **Não desista
no primeiro mês se não vender** — isso é curva normal de conta nova.

---

## Checklist antes de rodar o primeiro real em ads

- [ ] Pixel Meta instalado na Hotmart
- [ ] Events Manager mostra eventos `ViewContent` e `InitiateCheckout` funcionando
- [ ] Conta de anúncios criada e cartão adicionado
- [ ] Limite mensal R$ 500 configurado (segurança)
- [ ] Semana 1 orgânica concluída (você sabe qual é o post-vencedor)
- [ ] Criativos prontos (PNGs + Reel Dia 1 já publicados)
- [ ] Pelo menos 200 seguidores (senão o Lookalike 1% não funciona direito)

Quando tudo acima estiver ✓, você tá pronto pra Semana 2 de ads.
