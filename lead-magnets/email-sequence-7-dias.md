# Sequência de email — 7 dias pós-captura (lead magnet K8S)

## Estratégia

Fluxo automatizado disparado quando email é capturado via ManyChat keyword K8S. Cada email cria uma camada de:
1. **Trust** (entrega o que prometeu, mostra valor)
2. **Authority** (técnica real, sem fluff)
3. **Curiosity** (preview de outros ebooks)
4. **Urgency** (cupom FUNDADOR válido só pros 100 primeiros)

**Conversão esperada:** 5-10% da lista compra na sequência (info-produto técnico R$ 100-300).
Se chegar 30 leads/mês → 1.5-3 vendas/mês só de email, sem precisar do tráfego direto Hotmart.

## Onde configurar

**Opção A — Dentro do ManyChat (mais simples)**
ManyChat tem fluxo de "email follow-up" nativo. Limite gratuito: 1000 leads, ilimitado nos planos pagos.

**Opção B — Mailerlite / ConvertKit / Beehiiv (free até 1000 leads)**
Integra ManyChat → Mailerlite via Zapier (free). Email tem entregabilidade superior, melhor pra escala futura.

**Recomendação:** começa no **ManyChat** (já vai estar usando), migra pra Mailerlite quando passar de 200 leads.

## Os 7 emails

### Email 1 — Day 0 (mesma hora da captura)
**Assunto:** ✅ Seu PDF "10 erros K8s" — DevOpsRaiz

```
E aí [primeiro nome],

Aqui é o Tiago do @devopsraiz_oficial.

Conforme combinado, segue o PDF "10 erros que mandam dev junior pro CrashLoopBackOff":

📥 [BOTÃO: Baixar o PDF]
(link: raw.githubusercontent.com/.../10-erros-k8s-junior.pdf)

Lê com calma. Se aparecer um erro chato no kubectl, abre aí e busca pelo nome.

PS: nos próximos dias vou te mandar uns conteúdos extras que podem te ajudar a virar Pleno mais rápido. Mas se não quiser, tem link de descadastro lá no fim.

Bons deploys,
Tiago — DevOpsRaiz
```

### Email 2 — Day 1
**Assunto:** O erro mais caro que vi em produção (não tá no PDF)

```
E aí, beleza?

O PDF cobre os 10 erros mais COMUNS em K8s. Mas tem um erro que tá fora — porque é raro, mas quando acontece custa MUITO.

É o que eu chamo de **"silent OOM"**:

→ Pod fica em estado Running. ✅
→ HPA não escala (parece que tá tudo bem). ✅
→ Mas a aplicação trava silenciosamente. ❌

Causa: você setou request de memória mas esqueceu o LIMIT. Aí o kernel não mata (não passou do limit), mas o GC trava o app.

**Sintoma típico:** latência P99 sobe de 200ms pra 5s sem alerta nenhum.

**Fix:**
sempre configura request E limit no spec do pod.

Esse tipo de detalhe é o que separa Junior de Pleno — saber o COMPORTAMENTO do sistema, não só o COMANDO.

Tem um capítulo inteiro disso no Ebook 5 da Trilha (Observabilidade e SRE).

Se quiser ver, tá aqui: go.hotmart.com/S105313699A?dp=1

Te mando outra dica amanhã.

Tiago
```

### Email 3 — Day 3
**Assunto:** Você sabe quanto sua AWS tá QUEIMANDO de dinheiro?

```
Mudando de tópico — quero te mostrar algo que vai chocar.

Pesquisa Gartner 2024:
**32% do orçamento médio de cloud é desperdiçado por falta de visibilidade.**

Empresa que gasta R$ 100k/mês em AWS, joga R$ 32k no lixo.

E o pior: a maioria nem sabe.

Os 5 vazamentos mais comuns que eu já encontrei em auditoria:

1. EBS volumes órfãos (instância foi deletada, disco ficou cobrando)
2. Snapshots sem política de rotação
3. NAT Gateway em vez de VPC Endpoint
4. Load Balancer parado mas cobrando
5. CloudWatch Logs sem retention

Cada um sozinho parece pouco. Junto vira fortuna.

Como descobrir? Construir seu painel de FinOps multi-cloud.

No **Ebook 1 da Trilha DEVOPSRAIZ** eu mostro do zero como integrar:
✅ AWS Cost Explorer
✅ Azure Cost Management
✅ GCP Billing
✅ OCI

→ Num único painel Node.js + React + IA detectando anomalias automaticamente.

Tá aqui se quiser ver: go.hotmart.com/S105313699A?dp=1

Tiago
DevOpsRaiz
```

### Email 4 — Day 5
**Assunto:** Não passei pela faculdade. E hoje sou tech lead.

```
[primeiro nome], conta franca aqui.

Eu não passei pela faculdade. Comecei a programar em PHP4 em 2009 num PC de R$ 800.

Em 2026 sou tech lead de cloud-native, opero K8s em produção em 4 clouds (AWS, Azure, GCP, OCI) e construí a Trilha DEVOPSRAIZ com 6 ebooks.

Por que isso importa pra você?

Porque o caminho **não é** só estudar. É:
1. Estudar a tecnologia (qualquer curso decente serve)
2. **Aplicar num projeto real** (de ponta a ponta)
3. Aprender a explicar o que fez

A Trilha foi feita exatamente pra isso. Não são "tutoriais soltos". É um projeto único, integrado, que evolui ebook a ebook:

- Ebook 1 → painel multi-cloud
- Ebook 2 → mesma stack roda em K8s
- Ebook 3 → vira SaaS multi-tenant
- Ebook 4 → ganha IA conversacional (RAG + Agents)
- Ebook 5 → recebe observabilidade e SRE
- Ebook 6 → fica seguro (Zero Trust + LGPD)

No final você tem um projeto **vendável**. E mais: sabe explicar cada decisão técnica numa entrevista.

go.hotmart.com/S105313699A?dp=1

Não vou te empurrar. Mas se você é Junior/Pleno e quer subir de nível, é o caminho mais direto que conheço.

Tiago
```

### Email 5 — Day 7
**Assunto:** 🎁 Cupom FUNDADOR — só hoje e amanhã

```
[primeiro nome], chegou o momento.

Você entrou na lista de FUNDADOR quando me deu seu email pelo PDF do K8s.

Como prometido, segue o cupom exclusivo pros 100 primeiros:

**Cupom: FUNDADOR20**
Desconto: **20% OFF** na Trilha completa
Válido: **48h a partir desse email**

Como aplicar:
1. Vai em go.hotmart.com/S105313699A?dp=1
2. Clica em "Comprar agora"
3. No checkout, cola o cupom: **FUNDADOR20**
4. Confirma o desconto antes de pagar

Por que esse desconto é único:

→ É o melhor preço que a Trilha vai ter (sério, sem #BlackFriday tipo)
→ É só pra primeiros 100 que entraram na lista (limitado)
→ Vai expirar em 48h e não volta

Se ainda não tá certeza, sem stress. Continua nos próximos emails que mostro mais técnica e quando o cupom expirar, tá ok também.

Mas se já tava considerando: hoje é o dia.

go.hotmart.com/S105313699A?dp=1

Tiago
```

### Email 6 — Day 8 (último dia do cupom)
**Assunto:** ⏰ Restam 24h pro cupom FUNDADOR20

```
Lembrete rápido [primeiro nome] — restam 24h pro cupom FUNDADOR20 (20% off).

Não vou ficar empurrando, mas vale a conta:

Trilha completa preço cheio: R$ X
Com cupom FUNDADOR20: R$ Y (economiza R$ Z)

Entram no pacote:
✅ 6 ebooks PDF (1.500+ páginas no total)
✅ Código completo de cada projeto (multi-cloud, K8s, IA, SaaS, observabilidade, security)
✅ Update por 1 ano (toda atualização que eu fizer chega no seu email)
✅ Acesso à comunidade Discord (em construção)

Cupom: **FUNDADOR20**
Link: go.hotmart.com/S105313699A?dp=1

Expira amanhã 23:59.

Tiago
```

### Email 7 — Day 14
**Assunto:** O que você vai fazer com 30 dias de prática?

```
Última mensagem dessa série (relax, depois dela só te mando se eu publicar algo realmente útil).

30 dias atrás você baixou o PDF do K8s. Quero te perguntar:

→ Aplicou alguma técnica do PDF em prod?
→ Conseguiu resolver algum CrashLoopBackoff em menos tempo?

Se sim, **me responde aqui** com 1 frase só me contando. Adoro saber que ajudou.

E se você ainda tá em dúvida sobre a Trilha, deixa eu fazer um pacto contigo:

Compra hoje. Baixa o Ebook 1 (FinOps Multi-Cloud). Aplica em 1 stack que você já roda.

Se em **30 dias** você não conseguir achar pelo menos R$ 500 de vazamento de cloud na sua empresa atual ou de algum projeto que mexe — me responde esse email pedindo reembolso. Devolvo 100%, sem perguntas.

Se você é Junior/Pleno em DevOps/Cloud em 2026 e não tem um projeto end-to-end pra mostrar em entrevista, esse é o caminho mais direto.

go.hotmart.com/S105313699A?dp=1

Boa jornada — e se um dia eu puder ajudar mais, é só me chamar no DM @devopsraiz_oficial.

Tiago
DevOpsRaiz
```

## Configuração técnica (ManyChat)

ManyChat → Automation → Sequence → Email Drip

**Trigger:** Tag `lead_k8s` adicionada
**Step delays:**
- Email 1: send immediately
- Email 2: 1 day after
- Email 3: 3 days after
- Email 4: 5 days after
- Email 5: 7 days after
- Email 6: 8 days after
- Email 7: 14 days after

**Stop sequence se:**
- Lead clica em link Hotmart e completa Purchase (Webhook do Hotmart pixel)
- Lead descadastra
- Lead responde marca "spam"

## Métricas pra acompanhar

| Métrica | Meta saudável |
|---|---|
| Open rate emails 1-3 | > 40% |
| Open rate emails 4-7 | > 25% |
| Click rate (link Hotmart) | > 5% |
| Conversão venda na sequência | 5-10% |
| Unsubscribe rate | < 5% |

## Próxima evolução (quando passar de 200 leads)

- Migrar pra Mailerlite/ConvertKit (entregabilidade superior)
- Adicionar A/B test no Email 5 (subject lines)
- Segmentar por tag (`topic_kubernetes` recebe seq diferente de `topic_finops`)
- Email 8 (Day 30): "última chance" com bonus extra (consultoria 30min de presente)
