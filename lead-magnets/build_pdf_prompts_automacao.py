"""
Lead magnet PDF — DEVOPSRAIZ
"Prompts de Automação Diária com Claude + ChatGPT + ManyChat"

Distribuído via ManyChat keyword EU QUERO no Instagram (carrosséis das quintas).
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Frame, PageTemplate, BaseDocTemplate, KeepTogether,
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

OUT = Path("/sessions/sweet-friendly-maxwell/mnt/marketing/lead-magnets/prompts-automacao-ia-manychat.pdf")

# Paleta neon style (combinando com os carrosseis)
DARK_BG = HexColor("#020617")
DARK_2 = HexColor("#0F172A")
SLATE = HexColor("#1E293B")
LIGHT = HexColor("#E2E8F0")
MID = HexColor("#94A3B8")
ORANGE = HexColor("#F97316")
GREEN_NEON = HexColor("#10B981")
RED = HexColor("#EF4444")
YELLOW = HexColor("#F59E0B")
BLUE = HexColor("#3B82F6")
PURPLE = HexColor("#A855F7")
TEAL = HexColor("#06B6D4")

W, H = A4


def page_template_dark(canvas_obj, doc):
    """Background escuro + footer."""
    canvas_obj.saveState()
    canvas_obj.setFillColor(DARK_BG)
    canvas_obj.rect(0, 0, W, H, fill=1, stroke=0)
    canvas_obj.setFillColor(GREEN_NEON)
    canvas_obj.rect(0, H - 6, W, 6, fill=1, stroke=0)
    canvas_obj.setFillColor(DARK_2)
    canvas_obj.rect(0, 0, W, 30, fill=1, stroke=0)
    canvas_obj.setFillColor(GREEN_NEON)
    canvas_obj.rect(0, 30, W, 2, fill=1, stroke=0)
    canvas_obj.setFillColor(LIGHT)
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.drawString(40, 12, "@devopsraiz_oficial · Automação com IA")
    page_num = canvas_obj.getPageNumber()
    canvas_obj.setFillColor(MID)
    canvas_obj.drawRightString(W - 40, 12, f"pag. {page_num}")
    canvas_obj.restoreState()


styles = getSampleStyleSheet()

S = {
    "h1": ParagraphStyle("h1", parent=styles["Title"],
        textColor=white, fontSize=34, leading=40,
        alignment=TA_LEFT, spaceAfter=10, fontName="Helvetica-Bold"),
    "h2": ParagraphStyle("h2", parent=styles["Heading1"],
        textColor=GREEN_NEON, fontSize=22, leading=28,
        alignment=TA_LEFT, spaceAfter=12, fontName="Helvetica-Bold"),
    "h3": ParagraphStyle("h3", parent=styles["Heading2"],
        textColor=white, fontSize=16, leading=22,
        alignment=TA_LEFT, spaceAfter=6, fontName="Helvetica-Bold"),
    "body": ParagraphStyle("body", parent=styles["Normal"],
        textColor=LIGHT, fontSize=11, leading=16,
        alignment=TA_LEFT, spaceAfter=8, fontName="Helvetica"),
    "bodyJ": ParagraphStyle("bodyJ", parent=styles["Normal"],
        textColor=LIGHT, fontSize=11, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=8, fontName="Helvetica"),
    "code": ParagraphStyle("code", parent=styles["Code"],
        textColor=GREEN_NEON, fontSize=9, leading=13,
        fontName="Courier", backColor=DARK_2,
        leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=8,
        borderPadding=8),
    "small": ParagraphStyle("small", parent=styles["Normal"],
        textColor=MID, fontSize=9, leading=12,
        fontName="Helvetica"),
}


def prompt_card(num, titulo, descr, prompt, color_hex):
    """Card com prompt: número colorido + título + descrição + prompt em mono."""
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

    blocks = [header]
    blocks.append(Spacer(1, 4))
    blocks.append(Paragraph(f"<b>Quando usar:</b> {descr}", S["body"]))
    blocks.append(Paragraph(f"<font name='Courier'>{prompt}</font>", S["code"]))
    blocks.append(Spacer(1, 10))
    return KeepTogether(blocks)


story = []

# ----- PG 1 - COVER -----
story.append(Spacer(1, 5 * cm))
story.append(Paragraph("Prompts de", S["h1"]))
story.append(Paragraph(
    '<font color="#10B981">Automação Diária</font>', S["h1"]))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph(
    '<font color="#A855F7">com Claude + ChatGPT</font>', S["h1"]))
story.append(Paragraph(
    '<font color="#A855F7">+ ManyChat</font>', S["h1"]))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "15 prompts prontos pra você criar sua máquina de leads no Instagram em 30 minutos.",
    ParagraphStyle("sub", parent=S["body"], fontSize=14, textColor=LIGHT, leading=20)))
story.append(Spacer(1, 4 * cm))
story.append(Paragraph(
    "<b>DEVOPSRAIZ</b><br/>Tiago Alves da Rocha<br/>"
    "Recorte do Playbook IA + Automação",
    ParagraphStyle("auth", parent=S["body"], fontSize=11, textColor=MID, leading=16)))
story.append(PageBreak())

# ----- PG 2 - PLAYBOOK -----
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("O Playbook em 3 papéis", S["h2"]))
story.append(Paragraph(
    "Cada IA tem um superpoder diferente. Use os 3 juntos e você multiplica produtividade:",
    S["bodyJ"]))
story.append(Spacer(1, 8))

playbook = [
    ("CLAUDE", "Organiza estratégia. É melhor pra raciocínio longo, contexto enorme, e checagem de qualidade. "
     "Use pra planejar fluxos, escrever scripts Python e definir arquitetura.", "#10B981"),
    ("CHATGPT", "Refina copy e cria visuais. É melhor pra textos curtos magnéticos, variações de "
     "headlines e geração de imagens com DALL-E. Use pra polir legendas e gerar criativos.", "#A855F7"),
    ("MANYCHAT", "Executa o flow no Instagram. É melhor pra capturar leads dos comentários, "
     "responder em DM com um PDF, qualificar com email e marcar tags pra retargeting.", "#F97316"),
]

for nome, desc, cor in playbook:
    color = HexColor(cor)
    t = Table(
        [[Paragraph(f"<font color='white'><b>{nome}</b></font>", S["h2"]),
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
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

story.append(Spacer(1, 18))
dica = Table([[Paragraph(
    "<b>Dica do Tiago:</b> NUNCA use 1 IA pra fazer tudo. Cada uma tem sua força. "
    "Eu jogo o problema no Claude, peço pra ele me dar o esqueleto. "
    "Levo o esqueleto pro ChatGPT pra ele me dar 5 variações magnéticas. "
    "Configuro o vencedor no ManyChat. Pronto.",
    ParagraphStyle("dica", parent=S["body"], textColor=DARK_BG, fontSize=10, leading=14))]],
    colWidths=[16 * cm])
dica.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), YELLOW),
    ("TOPPADDING", (0, 0), (-1, -1), 12),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
]))
story.append(dica)
story.append(PageBreak())

# ----- PG 3 - PROMPTS CLAUDE (estratégia) -----
story.append(Paragraph("5 Prompts pro Claude", S["h2"]))
story.append(Paragraph("<b>Use Claude pra:</b> estratégia, arquitetura, código.",
    ParagraphStyle("subt", parent=S["body"], textColor=GREEN_NEON, fontSize=12)))
story.append(Spacer(1, 8))

story.append(prompt_card("01", "Definir o lead magnet ideal",
    "Antes de criar qualquer flow, defina QUE PDF você vai entregar.",
    "Eu sou criador de conteúdo no nicho [SEU NICHO]. Meu público é [PERFIL]. "
    "Quero criar um lead magnet (PDF gratuito) que resolve uma dor específica deles. "
    "Me dá 5 ideias de PDF, com título magnético + esqueleto de 6 páginas + por que cada um capturaria leads.",
    "#10B981"))

story.append(prompt_card("02", "Esqueleto do PDF (6 páginas)",
    "Depois de escolher a ideia, peça o esqueleto detalhado.",
    "Pra o lead magnet escolhido [TÍTULO], crie um esqueleto detalhado de 6 páginas. "
    "Pg 1 capa, Pg 2 intro, Pg 3-5 conteúdo principal (3 dores + 3 fixes cada), Pg 6 CTA. "
    "Pra cada página me dá: título, subtítulo, 3-5 bullets de conteúdo, e elemento visual sugerido.",
    "#10B981"))

story.append(prompt_card("03", "Setup ManyChat passo-a-passo",
    "Quer um guia técnico do flow? Claude faz bem.",
    "Crie um passo-a-passo COMPLETO de como configurar uma keyword no ManyChat (versão atual) que: "
    "trigga em comentário do meu post X, "
    "responde no comentário público, "
    "manda DM com captura de email obrigatório, "
    "entrega o link de download do PDF, "
    "marca tag 'lead_X' no contato. Inclua o que clicar em cada tela e textos prontos pra copy-paste.",
    "#10B981"))

story.append(prompt_card("04", "Sequência de 7 emails pós-lead",
    "Lead capturou. Agora você precisa nutrir e converter.",
    "Crie uma sequência de 7 emails de nurturing, espaçados ao longo de 14 dias, "
    "pra leads que baixaram meu PDF [TÍTULO]. Email 1 entrega o PDF + boas-vindas. "
    "Emails 2-4 educam com casos. Email 5 oferece o produto principal com cupom. "
    "Email 6 reforça urgência. Email 7 último convite. Pra cada email: assunto magnético + corpo de 200-300 palavras.",
    "#10B981"))

story.append(prompt_card("05", "Análise de funil",
    "Toda semana, peça pro Claude analisar suas métricas.",
    "Analise meu funil dos últimos 7 dias e me dê recomendações: "
    "Visitas no link bio: [N] / Cliques no Hotmart: [N] / Vendas: [N] / Leads ManyChat: [N] / Open rate emails: [N%]. "
    "Identifique os 3 maiores gargalos do funil + sugira 3 mudanças cirúrgicas pra próxima semana.",
    "#10B981"))
story.append(PageBreak())

# ----- PG 4 - PROMPTS CHATGPT (copy) -----
story.append(Paragraph("5 Prompts pro ChatGPT", S["h2"]))
story.append(Paragraph("<b>Use ChatGPT pra:</b> copy magnético, headlines, criativos visuais.",
    ParagraphStyle("subt", parent=S["body"], textColor=PURPLE, fontSize=12)))
story.append(Spacer(1, 8))

story.append(prompt_card("06", "10 hooks magnéticos pro post",
    "Hook fraco = post que ninguém para de scrollar. Pede 10 e escolhe o melhor.",
    "Crie 10 hooks magnéticos pro slide 1 do meu carrossel sobre [TEMA]. "
    "Cada hook deve: ser uma pergunta provocativa, criar curiosidade, ter no máximo 8 palavras. "
    "Estilo: direto e callado. Exemplo de tom: 'Já viu seu pod assim?'. "
    "Inclua emoji só se realmente agregar.",
    "#A855F7"))

story.append(prompt_card("07", "Legenda completa 200-280 palavras",
    "Depois do carrossel pronto, gera a legenda otimizada.",
    "Escreve uma legenda de Instagram pra um carrossel sobre [TEMA] que cobre [3 pontos principais]. "
    "Estrutura: hook (1 frase magnética) + 3-5 bullets com emojis + CTA (comentar X pra receber Y) + 10 hashtags. "
    "Tom: direto, brasileiro, técnico mas acessível. NUNCA use 'genuinamente', 'incrivelmente' ou 'literalmente'.",
    "#A855F7"))

story.append(prompt_card("08", "Imagem capa carrossel via DALL-E",
    "Quer cover irresistível? DALL-E entrega.",
    "Cria uma imagem 1080x1350px estilo dark neon (cores: preto profundo + neon verde, roxo, laranja). "
    "Conteúdo: título grande de impacto '[TÍTULO]' + ilustração de [ELEMENTO VISUAL] + selo lateral 'Sugestão 1 - Slide 1/3'. "
    "Tipografia: bold marcante, hierarquia clara. Sem clichês de tech genéricos. Mood: profissional + cool.",
    "#A855F7"))

story.append(prompt_card("09", "Variações A/B do CTA",
    "1 CTA é chute. 5 CTAs é teste.",
    "Crie 5 variações de CTA pra final de carrossel sobre [TEMA] que pedem pro user comentar 'EU QUERO' "
    "no post pra receber um PDF gratuito. Cada CTA deve ter no máximo 2 frases. "
    "Variação 1: tom direto. 2: tom curioso. 3: tom urgência. 4: tom prova social. 5: tom oferta exclusiva. "
    "Sem clichês. Estilo brasileiro casual.",
    "#A855F7"))

story.append(prompt_card("10", "Script de Reel 30s",
    "Reel curto converte mais que carrossel longo se a abertura for forte.",
    "Crie um script de Reel de 30s sobre [TEMA TÉCNICO]. Estrutura: "
    "0-3s hook visual + frase de impacto (DEVE parar o scroll), "
    "3-20s conteúdo de valor (3 pontos) com texto na tela acompanhando a fala, "
    "20-25s CTA (comenta X pra receber Y), "
    "25-30s reforço visual + handle. "
    "Linguagem natural, falada, brasileira. Sem 'galera, beleza, vamos lá'.",
    "#A855F7"))
story.append(PageBreak())

# ----- PG 5 - PROMPTS MANYCHAT -----
story.append(Paragraph("5 Configurações no ManyChat", S["h2"]))
story.append(Paragraph("<b>Use ManyChat pra:</b> capturar e nutrir leads do Instagram.",
    ParagraphStyle("subt", parent=S["body"], textColor=ORANGE, fontSize=12)))
story.append(Spacer(1, 8))

story.append(prompt_card("11", "Keyword Trigger (DM + comentário)",
    "Configure o trigger duplo pra cobrir comentário público + DM.",
    "ManyChat → Quick Automations → 'Enviar links automaticamente por DM a partir dos comentários'. "
    "Keywords: PALAVRA1, palavra1, PALAVRA2 (lowercase + caps + variantes). "
    "Trigger on: comentário do post X + DM. "
    "Resposta pública: 'Mandei no DM 📨' (cria prova social).",
    "#F97316"))

story.append(prompt_card("12", "Captura de email obrigatória",
    "Email é o ativo. Sem captura, o lead some.",
    "Bloco 2 do flow: 'uma DM solicitando endereço de e-mail' (ON). "
    "Texto: 'Antes de te mandar, qual seu email? Quem entra na lista ganha cupom FUNDADOR 20% off.' "
    "Quick reply: 'pular' pros que não querem dar email mas ainda recebem o PDF. "
    "Save to field: Email (built-in).",
    "#F97316"))

story.append(prompt_card("13", "Tag de segmentação",
    "Lead capturado → tag → retargeting cirúrgico.",
    "Action depois da captura: Add tag 'lead_TEMA' + 'topic_X'. "
    "Custom field: data_captura = today. "
    "Beneficio: futuramente você dispara campanhas só pra quem tem essa tag específica, "
    "ou retarga via Meta Ads usando uma audiência customizada do ManyChat.",
    "#F97316"))

story.append(prompt_card("14", "Link de entrega do PDF",
    "Hospede o PDF público (não anexa direto no ManyChat — pesado).",
    "Bloco 3 do flow: 'Adicionar Um Link'. "
    "Texto do botão: 'Baixar PDF grátis'. "
    "Link: URL público do PDF (ex: GitHub raw URL, Google Drive público com /uc?export=download&id=, ou S3). "
    "Bonus: encurta com bit.ly pra trackear cliques.",
    "#F97316"))

story.append(prompt_card("15", "Sequence de 7 emails pós-lead",
    "ManyChat também faz email follow-up native (1k leads grátis).",
    "ManyChat → Automation → Sequence → criar 'Email Drip 7 dias'. "
    "Trigger: tag 'lead_X' adicionada. "
    "Cada step com delay (1d, 3d, 5d, 7d, 8d, 14d). "
    "Stop sequence se: lead clicar em link do produto OU descadastrar.",
    "#F97316"))
story.append(PageBreak())

# ----- PG 6 - CTA -----
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Aplicou? Mostra pra mim.", S["h2"]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Esse PDF é um recorte do meu Playbook completo. Se você aplicou pelo menos 5 desses prompts "
    "e construiu sua máquina de leads, me marca no @devopsraiz_oficial — adoro ver gente colocando em prática.",
    S["bodyJ"]))

story.append(Spacer(1, 14))

story.append(Paragraph("Próximo passo lógico", S["h3"]))
story.append(Paragraph(
    "A Trilha DEVOPSRAIZ tem 6 ebooks integrados que cobrem do zero a produção: "
    "Cloud, K8s, IA Avançada, SaaS multi-tenant, Observabilidade e Security. "
    "Tudo com código real em PT-BR.",
    S["bodyJ"]))

story.append(Spacer(1, 18))

cupom = Table([[Paragraph(
    '<font color="white" size="18"><b>CUPOM FUNDADOR · 20% OFF</b></font><br/><br/>'
    '<font color="white" size="11">Use <b>FUNDADOR20</b> no checkout do Hotmart. '
    'Válido só pros 100 primeiros que entram na lista.</font>',
    ParagraphStyle("cup", parent=S["body"], alignment=TA_CENTER, leading=18, textColor=white))]],
    colWidths=[16 * cm])
cupom.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), GREEN_NEON),
    ("TOPPADDING", (0, 0), (-1, -1), 18),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
]))
story.append(cupom)

story.append(Spacer(1, 16))

cta_link = Table([[Paragraph(
    '<font color="white" size="14"><b>Trilha completa &raquo;</b></font><br/>'
    '<font color="#10B981" size="11">go.hotmart.com/S105313699A</font>',
    ParagraphStyle("link", parent=S["body"], alignment=TA_CENTER, leading=18))]],
    colWidths=[16 * cm])
cta_link.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("TOPPADDING", (0, 0), (-1, -1), 14),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
]))
story.append(cta_link)

story.append(Spacer(1, 14))
story.append(Paragraph(
    "Me segue lá no <b><font color='#10B981'>@devopsraiz_oficial</font></b> pra mais conteúdo "
    "de IA + automação + Cloud em PT-BR.",
    ParagraphStyle("foot", parent=S["body"], alignment=TA_CENTER, textColor=LIGHT, leading=16)))


# ==============================================================================
# Build
# ==============================================================================
doc = BaseDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=2.5 * cm, rightMargin=2.5 * cm,
    topMargin=1.8 * cm, bottomMargin=1.5 * cm,
    title="Prompts de Automacao Diaria com Claude + ChatGPT + ManyChat",
    author="Tiago Alves da Rocha",
    subject="Lead magnet — DEVOPSRAIZ Playbook IA",
)

frame = Frame(2.5 * cm, 1.5 * cm, W - 5 * cm, H - 3.3 * cm,
    leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
template = PageTemplate(id="dark", frames=[frame], onPage=page_template_dark)
doc.addPageTemplates([template])

doc.build(story)
print(f"OK: {OUT}")
print(f"Tamanho: {OUT.stat().st_size / 1024:.1f} KB")
