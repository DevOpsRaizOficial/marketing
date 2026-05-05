# Setup Meta Pixel no Hotmart — DEVOPSRAIZ

Necessário pra:
- Tracking de conversões nos R$300/mês de ads
- Retargeting (Campanha 3)
- Otimização do algoritmo Meta com dados reais (Custom Conversion)

## Passo 1 — Criar Pixel no Meta

1. Acessa [business.facebook.com/events_manager](https://business.facebook.com/events_manager)
2. Clica em **"Conectar fontes de dados"** → **"Web"** → **"Meta Pixel"**
3. Configura:
   - Nome: **DevOpsRaiz Pixel**
   - URL do site: `go.hotmart.com/S105313699A`
4. Anota o **Pixel ID** que aparece (formato: 16 dígitos numéricos, ex: `1234567890123456`)

## Passo 2 — Instalar no Hotmart

Hotmart aceita pixel terceiro de 2 formas. Use a Opção A.

### Opção A — Via Pixels & Tags do Hotmart (recomendado)

1. Hotmart → **Produto > Trilha DEVOPSRAIZ > Configurações > Pixels e Tags**
2. Clica em **"+ Adicionar pixel"** → escolhe **"Facebook"** (ou "Meta")
3. Cola o **Pixel ID** (só os 16 dígitos)
4. Eventos a ativar:
   - ☑ **PageView** (visita na página de vendas)
   - ☑ **InitiateCheckout** (clicou em "Comprar agora")
   - ☑ **Purchase** (compra completada — Hotmart envia automaticamente)
5. Salva

> Hotmart já injeta o pixel nas páginas dele (sales page + checkout + obrigado). Não precisa colar código.

### Opção B — Tag Manager terceiro (avançado, só se usar GTM)

Se você tem Google Tag Manager, pode incluir o snippet abaixo num GTM container. **Mas pra Hotmart a Opção A já cobre 100%.**

```html
<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'SEU_PIXEL_ID_AQUI');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=SEU_PIXEL_ID_AQUI&ev=PageView&noscript=1"/></noscript>
<!-- End Meta Pixel -->
```

> Substitua `SEU_PIXEL_ID_AQUI` pelo ID real do seu pixel.

## Passo 3 — Verificar funcionamento

### 3.1 — Instala extensão **Meta Pixel Helper** no Chrome
- [Link da Web Store](https://chrome.google.com/webstore/detail/meta-pixel-helper/fdgfkebogiimcoedlicjlajpkdmockpc)

### 3.2 — Abre a página de vendas em aba anônima
- URL: `https://go.hotmart.com/S105313699A?dp=1`

### 3.3 — Verifica eventos no Pixel Helper
Esperado:
- ✅ Pixel **DevOpsRaiz Pixel** detected
- ✅ Event: **PageView** disparou
- ✅ Status: **Successful**

Se não aparecer:
- Aguarda 5 minutos (cache da Hotmart)
- Limpa cookies e tenta de novo
- Verifica se o ID está correto (sem espaços, só números)

### 3.4 — Verifica `InitiateCheckout`
- Clica em "Comprar agora" na página de vendas
- No Pixel Helper, esperado: novo evento **InitiateCheckout** disparou

### 3.5 — Verifica `Purchase` (depois da 1ª venda real)
- Após você fizer 1 compra teste OU 1 venda real chegar
- Vai em **business.facebook.com/events_manager** > Eventos
- Aparece **Purchase** com valor monetário

## Passo 4 — Configurar Custom Conversions (Opcional, recomendado)

No Events Manager → **Conversões personalizadas** → **+ Criar**:

### Conversão 1 — Lead capturado
- Origem: ManyChat (via Zapier webhook)
- Categoria: Lead
- Trigger: Email captured
- Valor: R$0 (lead, não venda)

### Conversão 2 — Compra Trilha
- Origem: Pixel (já vem do Hotmart)
- Categoria: Purchase
- Trigger: Purchase event
- Valor: dinâmico (Hotmart envia o valor)

## Passo 5 — Configurar evento prioritário (CAPI)

**Evento prioritário (iOS 14.5+ compliance):**
1. Events Manager → Configurações de Web → **Configurações Agregadas de Mensuração de Eventos**
2. Adiciona:
   - **Posição 1**: Purchase (mais valioso)
   - **Posição 2**: InitiateCheckout
   - **Posição 3**: Lead
   - **Posição 4-8**: PageView, ViewContent, etc

Isso garante que mesmo usuários iOS sem opt-in tracking você capture a conversão Purchase.

## Resultado esperado após 7 dias

Com pixel funcionando + R$10/dia em Campanha 1 (tráfego):

| Métrica | Meta saudável | Bandeira |
|---|---|---|
| PageViews trackados/dia | 5-15 | 🟢 |
| InitiateCheckouts/semana | 1-3 | 🟢 |
| Purchases/mês | 1-3 | 🟢 |
| Eventos rejeitados | < 5% | 🟢 |

## Bonus — Catálogo de eventos do Hotmart

Pra referência, eventos que Hotmart envia automaticamente quando o pixel está conectado:

| Evento Meta | Quando dispara |
|---|---|
| PageView | Visita na página de vendas |
| ViewContent | Carregou detalhes do produto |
| InitiateCheckout | Clicou em "Comprar agora" |
| AddPaymentInfo | Inseriu dados pagamento |
| Purchase | Pagamento aprovado |

Pixel Helper deveria detectar todos esses durante uma sessão completa (de página de vendas até compra).
