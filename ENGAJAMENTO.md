# Engajamento — como sair de 17 seguidores

> A verdade dura: postar sozinho com conta zerada é jogar no vazio. O
> algoritmo não distribui post de quem ninguém engaja. Os **primeiros 500
> seguidores são manuais** — você vai atrás, não eles. Depois disso o
> algoritmo ajuda.

Essa é uma estratégia de **1h/dia** durante os primeiros 30 dias. Não é
bonita, é operacional. Mas funciona.

---

## Parte 1 — Ritual diário de 1 hora (a parte que ninguém quer fazer)

### Bloco A: Resposta (20 min, logo após postar)

Toda publicação, as primeiras 4 horas definem o alcance. O algoritmo do
Instagram monitora em tempo real: se um post começa com muitos comentários
e respostas rápidas, ele empurra pra mais gente.

**Rotina:**
1. Publica às 19:00 (horário do calendário)
2. Até 19:30: responde TODOS os comentários que chegarem
3. Cada resposta tem 3-5 palavras pelo menos ("valeu!" não conta).
   Comentários longos do autor **ampliam alcance**.
4. Até 20:00: volta ao post e responde novos.
5. Até 23:00: última passada.

**Script de resposta pra 5 cenários comuns:**

| Comentário | Sua resposta |
|---|---|
| "Conteúdo top!" | "@fulano valeu! Qual parte que mais te chamou atenção? Faço um post aprofundando." |
| "Já uso Docker" | "@fulano massa! Qual setup? Swarm ou K8s? Tô preparando um carrossel de K8s sexta." |
| "Comprei a trilha" | "@fulano que massa irmão! Qualquer dúvida me chama no DM. Me conta quando terminar o Ebook 2." |
| "Vc usa o que em produção?" | "@fulano varia muito. Na última que implementei: EKS + Istio + ArgoCD. Vou fazer post disso." |
| "[Crítica]" | "@fulano entendo seu ponto. Na minha experiência [discordância respeitosa]. Mas obrigado pelo contraponto." |

### Bloco B: Dar valor primeiro (20 min, durante o dia)

A cada dia, você comenta em **15 posts de criadores maiores** da sua
área. Não é spam — é comentário útil, técnico, que **agrega valor** ao
post original.

**Lista de criadores-alvo** (pesquise e siga se ainda não segue):

**DevOps/Cloud BR:**
- @lucasmontano
- @fulllcycle (Full Cycle)
- @codigofontetv
- @rocketseat
- @devquestoes
- @pachicodes
- @devsoutinho
- @gustavoguanabara

**Empresas/comunidades:**
- @awsbrasil
- @microsoftbr
- @googlecloudbrasil
- @linuxfoundation
- @cncfofficial

**Internacionais (em inglês):**
- @techwithnana
- @thedeveloper

**Onde comentar:**
- **NÃO** em posts com 2000+ comentários — seu comentário some
- **SIM** em posts com 20-200 comentários — chance de aparecer
- Posts **recentes** (< 2h) — algoritmo ainda está distribuindo

**Template de comentário útil:**

```
Bom ponto sobre [X]. Só complementando: [observação técnica própria]
[opcional: emoji leve]
```

**Exemplo real pra post de Kubernetes:**

Post original: "Kubernetes volumes podem ser estáticos ou dinâmicos."

Comentário bom: "Pra quem tá começando, vale ressaltar que StatefulSet +
PVC dinâmico é praticamente obrigatório em produção — ReplicaSet com
volumes quebra em rolling update."

Comentário ruim: "top!!! 🔥🔥"

### Bloco C: Hospedar conversa (20 min)

Abra sua lista de DMs e Stories.

**Stories diários (3 por dia):**
1. Manhã: foto do setup + 1 frase ("quinta-feira, escrevendo o ebook 4")
2. Meio-dia: enquete ("você usa Terraform ou Pulumi?" — pergunta provocadora)
3. Noite: um print de algum log/erro interessante ("alguém já viu isso?")

Cada story gera 2-5 respostas no DM. **Responde TODAS em até 1h**.

**Cada DM que chegar:**
1. Responde primeiro com pergunta aberta (ex: "massa! em que tá trabalhando?")
2. Conversa técnica por 3-5 mensagens
3. Se fizer sentido, menciona a Trilha naturalmente (sem forçar)

DMs convertem **10x mais que posts**. São os seus primeiros clientes.

---

## Parte 2 — Lead magnet (configurar 1x, roda sempre)

O maior erro: pedir "link na bio" pra vender. Venda direta pra quem nunca
ouviu falar de você tem taxa de 0.5%.

**Troca: você dá um capítulo grátis em troca do email** OU em troca de
"seguir + salvar + comentar a palavra DOCKER".

### Opção A — Comentário trigger

Fazer posts que peçam "comenta DOCKER pra eu mandar o capítulo 1 grátis
no DM". Mecânica:

1. Usuário comenta a palavra
2. Você usa o **ManyChat** (grátis até 1000 contatos) — automatiza DM
3. ManyChat envia: "Valeu pelo interesse! Aqui está o cap 1 grátis: [link]"
4. Usuário abre o DM, clica no link, baixa o PDF
5. No final do PDF: "quer a trilha completa? [link pro Hotmart]"

**Conversão esperada:** 10-20% dos que baixam o PDF clicam pra ver a trilha.
Dos que clicam, 3-10% compram.

### Opção B — Newsletter

Usa o **Beehiiv** ou **ConvertKit** (grátis até 1000 assinantes).

1. Cria landing page simples em tr99.com.br/newsletter
2. Formulário: email + nome
3. Em troca: "cap 1 do ebook 1 grátis + email semanal com dica DevOps"
4. Autoresponder manda o PDF automaticamente

Newsletter converte 5-10x mais que Insta a médio prazo porque **você
controla o canal**.

---

## Parte 3 — Traffic source não-Instagram (multiplica alcance)

Ninguém descobre Instagram pelo Instagram. Você precisa **plantar links
em outros lugares** que puxam pro seu perfil.

### 3.1 LinkedIn (maior potencial pro seu nicho)

Devs BR passam MUITO tempo no LinkedIn.

**Estratégia:**
- 1 post por semana replicando o conteúdo do Insta (carrossel → imagem + texto longo)
- Link do Instagram no seu perfil
- Comente em posts de empresas de tech com link sutil

**Template de post LinkedIn:**
```
[mesmo hook do carrossel Insta]

[desenvolvimento em texto — 3-4 parágrafos]

Esse post é um carrossel completo no meu Instagram → @devopsraiz_oficial

#devops #cloud #carreira
```

### 3.2 Threads (Meta, integrado com Insta)

Cada post do Insta, replica um resumo em 1-2 threads.
Threads tá em fase de crescimento, alcance orgânico altíssimo.

### 3.3 Reddit r/brdev

Não spam — participe. Poste **respostas técnicas úteis** em threads
existentes. No seu perfil, bio aponta pro Insta.

### 3.4 GitHub README

No README dos seus repos públicos:
```markdown
## Sobre o autor
Tiago Alves — Cloud + DevOps + IA
📱 Instagram: @devopsraiz_oficial
📚 Trilha completa: https://go.hotmart.com/S105313699A?dp=1
```

### 3.5 Stack Overflow

Bio do seu perfil SO aponta pro Insta + Trilha. Cada resposta que você dá
é uma chance de alguém clicar.

### 3.6 Discord de devs

Comunidades brasileiras:
- Código Fonte TV
- Rocketseat
- Alura
- Brasileirando no GitHub

Participe. Não posta link logo. Dá valor primeiro. Depois de 2 semanas,
seu nome fica conhecido e link na bio do Discord puxa tráfego.

---

## Parte 4 — Parcerias & collabs (aceleram 10x)

### 4.1 Micro-influencers

Identifica **10 contas dev BR com 5k-50k followers**. Manda DM personalizado:

```
Oi [nome], beleza?

Vi teu post sobre [X] — ajudou muito.

Sou o Tiago, acabei de lançar uma trilha de ebooks de DevOps +
Cloud + IA em português. Queria te mandar cortesia (todos os 6
ebooks grátis) pra você usar/ler.

Sem compromisso de divulgar nada. Se curtir e quiser comentar
algo comigo via story ou post, eu agradeço muito — mas fica à
vontade.

Manda teu email que te mando o link de download?
```

Taxa de resposta: ~30%. Dos que aceitam, ~50% posta alguma coisa natural
nos stories. Cada um pode render 20-100 seguidores.

### 4.2 Collab Reels

Convida gente pra fazer um Reel em dupla (Instagram permite collab
oficial — aparece no feed dos dois).

Pitch: "Topa a gente fazer um Reel juntos sobre [tema]? Eu faço o roteiro,
você grava 15s falando X, eu edito."

### 4.3 Lives conjuntas

Uma vez por mês, uma live de 30 min com algum criador parceiro. Traz
audiência dele pra você.

---

## Parte 5 — O primeiro post de "viralização" intencional

Nos próximos 30 dias, vale tentar **1 post específico pra viralizar**.
Tentou viralizar significa: post que tem potencial de espalhar **sem
depender da sua base** (porque você não tem).

**Formatos que viralizam fácil:**

1. **"X coisas que [público-alvo] não faz"** — gera identificação
   Ex: "10 coisas que dev Pleno nunca fala pro Junior"

2. **Contracultura / polêmica técnica**
   Ex: "Por que eu parei de usar Kubernetes em projetos pequenos"

3. **Mapa / Roadmap visual**
   Ex: "Roadmap DevOps 2026 em 1 imagem" (o que já está no seu calendário, Dia 11)

4. **Análise de caso público**
   Ex: "Como a AWS caiu ontem: explicado em 8 slides"

5. **Tool comparison grande**
   Ex: "Terraform vs Pulumi vs CDK: qual escolher em 2026"

**Reserve o Dia 30 do calendário pra UM desses formatos.** Agende
pra quinta-feira (dia de maior engagement).

---

## Parte 6 — Quando investir em paid ads

**NÃO antes de ter:**
- 200 seguidores orgânicos
- 5+ posts com > 50 saves cada
- Pixel Meta funcionando no Hotmart

**Sinal verde pra começar pagar:**
- Post orgânico teve > 5000 impressions
- CPC médio no teste de R$5 foi < R$0.50
- Você identificou criativo-vencedor (o post mais salvo das primeiras 2 semanas)

Plano completo em `CAMPANHAS_PAGAS.md`.

---

## Parte 7 — Métricas que você rastreia semanalmente

Toda segunda-feira 8h, 10 min de análise:

| Métrica | Onde vê | Alvo semana 1 | Alvo semana 4 |
|---|---|---|---|
| Followers | Insights > audience | +30 | +150 |
| Avg saves/post | Insights > content | 5 | 30 |
| Avg shares/post | Insights > content | 2 | 15 |
| Cliques no link bio | Insights > actions | 15 | 100 |
| DMs recebidas | Inbox manual | 5 | 40 |
| Vendas atribuídas | Hotmart | 0-1 | 2-5 |

Se uma métrica estagnar, ajusta o conteúdo ou frequência.

---

## Parte 8 — Armadilhas a evitar

- ❌ **Comprar seguidores** — trava o alcance por 90 dias
- ❌ **Bots de automação** pra curtir/comentar em outros posts
- ❌ **Spam em DM** — conta pode ser banida em 3 dias
- ❌ **Deletar post com pouco engajamento** — conta nova oscila muito
- ❌ **Seguir 500 pessoas no dia 1** — algoritmo classifica como bot
- ❌ **Usar hashtags tipo #love #followme** — público errado, diminui alcance
- ❌ **Repostar carrossel como 10 posts separados** — Instagram detecta e pune
- ❌ **Ignorar DMs** — mata rapport
- ❌ **Bio sem link** — já resolvemos

---

## Checklist diário (copia e cola onde te lembra)

**Manhã (15 min):**
- [ ] Story com foto do setup / dica rápida
- [ ] Responde DMs da noite
- [ ] Comenta em 5 posts de criadores grandes

**Almoço (15 min):**
- [ ] Responde comentários recentes
- [ ] Story com enquete/pergunta
- [ ] Comenta em 5 posts novos

**Noite (30 min):**
- [ ] Publica o post do dia (calendário diz a hora)
- [ ] Nas primeiras 2h: responde TODOS os comentários
- [ ] Story com print/bastidor
- [ ] Comenta em mais 5 posts

**Fim de semana:**
- [ ] 1 post LinkedIn replicando carrossel da semana
- [ ] 1 thread no Threads reciclando post mais curtido
- [ ] 1-2 DMs pra micro-influencers (2-3 por semana)

---

## Resumo: 30 dias, 3 fases

**Semana 1 (seguidores 17 → ~80):** Ritual diário. Nada de ads. Foco em
comentários e DMs. Objetivo é **aprender** o que engaja seu público.

**Semana 2-3 (80 → ~250):** Inicia parcerias. Lead magnet ativo. Primeira
campanha paga pequena (R$ 50) pra testar criativo vencedor.

**Semana 4 (250 → 500+):** Escala a campanha paga (R$ 150). 1 post de
tentativa de viralização. Fecha o ciclo com retargeting.

**Alvo mês 1: 500 seguidores + 2 vendas atribuídas.**
**Alvo mês 3: 2.000 seguidores + 10-20 vendas/mês.**
**Alvo mês 6: 10.000 seguidores + runway estável.**

Não é rápido. É realista.
