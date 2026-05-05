# Plano de Tráfego Pago — DEVOPSRAIZ

## Objetivo

Transformar **R$ 300/mês** (= R$ 10/dia) em volume real de cliques no link Hotmart pra **validar o preço com dados estatisticamente significantes**. Hoje (Day 15/30) temos só 12 cliques orgânicos em 7 dias — amostra pequena demais pra concluir nada.

Meta com R$ 300/mês: **+150 a 300 cliques extras no Hotmart**, suficiente pra:
- Confirmar se preço atual converte (>1% = aprovado, <0,5% = baixar)
- Capturar 30-60 leads via lead magnet (ManyChat keyword K8S)
- Crescer +200 a 500 seguidores qualificados em 30 dias

## Estrutura recomendada (3 campanhas)

### Campanha 1 — TRAFEGO REELS (60% do orçamento = R$180/mês = R$6/dia)

Promove os Reels educacionais que já estão prontos no perfil. Otimiza pra cliques no link da bio.

**Setup no Meta Ads Manager:**

| Campo | Valor |
|---|---|
| Objetivo | **Tráfego** |
| Estratégia de lances | Custo por resultado (deixar Meta otimizar) |
| Orçamento | R$ 6/dia, sem data fim |
| Início | Imediato |

**Conjunto de anúncios (criar 2):**

**Conjunto A — DevOps PT-BR** (R$3/dia)
- Localização: Brasil
- Idade: 22-45
- Idioma: Português
- Detalhamento: Interesses
  - "DevOps", "Kubernetes", "Docker"
  - "Amazon Web Services (AWS)"
  - "Programação", "Desenvolvedor de software"
  - "Cloud computing"
- Posicionamentos: Apenas Reels Instagram
- Otimização: **Cliques no link**

**Conjunto B — Carreira Tech BR** (R$3/dia)
- Localização: Brasil
- Idade: 24-40
- Idioma: Português
- Detalhamento:
  - "Carreira", "Educação", "Curso online"
  - "Tecnologia da informação"
  - "Desenvolvedor full stack"
  - "Engenheiro de software"
- Posicionamentos: Reels Instagram + Stories Instagram
- Otimização: **Cliques no link**

**Anúncios (use 2 dos seus reels Pixar como criativo):**
1. **Reel Dia 9 — Terraform 30s** (curto, alto engagement potencial)
2. **Reel Dia 16 — Docker 1.2GB → 150MB** (problema concreto, curiosidade alta)

CTA do anúncio: **"Saiba mais"** → Link do Hotmart `go.hotmart.com/S105313699A?dp=1`

### Campanha 2 — LEAD MAGNET (30% = R$90/mês = R$3/dia)

Promove o carrossel teaser do PDF "10 erros K8s". Otimiza pra **interação com a publicação** (comentários — porque a keyword K8S triggera o ManyChat).

**Setup:**

| Campo | Valor |
|---|---|
| Objetivo | **Engajamento** (engajamento na publicação) |
| Orçamento | R$ 3/dia |
| Posicionamento | Apenas Feed Instagram |
| Otimização | Comentários |

**Público:** mesmo Conjunto A da Campanha 1 (devops/k8s), reduzido pra "só K8s/Docker"
- Interesses: "Kubernetes", "Docker", "Containers"
- Idade: 23-38

**Anúncio:** carrossel teaser dos 5 slides do lead magnet
**CTA da legenda:** "Comenta K8S e recebe o PDF grátis"

> ⚠️ **Atenção Meta policy:** anúncios não podem ter "lead capture" disfarçado. O CTA "comenta X" é OK porque é engagement orgânico no post, não captura direta. ManyChat é stack permitida pelo Meta.

### Campanha 3 — RETARGETING (10% = R$30/mês = R$1/dia)

Retorna em quem viu o perfil mas não clicou no link. **Só ativa depois de 14 dias** (precisa volume mínimo no pixel/audiência).

**Setup (depois de 14 dias):**

| Campo | Valor |
|---|---|
| Objetivo | **Tráfego** |
| Orçamento | R$ 1/dia |
| Otimização | Cliques no link |

**Público customizado:**
- Pessoas que interagiram com Instagram nos últimos 30 dias (visualizaram, salvaram, comentaram)
- Excluir: já cliquearam no link bio (esses já estão no funil principal)

**Anúncio:** Story com depoimento (quando tiver 1ª venda) OU oferta direta com cupom FUNDADOR.

## Pixel + Conversões (configurar antes de lançar)

### Meta Pixel
1. Meta Business Manager → Eventos → Adicionar Origem → Pixel
2. Cria pixel "DevOpsRaiz Pixel"
3. **Instala no Hotmart** via JavaScript (Hotmart aceita pixel terceiro):
   - Hotmart > Produto > Página do produto > Configurações > Pixel
   - Cola o ID do Pixel
4. Eventos automáticos: `PageView`, `ViewContent`

### Eventos personalizados (importantes)
- `InitiateCheckout` — quando clica "Comprar agora"
- `Purchase` — quando completa pagamento

> 💡 Hotmart configura `Purchase` automaticamente se você adicionar o pixel no dashboard. Confirma em Hotmart > Estatísticas > Pixel.

## Cronograma de execução

### Semana 1 (Days 16-22 — esta semana)
- [ ] Criar Pixel no Meta
- [ ] Instalar Pixel no Hotmart
- [ ] Setup ManyChat keyword K8S (já tem PDF pronto)
- [ ] Postar carrossel teaser K8S no @devopsraiz_oficial
- [ ] **Lançar Campanha 1** (R$6/dia, Reels)
- [ ] **Lançar Campanha 2** (R$3/dia, lead magnet)
- ⏸️ Campanha 3 ainda não (precisa pixel acumular dados)

### Semana 2 (Days 23-29)
- [ ] Avaliar dados Campanha 1: CPC, CPM, taxa de conversão
- [ ] **Pausar conjunto que tiver CPC > R$ 1,50** (foi mal segmentado)
- [ ] Escalar conjunto vencedor +50% orçamento
- [ ] Lançar Campanha 3 (retargeting) se já tiver 100+ visitas no pixel

### Semana 3 (Days 30-36)
- [ ] Análise full do mês 1
- [ ] Decidir preço (manter / cupom / baixar) com base em DADOS, não chute
- [ ] Re-orçamentar mês 2 baseado em ROAS

## KPIs pra acompanhar (semanal)

| Métrica | Meta saudável | Bandeira vermelha |
|---|---|---|
| CPC (custo por clique) | < R$ 1,50 | > R$ 3,00 |
| CTR | > 1% | < 0,5% |
| CPM | < R$ 25 | > R$ 50 |
| Custo por lead (ManyChat) | < R$ 5 | > R$ 12 |
| Custo por venda Hotmart | < R$ 50 | > R$ 100 |
| ROAS (retorno) | > 3x | < 1x |

> Reference: info-produto técnico R$ 100-300, ROAS 3x = saudável, 5x+ = excelente.

## Criativo: como fazer o Reel virar anúncio

**Não duplica conteúdo.** Usa o post orgânico que já tá no perfil:

1. Meta Ads Manager → Criar anúncio
2. Em "Identidade", escolhe a conta `@devopsraiz_oficial`
3. Em "Mídia", escolhe **"Usar publicação existente"**
4. Cole a URL do reel ou seleciona da grade
5. Vantagem: **mantém o engagement orgânico do post** (likes, comentários) e adiciona "Patrocinado". Algoritmo trata como conteúdo top.

## Stop-loss (regras pra não queimar dinheiro)

**Pausa imediata se em 7 dias:**
- CPC > R$ 5 (público mal definido)
- CTR < 0,3% (criativo ruim)
- Zero comentários com keyword K8S na Campanha 2 (ManyChat broken ou flow ruim)

**Cupom de FUNDADOR só ativa se:**
- 100+ cliques Hotmart sem 1 venda → confirma teste de preço
- Lead na lista pediu desconto explicitamente
- Day 30 chega com <2 vendas → precisa puxar gatilho promocional

## Resumo executivo

```
ORÇAMENTO TOTAL: R$ 300/mês
├── R$ 180 — Tráfego Reels (validar funil)
├── R$  90 — Lead magnet (capturar emails)
└── R$  30 — Retargeting (a partir da semana 2)

META MÊS 1:
✅ +200-500 seguidores qualificados
✅ +150-300 cliques Hotmart
✅ +30-60 leads ManyChat (com email)
✅ 1-3 vendas (validação estatística)
✅ Pixel acumulando dados pra otimizar mês 2

REVIEW MENSAL: Day 30 (15/05)
- Análise full
- Decisão sobre preço
- Plano mês 2 (escalar / pivotar / pausar)
```
