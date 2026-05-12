# HOTMART_SETUP — Configuração dos produtos e cupons

Documento operacional para colocar no ar os dois produtos do funil DevOpsRaiz e os respectivos cupons de desconto.

## Visão geral do funil

| Camada | Produto | Preço cheio | Cupom | Preço final | Função |
|---|---|---|---|---|---|
| 1 | Ebook gratuito "Zero ao Deploy" | grátis | — | grátis | Captura email/seguidor |
| 2 | **PDF de Apoio (30 unidades)** | **R$ 9,90** | **CUPOM50** | **R$ 4,95** | Micro-monetização |
| 3 | Trilha DEVOPSRAIZ completa | R$ 199,99 | SEGUIDOR80 | R$ 39,99 | Produto principal |

A camada 3 já existe no seu Hotmart (ID 7537240). Vamos focar em montar a camada 2 e validar os 2 cupons.

---

## Parte 1 — Criar o produto "PDF de Apoio" no Hotmart

Você tem 2 caminhos. Escolha 1.

### Caminho A: 1 produto-pai com 30 variações (recomendo)

**Vantagens:** 1 página de checkout, 1 cupom CUPOM50 funciona pra qualquer dia, 1 link de afiliado, gestão simples.

1. Hotmart → **Produtos** → "Criar produto" → Tipo: **Ebook**
2. **Nome:** `PDF de Apoio · Trilha DEVOPSRAIZ`
3. **Descrição (copy):**

   ```
   Cada PDF de Apoio é o complemento de UM short do canal @DevOpsRaiz no
   YouTube. Inclui:
   • Resumo do conceito (4 tópicos)
   • 3 comandos copy-paste prontos
   • Troubleshooting dos erros mais comuns
   • Exercício prático
   • Cupom SEGUIDOR80 (80% off) pra Trilha completa

   30 PDFs disponíveis. Compra 1, todos, ou pacote completo.

   Tira-dúvidas direto comigo no WhatsApp (11) 96482-3126.
   ```

4. **Preço:** R$ 9,90
5. Faça upload de **TODOS os 30 PDFs** em "Arquivos de entrega" (pdf-apoio-01-* até pdf-apoio-30-*)
6. **Categoria:** Programação / Tecnologia
7. Salvar

### Caminho B: 30 produtos individuais

**Vantagens:** Métricas por aula, possibilidade de variar preço.
**Desvantagens:** Gestão repetitiva, 30 links, 30 vezes mais trabalho.

Cria 30 produtos seguindo o mesmo padrão acima, ajustando título/descrição/PDF de entrega por dia.

---

## Parte 2 — Criar o cupom **CUPOM50** (50% off no PDF)

1. Hotmart → produto **PDF de Apoio** → aba "Cupons"
2. "Criar novo cupom"
3. **Código:** `CUPOM50`
4. **Tipo:** Porcentagem
5. **Valor:** `50%`
6. **Aplicável a:** apenas este produto (PDF de Apoio)
7. **Validade:** sem data limite (ou estende por 6 meses pra começar)
8. **Limite de uso:** sem limite (ou 10.000 — alto)
9. **Limite por comprador:** 1 (evita abuso)
10. Salvar

Teste: abra o link de checkout em janela anônima → adicione `?off=CUPOM50` → confere se mostra `R$ 4,95`.

---

## Parte 3 — Verificar o cupom **SEGUIDOR80** (80% off na Trilha)

Se ainda não existe na Trilha, cria igual ao acima:

1. Hotmart → produto **Trilha DEVOPSRAIZ** (ID 7537240) → "Cupons"
2. "Criar novo cupom"
3. **Código:** `SEGUIDOR80`
4. **Tipo:** Porcentagem
5. **Valor:** `80%`
6. **Validade:** sem data limite
7. **Limite de uso:** ilimitado
8. **Limite por comprador:** 1
9. Salvar

Teste: abre `https://pay.hotmart.com/S105313699A?off=SEGUIDOR80` → confere `R$ 39,99`.

---

## Parte 4 — Atualizar links nos shorts

Depois de criar o produto, pega o link de checkout do PDF de Apoio (algo como `https://pay.hotmart.com/XXXXXXXX`) e substitui no codigo:

```bash
# Edita o template do short pra usar o link real
sed -i 's|https://pay.hotmart.com/D105790254W?off=CUPOM50|https://pay.hotmart.com/XXXXXXXX?off=CUPOM50|g' \
  /c/Projetos/TR99/Produtos/comercial/marketing/roteiros/generate_30_aulas.py

# Regenera os 30 shorts e 30 IGs
cd /c/Projetos/TR99/Produtos/comercial/marketing/roteiros
python generate_30_aulas.py
```

Os 30 shorts e 30 IG posts ficam com o link real do PDF.

---

## Parte 5 — Auto-incluir o cupom no link

Hotmart permite incluir o cupom direto na URL via `?off=CUPOM50`. **Use sempre essa forma nos shorts/descrições**. Por que? Porque o seguidor não precisa lembrar de digitar — ele clica e já vê R$ 4,95.

| Link | Quando usar |
|---|---|
| `https://pay.hotmart.com/XXX` | Quando quer mostrar preço cheio |
| `https://pay.hotmart.com/XXX?off=CUPOM50` | Sempre nos shorts/bio (já desconto aplicado) |

---

## Parte 6 — Testar fluxo de venda end-to-end

Antes de divulgar:

1. Abre **janela anônima** → clica no link com cupom → confere preço R$ 4,95
2. Compra com **cartão real** (você mesmo, depois pede reembolso ou usa Pix)
3. Confere que o email de entrega chegou com os 30 PDFs anexados
4. Abre 1 PDF aleatório, confere se abre limpo
5. Pede reembolso (se foi com cartão) — Hotmart tem 7 dias garantidos

---

## Parte 7 — Acompanhar vendas e ajustar

**KPIs pra primeiros 30 dias:**

| Métrica | Meta-mínima | Ótima |
|---|---|---|
| CTR do short → link bio | 3% | 8% |
| Conversão link → checkout | 5% | 15% |
| Conversão checkout → compra | 25% | 40% |
| Ticket médio | R$ 4,95 | R$ 4,95 (PDF) ou R$ 39,99 (Trilha upsell) |
| Reembolso | < 5% | < 2% |

**Onde acompanha:** Hotmart Dashboard → Relatórios → Vendas. Por cupom: filtra por `CUPOM50` e `SEGUIDOR80`.

---

## Parte 8 — Bumps e upsells (opcional)

Depois de o funil rodar 30 dias, considera:

1. **Order bump no checkout do PDF**: oferece a Trilha completa por R$ 39,99 no momento da compra do PDF
2. **Pacote 30 PDFs**: vende todos juntos por R$ 49,90 (5x cada, ou ~16% de desconto sobre comprar separado)
3. **PDF Pro**: versão expandida com videoaulas curtas (5 min) por R$ 19,90 com cupom PRO50

Mas isso fica pra depois dos primeiros 30 dias de tração.

---

## Resumo executivo: do zero ao funil rodando

| Passo | Tempo | Quem faz |
|---|---|---|
| 1. Criar produto PDF de Apoio + upload dos 30 PDFs | 30 min | VOCÊ no Hotmart |
| 2. Criar cupom CUPOM50 (50% off PDF) | 5 min | VOCÊ no Hotmart |
| 3. Confirmar cupom SEGUIDOR80 (80% off Trilha) | 5 min | VOCÊ no Hotmart |
| 4. Pegar link checkout com cupom e atualizar generate_30_aulas.py | 5 min | VOCÊ no editor |
| 5. Regerar 30 shorts e 30 IGs | 1 min | CLAUDE / terminal |
| 6. Testar end-to-end com janela anônima | 10 min | VOCÊ |
| 7. Ativar cron diário (publish-shorts-daily.yml) | 1 min | VOCÊ no GitHub Actions |

**Total: ~1 hora pra colocar o funil completo no ar.**

Tira-dúvidas operacional: chama no WhatsApp (11) 96482-3126 que eu ajudo a configurar passo-a-passo.
