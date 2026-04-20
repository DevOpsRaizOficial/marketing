# Marketing DEVOPSRAIZ — Kit de Lançamento

Tudo que você precisa para sair do **16 seguidores e 0 posts** até ter uma
rotina editorial profissional vendendo a Trilha DEVOPSRAIZ no Instagram.

- **Conta-alvo:** [@devopsraiz_oficial](https://instagram.com/devopsraiz_oficial)
- **Produto:** Trilha DEVOPSRAIZ no Hotmart (ID 7537240)
- **Janela:** 30 dias a partir de **21/04/2026**
- **Orçamento de paid:** R$ 300/mês

---

## Estrutura das entregas

```
marketing/
├─ calendario-editorial-30-dias.xlsx     ← 30 posts prontos com legenda + CTA + hashtags
├─ criativos/                            ← 11 PNGs prontos para postar (Instagram)
├─ automacao/                            ← scripts para publicar via Meta Graph API
└─ README.md                             ← este documento
```

---

## 1. Calendário editorial (30 posts)

Abra `calendario-editorial-30-dias.xlsx`. Três abas:

1. **Calendario 30 dias** — uma linha por post, com `Dia`, `Data`, `Horário`,
   `Pilar` (Educacional / Carreira / Autoridade / Venda), `Formato` (Carrossel,
   Reel, Post único, Story), `Ebook vinculado`, `Título`, `Legenda completa`,
   `CTA`, `Hashtags` e `Sugestão visual`.
2. **Estrategia Resumo** — distribuição por pilar, ebook, formato, horário
   ótimo, métricas-alvo de 30 dias e plano de R$ 300 em paid.
3. **Pool de Hashtags** — categorias temáticas (AWS, Kubernetes, IA, SRE,
   Segurança, Carreira, Comunidade) para mixar em cada post.

### Como usar

- Copie a célula de "Legenda Completa" do dia → cole na caixa de post do
  Instagram.
- Anexe o criativo correspondente em `/criativos`.
- Ajuste datas se quiser começar em outro dia; o script de automação
  entende o offset a partir de 21/04/2026.

---

## 2. Criativos (11 PNGs prontos)

Todos em **1080×1350** (feed vertical, formato que o Instagram prioriza)
ou **1080×1920** (stories). Identidade visual alinhada com as capas dos
ebooks — cada ebook tem sua cor:

| Arquivo | Post Dia | Ebook | Cor |
|--|--|--|--|
| `01-apresentacao-capa.png` | Dia 1 | Apresentação | Azul |
| `02-docker-vm-vs-container.png` | Dia 2 | Ebook 2 (Docker/K8s) | Laranja |
| `03-aws-custos-queimando.png` | Dia 4 | Ebook 1 (FinOps) | Azul |
| `04-owasp-top-10.png` | Dia 8 | Ebook 6 (Segurança) | Vermelho |
| `05-saas-multi-tenant.png` | Dia 10 | Ebook 3 (SaaS) | Roxo |
| `06-slo-uptime-table.png` | Dia 15 | Ebook 5 (SRE) | Amarelo |
| `07-rag-ia-pipeline.png` | Dia 5 | Ebook 4 (IA/RAG) | Verde |
| `08-frase-junior-vs-senior.png` | Dia 18 | Carreira | Azul |
| `09-fechamento-trilha-completa.png` | Dia 30 | Venda (trilha) | Azul |
| `10-story-cta-link-bio.png` | Story sempre fixado | — | Azul |
| `11-salario-devops-2026.png` | Dia 3 | Carreira | Verde |

Para os posts **sem PNG de capa** (20 restantes), use a coluna "Sugestão
Visual" no XLSX e crie no Canva/Figma seguindo o mesmo padrão:

- **Fundo escuro** `#0F172A` com gradiente radial no topo
- **Hook gigante** (fonte Bold, ~85px)
- **Cor de destaque** conforme o ebook
- **Footer neon** com CTA + `@devopsraiz_oficial`

---

## 3. Automação (Meta Graph API)

Em `automacao/instagram_publisher.py` você tem um publisher que:

- Lê a aba `Calendario 30 dias` do XLSX
- Monta a legenda final (corpo + CTA + hashtags)
- Cria o container de mídia na Meta Graph API e publica
- Loga cada publicação em `publish_log.jsonl`
- Funciona via `cron` (Linux/macOS) ou Agendador de Tarefas (Windows)

### Setup resumido

```bash
cd marketing/automacao
pip install -r requirements.txt

# configure suas credenciais
cp .env.example .env
# edite .env com IG_USER_ID, META_ACCESS_TOKEN e MEDIA_BASE_URL

# valida token e conta
python instagram_publisher.py check

# simula publicação do dia 1 sem chamar API
python instagram_publisher.py dry-run --day 1

# publica o post do dia atual (baseado em 21/04/2026 = Dia 1)
python instagram_publisher.py publish --today
```

**Agendar para rodar todo dia:**

- Linux/macOS: `bash agendar_cron_linux_mac.sh` (cria linha no crontab às 08h)
- Windows: `./agendar_task_windows.ps1` (como Administrador)

### Pré-requisitos Meta (uma única vez)

1. Converter @devopsraiz_oficial em **Conta Profissional** (Creator ou Business).
2. Conectar a conta Instagram a uma **Página do Facebook**.
3. Criar **app Business** em `developers.facebook.com` e habilitar o produto
   "Instagram Graph API".
4. Gerar um **long-lived token** (60 dias) e colocar no `.env`.
5. Hospedar as PNGs de `/criativos` em uma **URL pública** (GitHub raw,
   Cloudflare R2, Cloudinary, AWS S3+CDN) — a Meta baixa as imagens dessa URL.

Detalhes completos no cabeçalho de `instagram_publisher.py`.

### Limitações honestas da Meta Graph API

- ❌ Não agenda posts com mais de 30 dias de antecedência.
- ❌ Não publica **Stories** nem **Reels** de forma oficial (só feed photo/carousel/video).
  - Para Reels/Stories, grave e use o próprio app do Instagram.
- ❌ Precisa de conta **Business**, não funciona em conta Pessoal.
- ✅ Carrosséis de até 10 imagens: suportado (função `create_carousel_container`).

**Plano B (mais simples, sem API):** use ferramentas com UI grátis como
[Metricool](https://metricool.com), [Buffer](https://buffer.com) ou
[Later](https://later.com). Elas agendam feed/Reels/Stories e importam CSV.
A planilha do calendário pode ser exportada para CSV direto do Excel.

---

## 4. Estratégia (resumão rápido)

### Posicionamento
**"Do zero à produção em Cloud + IA — com código completo, sem copy/paste."**

Você vende o fato de que nenhum curso brasileiro faz uma trilha
integrada (1 projeto do ebook 1 ao 6), com código real, em português
técnico de verdade.

### Pilares de conteúdo (proporção nos 30 dias)

| Pilar | % | Posts |
|--|--|--|
| Educacional (carrosséis, dicas técnicas) | 70% | 21 |
| Carreira/Roadmap | 13% | 4 |
| Autoridade/Bastidores | 10% | 3 |
| Venda direta | 7% | 2 |

### Por que esse mix funciona para começar do zero

1. **Educacional domina** porque o algoritmo prioriza *saves* e *shares* — e
   conteúdo técnico de valor é o que mais salva.
2. **Carreira** puxa público ligeiramente maior (iniciantes buscando "como
   virar DevOps") — alimenta topo do funil.
3. **Autoridade** humaniza a marca (quem é o Tiago, por que a trilha existe).
4. **Venda é mínima** até você ter público. Venda pesada em conta zerada
   só queima alcance.

### Regra de ouro do algoritmo (2026)

O Instagram pondera, do mais importante pro menos:
1. **Saves** (sinal de "é conteúdo útil" → recomenda pra outros)
2. **Sends** (DM/compartilhamento — amplificação orgânica)
3. **Tempo de permanência no post** (por isso carrossel com 8-10 slides supera post único)
4. **Comentários longos** (mais de 4 palavras)
5. Curtidas (menos relevante que antes)

**Todos os 30 posts estão escritos pensando nisso:** cada CTA pede *save*,
*comment* ou *share* antes de like.

### Plano de R$ 300 em tráfego pago (3 fases)

**Semana 1 — R$ 0 (só orgânico)**
Não impulsione NADA. Deixe a Meta aprender qual dos 7 posts da semana tem
maior engajamento natural. Esse será seu criativo vencedor.

**Semana 2 — R$ 50**
Impulsione o post mais salvo da Semana 1 como "Boost post". Objetivo:
**Interações** (não alcance, não cliques). Público: Interesses — AWS,
Docker, Kubernetes + idade 22-40 + Brasil.

**Semana 3 — R$ 100**
Crie uma campanha **Advantage+ Shopping** ou **Tráfego** (se não tiver
produto físico) pro link da Hotmart direto. Campanha separada no
Gerenciador de Anúncios, não boost. Público: Lookalike 1% dos que
salvaram 3+ posts.

**Semana 4 — R$ 150**
Retargeting. Quem visitou o link da bio mas não comprou → campanha de
"oferta de lançamento" apontando pro post do Dia 30. Aqui você dobra o
orçamento porque é o público mais quente.

### Pixel da Meta (obrigatório para remarketing)

Peça pro suporte Hotmart te ajudar a instalar o pixel Meta na página de
checkout. Sem isso, você queima os R$ 150 da Semana 4 mirando no vazio.

### Métricas-alvo em 30 dias (realistas para conta zerada)

| Métrica | Meta conservadora | Ambiciosa |
|--|--|--|
| Seguidores | 500 | 1.500 |
| Salvos (soma dos 30 posts) | 800 | 3.000 |
| Cliques no link da bio | 400 | 1.200 |
| Vendas da trilha | 2 | 10 |

Se bater o conservador, você provou que o conteúdo funciona. Aí escala
em R$ 1k+/mês a partir do Mês 2.

---

## 5. Passo-a-passo para o Dia 1 (21/04/2026)

1. **Instagram** → Menu → Configurações → Conta → Mudar para Conta
   Profissional (categoria: "Criador de Conteúdo" ou "Educação").
2. **Perfil** → Editar → Bio: veja sugestão abaixo.
3. **Bio sugerida:**
   ```
   DEVOPSRAIZ 🌱 Cloud + IA + DevOps em PT-BR
   Trilha completa: 6 ebooks, 1 projeto real
   ↓ link direto
   ```
4. **Link da bio:** o próprio link do produto na Hotmart
   (`pay.hotmart.com/...`) ou use uma **linktree/beacons** se quiser
   separar trilha + ebooks avulsos.
5. **Foto de perfil:** sua foto atual já funciona (transmite
   autoridade + rosto humano).
6. **Destaques** (crie no Dia 1 mesmo com 1 story):
   - 📘 Trilha → posts sobre os 6 ebooks
   - 🛠 DevOps → dicas técnicas
   - 🤖 IA → posts de RAG/Agents
   - 🎁 Ofertas → promoções
7. **Publique o Post do Dia 1** às 19:00 (horário definido no calendário).
8. **Responda os comentários** nas primeiras 4 horas — esse é o sinal
   mais forte que o algoritmo usa pra decidir empurrar ou não.
9. **Stories de apoio no Dia 1:**
   - 1 story: "Novo post no feed, passa lá" com sticker de link para o post.
   - 1 story: o próprio `10-story-cta-link-bio.png` com sticker de link
     apontando pra bio/produto.
10. **DMs:** a cada 5 comentários significativos no post, envie uma DM de
    obrigado + pergunta aberta ("qual ebook te interessa mais?"). Isso
    triplica a retenção.

---

## 6. O que você NÃO vai fazer (armadilhas comuns)

- ❌ **Comprar seguidores.** Destrói alcance orgânico nos primeiros 90 dias.
- ❌ **Postar 3x por dia.** Você ainda não tem público pra justificar.
  1 post/dia + 2-3 stories é o correto.
- ❌ **Copiar trechos dos ebooks inteiros.** Post tem que ter 1 ideia
  clara, não substituir o ebook.
- ❌ **Pedir "curte e compartilha".** Peça ações específicas: "salva",
  "comenta X", "marca um amigo que usa Kubernetes".
- ❌ **Fazer boost logo no dia 1.** Espere 1 semana para a Meta aprender
  seu público orgânico.
- ❌ **Deletar posts com pouco engajamento.** Conta nova oscila muito.
  Deixe pra avaliar no Dia 15 com dados.

---

## 7. Próximos passos após o Dia 30

Quando terminar o calendário:

1. **Analise os 30 posts** (Insights do Instagram). Os 5 mais salvos
   viram "posts pilares" que você recicla a cada 3 meses.
2. **Expanda para YouTube Shorts** — reposte os melhores Reels.
3. **Newsletter** — ofereça um capítulo grátis em troca do email.
   Leads da newsletter convertem 10x mais que Instagram.
4. **Lançamento #2** com prova social (prints de quem comprou + depoimentos).
5. Escale o paid para R$ 1.000-3.000/mês com os criativos vencedores.

---

## Suporte

Fez setup da Meta e travou em algum passo? Documente o erro no arquivo
`automacao/publish.log` e rode:

```bash
python instagram_publisher.py check
```

A resposta JSON diz exatamente o que está faltando (token expirado, IG_ID
errado, conta não é business, etc).
