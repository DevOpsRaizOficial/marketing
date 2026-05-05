# ManyChat — Setup keyword K8S (lead magnet PDF)

Objetivo: quem comentar `K8S` (ou `k8s`, `kubernetes`, `crashloopbackoff`) em qualquer post, receber DM com:
1. Mensagem de boas-vindas
2. Pergunta capturando email (lead!)
3. Link de download do PDF
4. CTA pra Trilha completa
5. Marca a tag `lead_k8s` pra futuras campanhas

## Passo 1 — Subir o PDF pra um host público

**Opção A (recomendada): GitHub raw URL**

Push do PDF junto com o repo `marketing`:

```bash
cd ~/Ebooks-DevopsRaiz/marketing
git add lead-magnets/10-erros-k8s-junior.pdf
git commit -m "feat: lead magnet 10 erros k8s junior"
git push
```

URL final pública (vai funcionar 1-2 min depois do push):
```
https://raw.githubusercontent.com/DevOpsRaizOficial/marketing/main/lead-magnets/10-erros-k8s-junior.pdf
```

**Opção B: ManyChat hosting nativo** (mais lento, mas funciona offline do GitHub)
Sobe o arquivo direto no flow do ManyChat (Settings > Files). Limite gratuito = 5 MB. Nosso PDF tem 13.7 KB, cabe folgado.

## Passo 2 — Criar Keyword no ManyChat

ManyChat → **Automation → Keywords → + New Keyword**

| Campo | Valor |
|---|---|
| Keyword names | `K8S`, `k8s`, `KUBERNETES`, `kubernetes`, `CRASHLOOPBACKOFF` |
| Match type | Whole word (ou Contains pra ser mais flexível) |
| Channel | Instagram |
| Trigger on | Comments + DMs |

**Marca também:** "Reply in DM" + "Reply in Comments" pra dupla cobertura.

## Passo 3 — Construir o Flow

**Bloco 1 — Boas-vindas (texto)**
```
Eae mano, valeu pelo interesse! 🔥

Vou te mandar agora o PDF "10 erros que mandam dev junior pro CrashLoopBackOff" — recorte do Ebook 2 da Trilha DEVOPSRAIZ.

Antes, só me confirma: pra qual email mando o PDF? Assim já te garante na lista de fundadores (preço especial pra primeiros 100).
```

**Bloco 2 — User Input (CAPTURA O EMAIL)**

Tipo de input: **Email**
Save to field: **Email** (built-in field do ManyChat)
Quick reply: "Pular" (pra quem quer só o PDF sem dar email)

→ Se preencher email: vai pro Bloco 3a (com agradecimento)
→ Se pular: vai pro Bloco 3b (só PDF, sem CTA fundador)

**Bloco 3a — Agradece + entrega PDF + CTA (com email)**
```
Show! ✅ Te coloquei na lista FUNDADOR.

Em poucos dias você recebe um email com o PDF + dicas extras + cupom de 20% off (só pros 100 primeiros, válido só essa semana).

Por enquanto, segue o PDF aqui:
👇

[Anexa: 10-erros-k8s-junior.pdf — ou link raw GitHub]

Se gostar, dá um 💾 salva e manda pra um amigo dev que já passou raiva com kubectl 😂
```

**Bloco 3b — Sem email**
```
Beleza, segue o PDF:

👇

[Anexa: 10-erros-k8s-junior.pdf]

Se mudar de ideia e quiser entrar na lista de FUNDADOR (cupom 20% off pros 100 primeiros), me responde com seu email aqui que eu cadastro 🚀
```

**Bloco 4 — Tag + CTA Trilha (3 segundos depois)**

Action:
- Add tag: `lead_k8s`
- Add tag: `topic_kubernetes`
- Custom field: `data_lead_k8s` = data de hoje

Mensagem:
```
Curiosidade rápida: a Trilha completa tem 6 ebooks integrados (Cloud, K8s, IA, SaaS, SRE, Security) — todos com código real em PT-BR.

Se quiser ver, tá aqui: 👇
go.hotmart.com/S105313699A?dp=1

Mas sem pressão. Curte o PDF primeiro 😉
```

## Passo 4 — Configurar disparador no comentário

Quando alguém comenta `K8S` num post:
1. ManyChat responde no comentário: `Mandei no DM 📨`
2. Em paralelo, dispara o flow no DM da pessoa

**Trigger setup:**
- Source: Instagram → Comment Reply
- Trigger: Keyword in comment
- Keywords: `K8S`, `k8s`, `KUBERNETES`, `kubernetes`, `CRASHLOOPBACKOFF`
- Action: Send DM (link pro Flow acima)
- Bonus: Reply public comment com `Mandei no DM 📨` (prova social)

## Passo 5 — Setup notificação pra você

Pra você ser avisado quando alguém triggar:

ManyChat → **Settings → Notifications**
- ☑ Notify by email when new lead is captured
- Email: tiago@tr83.com.br

Assim você acompanha em tempo real cada lead novo.

## Verificação (teste antes de divulgar)

1. Abre Instagram com sua conta secundária (ou de um amigo)
2. Vai num post antigo do @devopsraiz_oficial
3. Comenta `k8s` ou `K8S`
4. Esperado: dentro de 5s recebe DM automatizada
5. Responde com email teste
6. Esperado: recebe PDF + tag `lead_k8s`

Se funcionar, libera nas próximas postagens com CTA tipo:
> "Comenta **K8S** que mando o PDF '10 erros que mandam dev junior pro CrashLoopBackOff' direto no seu DM 📨"

## Métricas pra acompanhar

ManyChat → Reports:
- **Keyword triggers / dia**: quantos comentaram K8S
- **Email capture rate**: quantos % dos triggers deram email
- **Tag `lead_k8s` count**: total de leads acumulados

Meta saudável após 14 dias: 30+ leads, 50%+ capture rate.
