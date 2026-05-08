"""
PDF pos-compra — DEVOPSRAIZ
"Guia de Execucao: Pre-requisitos e Setup pra rodar os 15 Prompts"

Distribuido como conteudo extra do produto Hotmart 7696164
(area de membros). Quem comprar recebe automaticamente.
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, Table, TableStyle,
    Frame, PageTemplate, BaseDocTemplate, KeepTogether,
)

OUT = Path("/sessions/sweet-friendly-maxwell/mnt/marketing/lead-magnets/guia-execucao-prompts.pdf")

DARK_BG = HexColor("#020617")
DARK_2 = HexColor("#0F172A")
SLATE = HexColor("#1E293B")
LIGHT = HexColor("#E2E8F0")
MID = HexColor("#94A3B8")
ORANGE = HexColor("#F97316")
GREEN = HexColor("#10B981")
RED = HexColor("#EF4444")
YELLOW = HexColor("#F59E0B")
BLUE = HexColor("#3B82F6")
PURPLE = HexColor("#A855F7")
TEAL = HexColor("#06B6D4")

W, H = A4


def page_template_dark(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(DARK_BG)
    canvas_obj.rect(0, 0, W, H, fill=1, stroke=0)
    canvas_obj.setFillColor(GREEN)
    canvas_obj.rect(0, H - 6, W, 6, fill=1, stroke=0)
    canvas_obj.setFillColor(DARK_2)
    canvas_obj.rect(0, 0, W, 30, fill=1, stroke=0)
    canvas_obj.setFillColor(GREEN)
    canvas_obj.rect(0, 30, W, 2, fill=1, stroke=0)
    canvas_obj.setFillColor(LIGHT)
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.drawString(40, 12, "DEVOPSRAIZ · Guia de Execucao Pos-compra")
    page_num = canvas_obj.getPageNumber()
    canvas_obj.setFillColor(MID)
    canvas_obj.drawRightString(W - 40, 12, f"pag. {page_num}")
    canvas_obj.restoreState()


styles = getSampleStyleSheet()
S = {
    "h1": ParagraphStyle("h1", parent=styles["Title"],
        textColor=white, fontSize=32, leading=38,
        alignment=TA_LEFT, spaceAfter=10, fontName="Helvetica-Bold"),
    "h2": ParagraphStyle("h2", parent=styles["Heading1"],
        textColor=GREEN, fontSize=22, leading=28,
        alignment=TA_LEFT, spaceAfter=12, fontName="Helvetica-Bold"),
    "h3": ParagraphStyle("h3", parent=styles["Heading2"],
        textColor=white, fontSize=15, leading=20,
        alignment=TA_LEFT, spaceAfter=6, fontName="Helvetica-Bold"),
    "body": ParagraphStyle("body", parent=styles["Normal"],
        textColor=LIGHT, fontSize=11, leading=16,
        alignment=TA_LEFT, spaceAfter=8, fontName="Helvetica"),
    "bodyJ": ParagraphStyle("bodyJ", parent=styles["Normal"],
        textColor=LIGHT, fontSize=11, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=8, fontName="Helvetica"),
    "small": ParagraphStyle("small", parent=styles["Normal"],
        textColor=MID, fontSize=9, leading=12,
        fontName="Helvetica"),
    "code": ParagraphStyle("code", parent=styles["Code"],
        textColor=GREEN, fontSize=9, leading=13,
        fontName="Courier", backColor=DARK_2,
        leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=8,
        borderPadding=8),
}


def step_card(num, titulo, descr, comandos, color_hex):
    color = HexColor(color_hex)
    header = Table(
        [[Paragraph(f"<font color='white'><b>{num}</b></font>", S["h2"]),
          Paragraph(f"<font color='white'><b>{titulo}</b></font>", S["h3"])]],
        colWidths=[1.2 * cm, 14.3 * cm],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (1, 0), (1, 0), DARK_2),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    blocks = [header, Spacer(1, 4)]
    blocks.append(Paragraph(descr, S["body"]))
    if comandos:
        blocks.append(Paragraph(f"<font name='Courier'>{comandos}</font>", S["code"]))
    blocks.append(Spacer(1, 8))
    return KeepTogether(blocks)


story = []

# ----- PG 1 - COVER -----
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("Voce comprou.", S["h1"]))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    '<font color="#10B981">Agora e so executar.</font>', S["h1"]))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "Esse guia te leva do zero ate sua primeira automacao rodando "
    "no Instagram em menos de 1 hora.",
    ParagraphStyle("sub", parent=S["body"], fontSize=14, textColor=LIGHT, leading=20)))
story.append(Spacer(1, 1.5 * cm))

dica_capa = Table([[Paragraph(
    "<b>Importante:</b> Esse PDF complementa o "
    "<b>'Prompts de Automacao IA'</b> que voce recebeu. "
    "La voce tem os 15 prompts. Aqui voce tem o passo-a-passo "
    "pra rodar cada um.",
    ParagraphStyle("dica", parent=S["body"], textColor=DARK_BG, fontSize=10, leading=14))]],
    colWidths=[16 * cm])
dica_capa.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), YELLOW),
    ("TOPPADDING", (0, 0), (-1, -1), 12),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
]))
story.append(dica_capa)

story.append(Spacer(1, 2 * cm))

story.append(Paragraph(
    "<b>DEVOPSRAIZ</b><br/>Tiago Alves da Rocha<br/>"
    "Suporte: WhatsApp (11) 96482-3126",
    ParagraphStyle("auth", parent=S["body"], fontSize=11, textColor=MID, leading=16)))

story.append(PageBreak())

# ----- PG 2 - PRE-REQUISITOS -----
story.append(Paragraph("Pre-requisitos: o que voce precisa", S["h2"]))
story.append(Paragraph(
    "Antes de comecar, garante que tem essas 4 contas. Tudo gratuito ou ja deve ter:",
    S["bodyJ"]))
story.append(Spacer(1, 8))

prereq = [
    ("CLAUDE", "claude.ai", "Free serve. Plano Pro (USD 20/mes) "
     "se quiser conversas longas e contexto maior.", "#10B981"),
    ("CHATGPT", "chat.openai.com", "Free serve pra texto. Pra gerar imagens "
     "(slide capas) precisa do ChatGPT Plus (USD 20/mes - DALL-E incluido).", "#A855F7"),
    ("MANYCHAT", "manychat.com", "Free pra ate 1.000 contatos. Pro (USD 15/mes) "
     "pra automacao avancada e email follow-up.", "#F97316"),
    ("INSTAGRAM", "Conta Business", "OBRIGATORIO ser Business ou Creator. "
     "Conectar a uma Pagina do Facebook. Sem isso, ManyChat nao integra.", "#F59E0B"),
]
for nome, link, desc, cor in prereq:
    color = HexColor(cor)
    t = Table(
        [[Paragraph(f"<font color='white'><b>{nome}</b></font><br/>"
                    f"<font color='white' size='8'>{link}</font>", S["body"]),
          Paragraph(f"<font color='white'>{desc}</font>", S["body"])]],
        colWidths=[3.5 * cm, 12 * cm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (1, 0), (1, 0), DARK_2),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 14),
        ("RIGHTPADDING", (1, 0), (1, 0), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

story.append(Spacer(1, 14))
story.append(Paragraph(
    "<b>Dica do Tiago:</b> se vai testar com seu perfil pessoal antes "
    "de migrar pra Business, faz isso primeiro. Conta Pessoal nao funciona "
    "com a API do Meta. Migra antes pra evitar retrabalho.",
    ParagraphStyle("dica2", parent=S["body"], textColor=YELLOW, fontSize=10)))

story.append(PageBreak())

# ----- PG 3 - SETUP CLAUDE -----
story.append(Paragraph("Setup Claude (5 min)", S["h2"]))

story.append(step_card("01", "Cria conta gratis em claude.ai",
    "Login com email + senha ou Google. Se ja tem, login normal.",
    "Tip: ative MFA em Settings &gt; Security pra proteger a conta.",
    "#10B981"))

story.append(step_card("02", "Cria nova conversa pra cada prompt",
    "NUNCA cole varios prompts numa conversa so. Cada um tem contexto diferente. "
    "Botao 'New chat' no canto superior esquerdo.",
    "",
    "#10B981"))

story.append(step_card("03", "Cole o prompt + suas variaveis",
    "Os prompts no PDF principal tem [VARIAVEIS] entre colchetes. "
    "Substitua antes de mandar pro Claude. Ex: [SEU NICHO] vira 'Cloud Computing PT-BR'.",
    "",
    "#10B981"))

story.append(step_card("04", "Itere com follow-ups",
    "Claude responde melhor com refinamento. Depois da primeira resposta, "
    "faca pedidos do tipo: 'Reescreve mais direto', 'Da 3 alternativas', "
    "'Adiciona exemplo concreto'.",
    "",
    "#10B981"))

story.append(step_card("05", "Salve as melhores respostas",
    "Crie um doc Notion ou Google Docs e cole tudo que Claude gerou de bom. "
    "Vai virar seu acervo pessoal de copy + estrategia.",
    "",
    "#10B981"))

story.append(PageBreak())

# ----- PG 4 - SETUP CHATGPT -----
story.append(Paragraph("Setup ChatGPT (5 min)", S["h2"]))

story.append(step_card("06", "Cria conta em chat.openai.com",
    "Mesmo padrao do Claude. Se quer usar DALL-E pra gerar imagens "
    "(prompts 8 do PDF principal), precisa do plano Plus (USD 20/mes).",
    "",
    "#A855F7"))

story.append(step_card("07", "Use GPT-4o pra texto e GPT-4 Image pra visual",
    "GPT-4o (mini ou full) pra refinamento de copy. "
    "Pra imagens, escolhe 'Image' no menu ou ativa DALL-E. "
    "Imagens custam ~USD 0.08 cada na API ou ilimitadas no Plus.",
    "",
    "#A855F7"))

story.append(step_card("08", "Resolucao das imagens DALL-E",
    "Por padrao, DALL-E gera 1024x1024. Pra Instagram carrossel (1080x1350), "
    "pede explicito: 'Imagem em formato 9:16 ou 1080x1350px'. "
    "Se nao sair certo, peca pra regerar com aspect_ratio diferente.",
    "",
    "#A855F7"))

story.append(step_card("09", "Faz Claude e ChatGPT trabalharem juntos",
    "Fluxo recomendado: <b>Claude organiza</b> a estrutura -&gt; "
    "<b>ChatGPT refina</b> o texto magnetico -&gt; "
    "<b>Claude valida</b> a versao final. Cada IA e melhor em uma parte.",
    "",
    "#A855F7"))

story.append(step_card("10", "Salve seu prompt template no ChatGPT",
    "Use 'Custom GPTs' (Plus) pra criar um GPT especifico do seu nicho "
    "que ja sabe seu tom de voz. Cola os 5 prompts do ChatGPT do PDF principal "
    "como Knowledge File.",
    "",
    "#A855F7"))

story.append(PageBreak())

# ----- PG 5 - SETUP MANYCHAT -----
story.append(Paragraph("Setup ManyChat (15 min)", S["h2"]))

story.append(step_card("11", "Cria conta em app.manychat.com",
    "Login com Facebook (precisa ja ter ligacao Insta -&gt; FB Page). "
    "Plano Free serve pra comecar (1.000 contatos).",
    "",
    "#F97316"))

story.append(step_card("12", "Conecta seu Instagram Business",
    "Settings &gt; Channels &gt; Instagram. Autoriza permissoes "
    "(messaging_send, comments_read). Se nao aparecer Instagram, "
    "sua conta nao esta como Business -- migra primeiro.",
    "",
    "#F97316"))

story.append(step_card("13", "Hospede o PDF que vai entregar",
    "Opcoes (em ordem de robustez): "
    "<b>1. Hotmart</b> (se vai vender) - URL automatica, profissional. "
    "<b>2. Google Drive publico</b> - URL formato <font name='Courier'>drive.google.com/uc?export=download&amp;id=ID</font>. "
    "<b>3. ManyChat Files</b> (max 5MB) - upload direto em Settings &gt; Files. "
    "<b>4. GitHub raw</b> - se PDF e publico, OK pra teste; pode ter inconsistencia em mobile.",
    "",
    "#F97316"))

story.append(step_card("14", "Crie a Quick Automation 'Comments to DM'",
    "Automation &gt; Templates &gt; 'Enviar links automaticamente por DM "
    "a partir dos comentarios'. Configure o trigger no post especifico OU "
    "em qualquer post (se quer cobertura total).",
    "",
    "#F97316"))

story.append(step_card("15", "Use o prompt #11-15 do PDF principal",
    "Cada um cobre uma parte: keyword, captura email, tag, link, sequencia "
    "de email. Implementa um por um, testa em conta secundaria, refina.",
    "",
    "#F97316"))

story.append(PageBreak())

# ----- PG 6 - ORDEM RECOMENDADA -----
story.append(Paragraph("Ordem recomendada de execucao", S["h2"]))
story.append(Paragraph(
    "Os 15 prompts no PDF principal estao agrupados em 3 fases. "
    "Execute em ordem pra construir uma maquina de leads completa em ~3h:",
    S["bodyJ"]))
story.append(Spacer(1, 12))

fases = [
    ("FASE 1 - Estrategia (45 min)",
     "Use Claude pra definir lead magnet (P1), montar esqueleto do PDF (P2), "
     "criar passo-a-passo ManyChat (P3) e sequencia de emails (P4). "
     "Resultado: voce tem CLAREZA do que vai entregar e como capturar.",
     GREEN),
    ("FASE 2 - Producao (60 min)",
     "Use ChatGPT pra criar 10 hooks (P6), legenda completa (P7), "
     "imagem capa do carrossel via DALL-E (P8) e variantes A/B do CTA (P9). "
     "Resultado: voce tem CONTEUDO pronto pra publicar.",
     PURPLE),
    ("FASE 3 - Automacao (90 min)",
     "Use ManyChat pra setup do trigger (P11), captura de email (P12), "
     "tag de segmentacao (P13), link de entrega (P14) e email drip (P15). "
     "Resultado: voce tem MAQUINA rodando 24/7.",
     ORANGE),
]
for nome, desc, cor in fases:
    t = Table(
        [[Paragraph(f"<font color='white'><b>{nome}</b></font>", S["h3"]),
          Paragraph(f"<font color='white'>{desc}</font>", S["body"])]],
        colWidths=[5.5 * cm, 10 * cm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), cor),
        ("BACKGROUND", (1, 0), (1, 0), DARK_2),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

story.append(Spacer(1, 14))
story.append(Paragraph(
    "Apos as 3 fases, monitore por 7 dias. Use o prompt P5 (analise de funil) "
    "pra cruzar metricas e decidir o que escalar.",
    S["bodyJ"]))

story.append(PageBreak())

# ----- PG 7 - TROUBLESHOOTING + SUPORTE -----
story.append(Paragraph("Travou? Suporte WhatsApp", S["h2"]))
story.append(Spacer(1, 12))

story.append(Paragraph("Problemas comuns e fixes rapidos", S["h3"]))
story.append(Spacer(1, 8))

problemas = [
    ("ManyChat nao conecta Instagram",
     "Sua conta nao e Business OU nao tem Page Facebook ligada. Migra primeiro.",
     RED),
    ("Trigger nao dispara em comentarios",
     "Verifica se a keyword esta como 'whole word' OU 'contains'. "
     "Tambem confirma que o post escolhido permite comentarios.",
     ORANGE),
    ("Link enviado mas pessoa nao consegue baixar",
     "In-app browser do Instagram falha com PDFs do GitHub raw. "
     "Use Hotmart, Google Drive direct download, ou anexa PDF direto no ManyChat.",
     YELLOW),
    ("DALL-E gera imagem feia",
     "Seja MAIS especifico no prompt: cor, estilo, composicao, mood. "
     "Pede 4 variacoes (DALL-E 3 gera 1 por vez, peca em 4 chamadas).",
     PURPLE),
]
for prob, fix, cor in problemas:
    t = Table(
        [[Paragraph(f"<font color='white'><b>{prob}</b></font><br/>"
                    f"<font color='white' size='10'>{fix}</font>",
                    ParagraphStyle("p", parent=S["body"], leading=14))]],
        colWidths=[15.5 * cm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEBEFORE", (0, 0), (0, -1), 4, cor),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

story.append(Spacer(1, 24))

# WhatsApp suporte destacado
suporte = Table([[Paragraph(
    '<font color="white" size="20"><b>Suporte direto comigo</b></font><br/><br/>'
    '<font color="white" size="14">Se travar em qualquer step, me chama no WhatsApp:</font><br/><br/>'
    '<font color="white" size="22"><b>(11) 96482-3126</b></font><br/>'
    '<font color="white" size="11">wa.me/5511964823126</font><br/><br/>'
    '<font color="white" size="11">Atendo de seg a sex, 9h as 18h BRT. '
    'Resposta em 1 dia util.</font>',
    ParagraphStyle("sup", parent=S["body"], alignment=TA_CENTER, leading=20, textColor=white))]],
    colWidths=[16 * cm])
suporte.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), GREEN),
    ("TOPPADDING", (0, 0), (-1, -1), 22),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
]))
story.append(suporte)

story.append(Spacer(1, 18))

# CTA Trilha
trilha = Table([[Paragraph(
    '<font color="white" size="14"><b>Quer ir alem? Trilha DEVOPSRAIZ completa</b></font><br/><br/>'
    '<font color="white" size="11">6 ebooks integrados de Cloud, K8s, IA Avancada, SaaS, '
    'Observabilidade e Security. Use cupom <b>FUNDADOR50</b> = 50% off (so pros 100 primeiros que entram pelo PDF).</font><br/><br/>'
    '<font color="#10B981" size="11">go.hotmart.com/S105313699A</font>',
    ParagraphStyle("trilha", parent=S["body"], alignment=TA_CENTER, leading=16))]],
    colWidths=[16 * cm])
trilha.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("TOPPADDING", (0, 0), (-1, -1), 16),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
]))
story.append(trilha)

# ==============================================================================
# Build
# ==============================================================================
doc = BaseDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=2.5 * cm, rightMargin=2.5 * cm,
    topMargin=1.8 * cm, bottomMargin=1.5 * cm,
    title="Guia de Execucao - Pos-compra DEVOPSRAIZ",
    author="Tiago Alves da Rocha",
    subject="Conteudo extra do produto Prompts de Automacao IA",
)

frame = Frame(2.5 * cm, 1.5 * cm, W - 5 * cm, H - 3.3 * cm,
    leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
template = PageTemplate(id="dark", frames=[frame], onPage=page_template_dark)
doc.addPageTemplates([template])

doc.build(story)
print(f"OK: {OUT}")
print(f"Tamanho: {OUT.stat().st_size / 1024:.1f} KB")
