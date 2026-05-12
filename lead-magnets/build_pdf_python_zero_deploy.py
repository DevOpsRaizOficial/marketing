"""
Lead magnet PDF — DEVOPSRAIZ
"Zero ao Deploy: sua primeira API Python publicada em 7 dias"

Ebook gratuito que entrega: conceitos de infra + Python + FastAPI + Docker
+ CI/CD + deploy real. Funil pra Trilha DEVOPSRAIZ paga (R$199,99 com
cupom SEGUIDOR80 = 80% off = R$39,99).

Distribuído via Instagram (@devopsraiz_oficial), ManyChat keyword PYTHON,
e Hotmart sales page como bônus.
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Frame, PageTemplate, BaseDocTemplate, KeepTogether, ListFlowable, ListItem,
)
from reportlab.pdfgen import canvas

# ==============================================================================
# Output path — usa caminho relativo ao script
# ==============================================================================
SCRIPT_DIR = Path(__file__).parent
OUT = SCRIPT_DIR / "ebook-gratuito-python-zero-deploy.pdf"

# ==============================================================================
# Paleta DevOpsRaiz (mesma da Trilha)
# ==============================================================================
DARK_BG = HexColor("#020617")
DARK_2 = HexColor("#0F172A")
SLATE = HexColor("#1E293B")
LIGHT = HexColor("#E2E8F0")
MID = HexColor("#94A3B8")
ORANGE = HexColor("#F97316")
RED = HexColor("#EF4444")
YELLOW = HexColor("#F59E0B")
GREEN = HexColor("#10B981")
BLUE = HexColor("#3B82F6")
PURPLE = HexColor("#A855F7")

W, H = A4  # 595 x 842 pts


# ==============================================================================
# Page templates
# ==============================================================================
def page_dark(canvas_obj, doc):
    """Background escuro + faixa laranja topo + footer."""
    canvas_obj.saveState()
    canvas_obj.setFillColor(DARK_BG)
    canvas_obj.rect(0, 0, W, H, fill=1, stroke=0)
    # Faixa orange topo
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, H - 6, W, 6, fill=1, stroke=0)
    # Footer
    canvas_obj.setFillColor(DARK_2)
    canvas_obj.rect(0, 0, W, 30, fill=1, stroke=0)
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, 30, W, 2, fill=1, stroke=0)
    canvas_obj.setFillColor(LIGHT)
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.drawString(40, 12, "@devopsraiz_oficial  ·  Trilha DEVOPSRAIZ")
    page_num = canvas_obj.getPageNumber()
    canvas_obj.setFillColor(MID)
    canvas_obj.drawRightString(W - 40, 12, f"pag. {page_num}")
    canvas_obj.restoreState()


def page_cover(canvas_obj, doc):
    """Capa: fundo escuro + bloco laranja gigante."""
    canvas_obj.saveState()
    canvas_obj.setFillColor(DARK_BG)
    canvas_obj.rect(0, 0, W, H, fill=1, stroke=0)
    # Bloco laranja lateral esquerdo
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, 0, 12, H, fill=1, stroke=0)
    # Faixa laranja topo
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, H - 6, W, 6, fill=1, stroke=0)
    # Footer
    canvas_obj.setFillColor(DARK_2)
    canvas_obj.rect(0, 0, W, 30, fill=1, stroke=0)
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, 30, W, 2, fill=1, stroke=0)
    canvas_obj.setFillColor(LIGHT)
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.drawString(40, 12, "@devopsraiz_oficial  ·  ebook gratuito")
    canvas_obj.setFillColor(MID)
    canvas_obj.drawRightString(W - 40, 12, "Tiago Alves da Rocha")
    canvas_obj.restoreState()


# ==============================================================================
# Estilos
# ==============================================================================
styles = getSampleStyleSheet()

S = {
    "h0": ParagraphStyle(
        "h0", parent=styles["Title"],
        textColor=white, fontSize=44, leading=50,
        alignment=TA_LEFT, spaceAfter=10, fontName="Helvetica-Bold",
    ),
    "h1": ParagraphStyle(
        "h1", parent=styles["Title"],
        textColor=white, fontSize=32, leading=38,
        alignment=TA_LEFT, spaceAfter=10, fontName="Helvetica-Bold",
    ),
    "h2": ParagraphStyle(
        "h2", parent=styles["Heading1"],
        textColor=ORANGE, fontSize=22, leading=28,
        alignment=TA_LEFT, spaceAfter=12, fontName="Helvetica-Bold",
    ),
    "h3": ParagraphStyle(
        "h3", parent=styles["Heading2"],
        textColor=white, fontSize=15, leading=20,
        alignment=TA_LEFT, spaceAfter=6, fontName="Helvetica-Bold",
    ),
    "tag": ParagraphStyle(
        "tag", parent=styles["Normal"],
        textColor=ORANGE, fontSize=10, leading=14,
        fontName="Helvetica-Bold", spaceAfter=4,
    ),
    "body": ParagraphStyle(
        "body", parent=styles["Normal"],
        textColor=LIGHT, fontSize=11, leading=16,
        alignment=TA_LEFT, spaceAfter=8, fontName="Helvetica",
    ),
    "bodyJ": ParagraphStyle(
        "bodyJ", parent=styles["Normal"],
        textColor=LIGHT, fontSize=11, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=8, fontName="Helvetica",
    ),
    "code": ParagraphStyle(
        "code", parent=styles["Code"],
        textColor=GREEN, fontSize=9, leading=13,
        fontName="Courier-Bold", backColor=DARK_2,
        leftIndent=12, rightIndent=12, spaceBefore=6, spaceAfter=10,
        borderPadding=8,
    ),
    "small": ParagraphStyle(
        "small", parent=styles["Normal"],
        textColor=MID, fontSize=9, leading=12,
        fontName="Helvetica",
    ),
    "cta": ParagraphStyle(
        "cta", parent=styles["Title"],
        textColor=white, fontSize=20, leading=26,
        alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=14,
    ),
}


# ==============================================================================
# Helpers
# ==============================================================================
def code_block(txt):
    """Bloco de código (Courier verde sobre fundo dark)."""
    return Paragraph(f"<font name='Courier-Bold'>{txt}</font>", S["code"])


def callout(text, bg=YELLOW, fg=DARK_BG):
    """Caixa de destaque (dica do Tiago, alerta, etc)."""
    t = Table(
        [[Paragraph(text, ParagraphStyle(
            "callout", parent=S["body"], textColor=fg,
            fontSize=10, leading=14))]],
        colWidths=[16 * cm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ]))
    return t


def section_header(num, title, color_hex):
    """Cabeçalho de seção numerado tipo PARTE I."""
    color = HexColor(color_hex)
    t = Table(
        [[Paragraph(f"<font color='white'><b>{num}</b></font>",
                    ParagraphStyle("sn", parent=S["h2"], fontSize=20,
                                   alignment=TA_CENTER, textColor=white)),
          Paragraph(f"<font color='white'><b>{title}</b></font>",
                    ParagraphStyle("st", parent=S["h2"], fontSize=18,
                                   textColor=white))]],
        colWidths=[1.6 * cm, 14 * cm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (1, 0), (1, 0), DARK_2),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    return t


def cap_box(title, body, color_hex):
    """Box de capítulo com título colorido e corpo."""
    color = HexColor(color_hex)
    parts = [
        Table(
            [[Paragraph(f"<font color='white'><b>{title}</b></font>",
                        ParagraphStyle("cb", parent=S["h3"], fontSize=13,
                                       textColor=white))]],
            colWidths=[16 * cm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]),
        ),
        Spacer(1, 6),
        Paragraph(body, S["bodyJ"]),
        Spacer(1, 6),
    ]
    return KeepTogether(parts)


# ==============================================================================
# Conteúdo
# ==============================================================================
story = []

# ============================================================
# PÁGINA 1 — CAPA
# ============================================================
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("ZERO ao", S["h0"]))
story.append(Paragraph('<font color="#F97316">DEPLOY</font>', S["h0"]))
story.append(Spacer(1, 0.6 * cm))
story.append(Paragraph(
    "Sua primeira API Python publicada na internet em <b>7 dias</b>.",
    ParagraphStyle("sub", parent=S["body"], fontSize=15, textColor=LIGHT,
                   leading=22)))
story.append(Spacer(1, 0.8 * cm))
story.append(Paragraph(
    "<font color='#94A3B8'>Infra · Python · FastAPI · Docker · CI/CD · Deploy real</font>",
    ParagraphStyle("subtag", parent=S["body"], fontSize=11, leading=16)))

story.append(Spacer(1, 4.5 * cm))
# Tag "gratuito"
gratis = Table(
    [[Paragraph(
        '<font color="white" size="11"><b>EBOOK GRATUITO</b></font>',
        ParagraphStyle("g", parent=S["body"], alignment=TA_CENTER,
                       textColor=white))]],
    colWidths=[4 * cm],
    style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ORANGE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]),
)
story.append(gratis)
story.append(Spacer(1, 0.6 * cm))
story.append(Paragraph(
    "<b>DEVOPSRAIZ</b><br/>"
    "Tiago Alves da Rocha &mdash; 15 anos de Cloud, DevOps e IA<br/>"
    "Material de boas-vindas da Trilha DEVOPSRAIZ",
    ParagraphStyle("auth", parent=S["body"], fontSize=10, textColor=MID,
                   leading=14)))
story.append(PageBreak())

# ============================================================
# PÁGINA 2 — ANTES DE COMEÇAR / QUEM SOU EU
# ============================================================
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("Antes de começar", S["h2"]))
story.append(Paragraph(
    "Se você nunca subiu uma aplicação na internet, esse ebook é pra você. "
    "Em 7 dias de leitura honesta (1 capítulo por dia, ou tudo num fim de semana se "
    "quiser) você vai sair daqui com <b>uma API Python rodando em um servidor de verdade, "
    "com domínio, HTTPS, banco de dados e deploy automático no Git push</b>.",
    S["bodyJ"]))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Sem fluff. Sem teoria desnecessária. Sem &laquo;monta um cluster Kubernetes com "
    "Istio e service mesh&raquo; logo na primeira semana. Você vai entender o básico de "
    "infra, escrever Python que funciona, empacotar em Docker e publicar. <b>Nessa ordem.</b>",
    S["bodyJ"]))
story.append(Spacer(1, 14))

story.append(Paragraph("Quem sou eu", S["h3"]))
story.append(Paragraph(
    "Sou Tiago Alves da Rocha. 15 anos como engenheiro de software, focado em "
    "Cloud, DevOps e IA aplicada. Já operei sistemas críticos em AWS, Azure, GCP "
    "e OCI &mdash; e em 2026 lancei a <b>Trilha DEVOPSRAIZ</b>, 6 ebooks levando "
    "do zero até produção real.",
    S["bodyJ"]))
story.append(Paragraph(
    "Esse ebook gratuito que você está lendo é o <b>ponto de entrada</b> da trilha. "
    "Se gostar do estilo, lá no final eu te conto como pegar a trilha completa com "
    "<b>80% de desconto</b> &mdash; cupom de seguidor.",
    S["bodyJ"]))
story.append(Spacer(1, 12))

story.append(Paragraph("Pré-requisitos", S["h3"]))
story.append(Paragraph(
    "&bull; Um computador com Windows, Mac ou Linux<br/>"
    "&bull; Conexão com a internet<br/>"
    "&bull; <b>Zero</b> conhecimento prévio de programação ou infra<br/>"
    "&bull; Disposição pra abrir o terminal e digitar coisa estranha",
    S["body"]))
story.append(Spacer(1, 14))

story.append(callout(
    "<b>Dica do Tiago:</b> tira-dúvidas pelo WhatsApp <b>(11) 96482-3126</b>. "
    "Manda print do erro, comando que rodou e mensagem que apareceu. "
    "Resposta normalmente em algumas horas.",
    bg=YELLOW, fg=DARK_BG,
))
story.append(PageBreak())

# ============================================================
# PÁGINA 3 — O QUE VOCÊ VAI CONSTRUIR
# ============================================================
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("O que você vai construir", S["h2"]))
story.append(Paragraph(
    "Uma <b>API REST de lista de tarefas</b> (clássico, sei) &mdash; mas publicada na "
    "internet com tudo que uma aplicação real precisa. Vai parecer simples, mas o "
    "<i>esqueleto</i> que você vai montar é o mesmo de produtos que faturam milhões.",
    S["bodyJ"]))
story.append(Spacer(1, 10))

arq = [
    ["1.", "API em Python", "FastAPI &mdash; framework moderno, rápido, com docs automáticos"],
    ["2.", "Banco de dados", "PostgreSQL rodando em container"],
    ["3.", "Container", "Dockerfile com sua app + docker-compose pra subir tudo"],
    ["4.", "CI/CD", "GitHub Actions roda testes e faz build a cada push"],
    ["5.", "Deploy", "Publicado no Render (free tier) com domínio + HTTPS"],
    ["6.", "Monitoramento", "Logs estruturados e health-check funcionando"],
]
arq_data = []
for n, titulo, descricao in arq:
    arq_data.append([
        Paragraph(f"<font color='#F97316'><b>{n}</b></font>",
                  ParagraphStyle("an", parent=S["body"], fontSize=12)),
        Paragraph(f"<b>{titulo}</b>",
                  ParagraphStyle("at", parent=S["body"], textColor=white, fontSize=11)),
        Paragraph(descricao, S["body"]),
    ])
arq_t = Table(arq_data, colWidths=[1 * cm, 4.5 * cm, 10.5 * cm])
arq_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(arq_t)

story.append(Spacer(1, 18))
story.append(Paragraph("Cronograma sugerido (7 dias)", S["h3"]))
crono = [
    ["Dia 1", "Fundamentos de infra (cliente/servidor, DNS, HTTP, Linux básico)"],
    ["Dia 2", "Git + Python em 30 minutos"],
    ["Dia 3", "Primeira API FastAPI rodando no localhost"],
    ["Dia 4", "Banco PostgreSQL + persistência"],
    ["Dia 5", "Docker e docker-compose"],
    ["Dia 6", "Pipeline GitHub Actions"],
    ["Dia 7", "Deploy no Render + domínio + HTTPS"],
]
crono_data = [[Paragraph(f"<b><font color='#F97316'>{d}</font></b>",
                          ParagraphStyle("cd", parent=S["body"], fontSize=11)),
                Paragraph(t, S["body"])] for d, t in crono]
crono_t = Table(crono_data, colWidths=[2 * cm, 14 * cm])
crono_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(crono_t)
story.append(PageBreak())

# ============================================================
# PARTE I — FUNDAMENTOS DE INFRA
# ============================================================
story.append(Spacer(1, 2 * cm))
story.append(section_header("I", "FUNDAMENTOS DE INFRA", "#3B82F6"))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "Antes de escrever uma linha de código, você precisa entender <b>onde</b> esse "
    "código vai rodar. Aqui você descobre o básico que junior tem vergonha de perguntar.",
    ParagraphStyle("intro", parent=S["bodyJ"], fontSize=12, leading=18)))
story.append(Spacer(1, 0.8 * cm))
story.append(Paragraph(
    "<b><font color='#F97316'>Capítulos:</font></b>", S["body"]))
story.append(Paragraph(
    "&bull; Cap. 1 &mdash; Cliente, servidor e a internet em 60 segundos<br/>"
    "&bull; Cap. 2 &mdash; DNS, IP e HTTP sem mistério<br/>"
    "&bull; Cap. 3 &mdash; Os 8 comandos Linux que mudam sua vida<br/>"
    "&bull; Cap. 4 &mdash; Git: o controle de versão que toda vaga pede",
    S["body"]))
story.append(PageBreak())

# ----- CAP 1 -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 1 &mdash; Cliente, servidor e a internet", S["h2"]))
story.append(Paragraph(
    "Quando você abre <font name='Courier-Bold' color='#F59E0B'>instagram.com</font> no celular, três coisas acontecem em "
    "menos de meio segundo:",
    S["bodyJ"]))
story.append(Paragraph(
    "<b>1.</b> Seu celular (o <b>cliente</b>) pergunta pra um servidor de DNS: "
    "&laquo;onde fica instagram.com?&raquo;<br/>"
    "<b>2.</b> O DNS responde com um <b>endereço IP</b> (algo como 157.240.246.174).<br/>"
    "<b>3.</b> Seu celular abre uma conexão HTTPS naquele IP e baixa o HTML, "
    "as imagens, os scripts.",
    S["body"]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Esse &laquo;servidor&raquo; é só um computador igual o seu &mdash; só que ele fica "
    "ligado 24/7 dentro de um datacenter, com IP fixo, e tem um programa rodando que "
    "<b>fica escutando</b> em uma porta (geralmente 80 pra HTTP ou 443 pra HTTPS) "
    "esperando alguém pedir alguma coisa.",
    S["bodyJ"]))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Sua missão nesse ebook é <b>ser o cara que escreve esse programa</b> e <b>publica "
    "ele num servidor desses</b>. Spoiler: você não vai precisar comprar servidor &mdash; "
    "vamos usar serviços de nuvem (Render, no nosso caso) que cuidam disso pra você.",
    S["bodyJ"]))
story.append(Spacer(1, 10))

story.append(Paragraph("Glossário rápido", S["h3"]))
glos1 = [
    ["Cliente", "Quem faz a requisição. Seu navegador, app, curl, etc."],
    ["Servidor", "Quem responde. Pode ser uma API, um site, um banco..."],
    ["Request", "O pedido que o cliente faz. Ex: GET /tarefas"],
    ["Response", "A resposta do servidor. Ex: 200 OK + JSON com tarefas"],
    ["Porta", "Número que identifica o &laquo;atendente&raquo; no servidor. 80, 443, 5432..."],
    ["Localhost", "Você mesmo. Apelido pra 127.0.0.1 &mdash; seu próprio computador."],
]
glos1_data = [[Paragraph(f"<b><font color='#F97316'>{a}</font></b>",
                          ParagraphStyle("g1", parent=S["body"], fontSize=10)),
                Paragraph(b, S["body"])] for a, b in glos1]
glos1_t = Table(glos1_data, colWidths=[3 * cm, 13 * cm])
glos1_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(glos1_t)
story.append(PageBreak())

# ----- CAP 2 -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 2 &mdash; DNS, IP e HTTP", S["h2"]))
story.append(Paragraph(
    "Você não precisa decorar RFC. Mas três conceitos abaixo são <b>obrigatórios</b> "
    "&mdash; vão aparecer em <i>toda</i> entrevista de júnior pra dev/SRE.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

story.append(Paragraph("DNS &mdash; a agenda da internet", S["h3"]))
story.append(Paragraph(
    "Domínios como <font name='Courier-Bold' color='#F59E0B'>devopsraiz.com.br</font> são pra gente lembrar. "
    "Computadores trabalham com IPs (números). O DNS faz a tradução. "
    "Quando você compra um domínio, você aponta ele pra um IP &mdash; e o navegador "
    "do mundo todo consegue chegar no seu servidor.",
    S["bodyJ"]))
story.append(Spacer(1, 6))

story.append(Paragraph("IP &mdash; o CEP do computador", S["h3"]))
story.append(Paragraph(
    "Todo dispositivo conectado tem um IP. Existe IPv4 (4 números separados por ponto, "
    "tipo <font name='Courier-Bold'>192.168.0.1</font>) e IPv6 (mais longo, com letras e dois-pontos). "
    "Servidores em nuvem normalmente têm IP <b>fixo público</b>. Sua casa tem IP "
    "público <b>compartilhado</b> e dinâmico (muda de tempos em tempos).",
    S["bodyJ"]))
story.append(Spacer(1, 6))

story.append(Paragraph("HTTP &mdash; o idioma da web", S["h3"]))
story.append(Paragraph(
    "Toda conversa entre cliente e servidor web acontece em HTTP (ou HTTPS, que é "
    "HTTP criptografado). Os <b>métodos</b> que você precisa saber:",
    S["bodyJ"]))

http_data = [
    [Paragraph("<b><font color='#3B82F6'>GET</font></b>", S["body"]),
     Paragraph("Buscar dados. <i>GET /tarefas</i> = me lista as tarefas", S["body"])],
    [Paragraph("<b><font color='#10B981'>POST</font></b>", S["body"]),
     Paragraph("Criar algo novo. <i>POST /tarefas</i> = cria uma tarefa", S["body"])],
    [Paragraph("<b><font color='#F59E0B'>PUT/PATCH</font></b>", S["body"]),
     Paragraph("Atualizar. <i>PUT /tarefas/42</i> = atualiza a tarefa 42", S["body"])],
    [Paragraph("<b><font color='#EF4444'>DELETE</font></b>", S["body"]),
     Paragraph("Apagar. <i>DELETE /tarefas/42</i> = deleta a tarefa 42", S["body"])],
]
http_t = Table(http_data, colWidths=[2.5 * cm, 13.5 * cm])
http_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(http_t)

story.append(Spacer(1, 10))
story.append(Paragraph("Códigos de resposta que importam:", S["h3"]))
story.append(Paragraph(
    "&bull; <b><font color='#10B981'>2xx</font></b> &mdash; tudo certo (200 OK, 201 Created)<br/>"
    "&bull; <b><font color='#F59E0B'>3xx</font></b> &mdash; redirecionamento<br/>"
    "&bull; <b><font color='#EF4444'>4xx</font></b> &mdash; culpa do cliente (404 não achou, 401 não autenticou)<br/>"
    "&bull; <b><font color='#A855F7'>5xx</font></b> &mdash; culpa do servidor (500 deu pau, 503 fora do ar)",
    S["body"]))
story.append(PageBreak())

# ----- CAP 3 -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 3 &mdash; Linux essencial", S["h2"]))
story.append(Paragraph(
    "99% dos servidores em produção rodam Linux. Você não precisa virar sysadmin, "
    "mas precisa <b>conseguir navegar no terminal sem entrar em pânico</b>. "
    "Aprende esses 8 comandos abaixo e você sobrevive em qualquer servidor.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

linux_cmds = [
    ["pwd", "&laquo;Onde eu tô?&raquo; &mdash; mostra o caminho do diretório atual"],
    ["ls -la", "Lista tudo (até arquivos ocultos) do diretório atual"],
    ["cd pasta", "Entra na pasta. <font name='Courier-Bold'>cd ..</font> volta uma pasta"],
    ["cat arquivo", "Mostra o conteúdo do arquivo no terminal"],
    ["grep \"texto\" arquivo", "Busca por &laquo;texto&raquo; dentro do arquivo"],
    ["nano arquivo", "Editor de texto simples. Ctrl+O salva, Ctrl+X sai"],
    ["chmod +x script.sh", "Dá permissão de execução pro arquivo"],
    ["ps aux | grep nome", "Lista processos rodando que casam com &laquo;nome&raquo;"],
]
linux_data = [[Paragraph(f"<font name='Courier-Bold' color='#F59E0B'>{c}</font>",
                          S["body"]),
                Paragraph(d, S["body"])] for c, d in linux_cmds]
linux_t = Table(linux_data, colWidths=[5 * cm, 11 * cm])
linux_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(linux_t)

story.append(Spacer(1, 12))
story.append(Paragraph("Se você tá no Windows", S["h3"]))
story.append(Paragraph(
    "Instala o <b>WSL2</b> (Windows Subsystem for Linux) com um comando no PowerShell "
    "rodado como administrador:",
    S["bodyJ"]))
story.append(code_block("wsl --install -d Ubuntu"))
story.append(Paragraph(
    "Reinicia, abre o Ubuntu pelo menu Iniciar, cria seu usuário e pronto: você tem um "
    "Linux real dentro do Windows. Daqui pra frente, <b>todos os comandos desse "
    "ebook rodam dentro do WSL</b>.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

story.append(callout(
    "<b>Dica do Tiago:</b> instala também o <b>Visual Studio Code</b>. É o editor de "
    "código mais usado do mundo, é grátis, e tem extensão pra <b>tudo</b> que vamos "
    "usar (Python, Docker, GitHub, etc).",
    bg=YELLOW, fg=DARK_BG,
))
story.append(PageBreak())

# ----- CAP 4 -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 4 &mdash; Git em 5 minutos", S["h2"]))
story.append(Paragraph(
    "<b>Git</b> é um controle de versão. Pensa nele como um &laquo;Ctrl+Z infinito&raquo; "
    "que funciona pra qualquer arquivo de texto/código &mdash; e que sincroniza com a nuvem "
    "(GitHub) pra você não perder nada e pra outros devs trabalharem junto.",
    S["bodyJ"]))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "Toda vaga de programador pede Git. Recrutador olha o GitHub do candidato. "
    "Empresa hospeda código no GitHub. CI/CD escuta evento do GitHub. <b>Sem Git, "
    "você não existe no mercado.</b> Boa notícia: 8 comandos resolvem 95% do uso real.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

git_cmds = [
    ["git init", "Cria um repositório Git nesse diretório"],
    ["git clone &lt;url&gt;", "Baixa um repositório existente"],
    ["git status", "Mostra o que mudou desde o último commit"],
    ["git add .", "Marca todas as mudanças pra serem commitadas"],
    ["git commit -m \"msg\"", "Salva as mudanças com uma mensagem descritiva"],
    ["git push", "Manda os commits pro GitHub"],
    ["git pull", "Baixa commits novos do GitHub pro seu PC"],
    ["git checkout -b feature/x", "Cria uma branch nova e troca pra ela"],
]
git_data = [[Paragraph(f"<font name='Courier-Bold' color='#F59E0B'>{c}</font>",
                        S["body"]),
              Paragraph(d, S["body"])] for c, d in git_cmds]
git_t = Table(git_data, colWidths=[6 * cm, 10 * cm])
git_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(git_t)

story.append(Spacer(1, 12))
story.append(Paragraph("Fluxo básico do dia-a-dia", S["h3"]))
story.append(code_block(
    "# manhã: pega o que o time mexeu<br/>"
    "git pull<br/><br/>"
    "# trabalha, mexe nos arquivos...<br/><br/>"
    "# fim do dia: salva no GitHub<br/>"
    "git status              # confere o que mudou<br/>"
    "git add .               # marca tudo<br/>"
    "git commit -m \"add tarefa endpoint\"<br/>"
    "git push                # manda pra nuvem"
))
story.append(Spacer(1, 6))

story.append(Paragraph("Criando sua conta GitHub", S["h3"]))
story.append(Paragraph(
    "1. Entra em <font name='Courier-Bold' color='#F59E0B'>github.com</font> e cria conta gratuita.<br/>"
    "2. No terminal Linux/WSL, configura seu nome e email:",
    S["body"]))
story.append(code_block(
    "git config --global user.name \"Seu Nome\"<br/>"
    "git config --global user.email \"voce@email.com\""
))
story.append(Paragraph(
    "3. Pra autenticar sem digitar senha a cada push, gera uma chave SSH e adiciona "
    "no GitHub. (No próximo capítulo vou mostrar o primeiro repo.)",
    S["body"]))
story.append(PageBreak())

# ============================================================
# PARTE II — PYTHON + FASTAPI
# ============================================================
story.append(Spacer(1, 2 * cm))
story.append(section_header("II", "PYTHON + FASTAPI", "#F97316"))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "Hora de escrever código. Python porque é a linguagem mais procurada do mercado em "
    "2026 (backend, dados, IA, automação &mdash; tudo). FastAPI porque é o framework "
    "moderno: rápido, com validação automática e documentação gerada de graça.",
    ParagraphStyle("intro", parent=S["bodyJ"], fontSize=12, leading=18)))
story.append(Spacer(1, 0.8 * cm))
story.append(Paragraph(
    "<b><font color='#F97316'>Capítulos:</font></b>", S["body"]))
story.append(Paragraph(
    "&bull; Cap. 5 &mdash; Python em 30 minutos (variáveis, funções, listas)<br/>"
    "&bull; Cap. 6 &mdash; Setup do projeto: venv, pip e o primeiro Hello World<br/>"
    "&bull; Cap. 7 &mdash; FastAPI: sua primeira API rodando<br/>"
    "&bull; Cap. 8 &mdash; PostgreSQL e persistência de verdade",
    S["body"]))
story.append(PageBreak())

# ----- CAP 5 PYTHON BASICS -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 5 &mdash; Python em 30 minutos", S["h2"]))
story.append(Paragraph(
    "Python é uma linguagem que <b>parece pseudocódigo</b>. Você consegue ler um "
    "programa Python antes mesmo de saber programar. Não te peço pra decorar nada: "
    "abre o terminal e digita junto comigo.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

story.append(Paragraph("Instalando Python (WSL/Linux/Mac)", S["h3"]))
story.append(code_block(
    "sudo apt update && sudo apt install -y python3 python3-pip python3-venv<br/>"
    "python3 --version   # deve mostrar 3.10 ou mais novo"
))
story.append(Spacer(1, 6))

story.append(Paragraph("Variáveis", S["h3"]))
story.append(code_block(
    "nome = \"Tiago\"<br/>"
    "idade = 36<br/>"
    "ativo = True<br/>"
    "salario = 12000.50<br/>"
    "print(f\"Oi {nome}, voce tem {idade} anos\")"
))
story.append(Spacer(1, 4))

story.append(Paragraph("Listas e dicionários (os 2 que importam)", S["h3"]))
story.append(code_block(
    "tarefas = [\"comprar pao\", \"estudar\", \"deploy\"]<br/>"
    "tarefas.append(\"academia\")<br/>"
    "print(tarefas[0])    # comprar pao<br/><br/>"
    "tarefa = {<br/>"
    "    \"id\": 1,<br/>"
    "    \"titulo\": \"estudar FastAPI\",<br/>"
    "    \"concluida\": False,<br/>"
    "}<br/>"
    "print(tarefa[\"titulo\"])"
))
story.append(Spacer(1, 4))

story.append(Paragraph("If, for e funções", S["h3"]))
story.append(code_block(
    "def saudacao(nome, formal=False):<br/>"
    "    if formal:<br/>"
    "        return f\"Bom dia, {nome}.\"<br/>"
    "    return f\"E ai {nome}!\"<br/><br/>"
    "for t in tarefas:<br/>"
    "    print(saudacao(t))"
))
story.append(Spacer(1, 6))

story.append(callout(
    "<b>Por que Python?</b> É a linguagem #1 do TIOBE e PyPL em 2026. "
    "Vagas no Brasil pagam de R$6k (júnior) a R$25k (sênior) &mdash; "
    "e é a base de praticamente todo projeto de IA hoje em dia.",
    bg=BLUE, fg=white,
))
story.append(PageBreak())

# ----- CAP 6 PROJETO SETUP -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 6 &mdash; Setup do projeto", S["h2"]))
story.append(Paragraph(
    "Toda projeto Python começa criando uma pasta, um <b>ambiente virtual</b> (venv) "
    "e instalando dependências. Sempre. Sem exceção. Esse hábito te separa do dev "
    "que &laquo;funciona na minha máquina&raquo;.",
    S["bodyJ"]))
story.append(Spacer(1, 6))

story.append(Paragraph("Criando o projeto", S["h3"]))
story.append(code_block(
    "mkdir tarefas-api && cd tarefas-api<br/>"
    "python3 -m venv .venv<br/>"
    "source .venv/bin/activate    # no Windows puro: .venv\\Scripts\\activate<br/>"
    "pip install --upgrade pip"
))
story.append(Paragraph(
    "Quando o venv está ativo, aparece <font name='Courier-Bold'>(.venv)</font> no começo do seu prompt. "
    "Isso significa que o <font name='Courier-Bold'>pip install</font> daqui pra frente vai instalar <b>só "
    "nessa pasta</b> &mdash; não polui seu sistema.",
    S["bodyJ"]))
story.append(Spacer(1, 6))

story.append(Paragraph("Hello World em Python", S["h3"]))
story.append(Paragraph(
    "Cria um arquivo <font name='Courier-Bold' color='#F59E0B'>main.py</font>:",
    S["body"]))
story.append(code_block(
    "def soma(a: int, b: int) -&gt; int:<br/>"
    "    return a + b<br/><br/>"
    "if __name__ == \"__main__\":<br/>"
    "    print(\"oi mundo!\")<br/>"
    "    print(f\"2 + 2 = {soma(2, 2)}\")"
))
story.append(code_block("python main.py   # roda o arquivo"))
story.append(Spacer(1, 8))

story.append(Paragraph("Sobre type hints", S["h3"]))
story.append(Paragraph(
    "Aqueles <font name='Courier-Bold'>: int</font> e <font name='Courier-Bold'>-&gt; int</font> são <b>type hints</b>. Não mudam como o código roda "
    "&mdash; mas ajudam o editor (VS Code) a te avisar quando você passa string onde "
    "esperava número. <b>O FastAPI usa esses hints pra validar dados da sua API "
    "automaticamente</b>. Acostume desde já.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

story.append(Paragraph("Salvando dependências (requirements.txt)", S["h3"]))
story.append(code_block(
    "pip freeze &gt; requirements.txt    # gera a lista do que tá instalado<br/>"
    "pip install -r requirements.txt  # outro dev instala tudo numa tacada"
))
story.append(PageBreak())

# ----- CAP 7 FASTAPI -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 7 &mdash; FastAPI: sua primeira API", S["h2"]))
story.append(Paragraph(
    "Agora a mágica. Em <b>15 linhas de código</b> você tem uma API REST funcionando, "
    "com validação automática e documentação interativa (Swagger) gerada sozinha.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

story.append(code_block(
    "pip install \"fastapi[standard]\""
))
story.append(Paragraph(
    "Substitui o conteúdo do <font name='Courier-Bold'>main.py</font>:",
    S["body"]))
story.append(code_block(
    "from fastapi import FastAPI<br/>"
    "from pydantic import BaseModel<br/><br/>"
    "app = FastAPI(title=\"Tarefas API\")<br/><br/>"
    "class Tarefa(BaseModel):<br/>"
    "    titulo: str<br/>"
    "    concluida: bool = False<br/><br/>"
    "tarefas = []<br/><br/>"
    "@app.get(\"/health\")<br/>"
    "def health():<br/>"
    "    return {\"status\": \"ok\"}<br/><br/>"
    "@app.get(\"/tarefas\")<br/>"
    "def listar():<br/>"
    "    return tarefas<br/><br/>"
    "@app.post(\"/tarefas\", status_code=201)<br/>"
    "def criar(t: Tarefa):<br/>"
    "    tarefas.append(t)<br/>"
    "    return t"
))
story.append(Paragraph("Roda no terminal:", S["body"]))
story.append(code_block("fastapi dev main.py"))
story.append(Paragraph(
    "Abre no navegador <font name='Courier-Bold' color='#F59E0B'>http://localhost:8000/docs</font> &mdash; você vai ver "
    "uma documentação interativa onde dá pra testar os endpoints clicando. "
    "<b>Tudo gerado a partir dos type hints</b>. É magia? Quase.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

story.append(callout(
    "<b>Testa pelo terminal:</b> <font name='Courier-Bold'>curl http://localhost:8000/tarefas</font> &mdash; vai retornar <font name='Courier-Bold'>[]</font>. "
    "Depois: <font name='Courier-Bold'>curl -X POST http://localhost:8000/tarefas -H \"Content-Type: application/json\" "
    "-d '{\"titulo\":\"deploy\"}'</font> &mdash; cria a tarefa.",
    bg=GREEN, fg=DARK_BG,
))
story.append(PageBreak())

# ----- CAP 8 POSTGRES -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 8 &mdash; Persistência com PostgreSQL", S["h2"]))
story.append(Paragraph(
    "Até aqui as tarefas estão em uma lista na memória &mdash; somem quando o servidor "
    "reinicia. Hora de salvar de verdade. Vamos usar <b>PostgreSQL</b> (o banco "
    "relacional mais usado do mundo) e <b>SQLAlchemy</b> (a ORM Python mais popular).",
    S["bodyJ"]))
story.append(Spacer(1, 6))

story.append(Paragraph("Instalando", S["h3"]))
story.append(code_block(
    "pip install \"sqlalchemy[asyncio]\" asyncpg python-dotenv<br/>"
    "pip freeze &gt; requirements.txt"
))
story.append(Paragraph(
    "Pro Postgres em si, vamos subir ele em Docker no <b>capítulo 10</b> (mais fácil "
    "que instalar manualmente). Por enquanto, salva o código.",
    S["body"]))
story.append(Spacer(1, 6))

story.append(Paragraph("Modelo + sessão (db.py)", S["h3"]))
story.append(code_block(
    "from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession<br/>"
    "from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column<br/>"
    "import os<br/><br/>"
    "DATABASE_URL = os.getenv(<br/>"
    "    \"DATABASE_URL\",<br/>"
    "    \"postgresql+asyncpg://postgres:postgres@localhost:5432/tarefas\"<br/>"
    ")<br/><br/>"
    "engine = create_async_engine(DATABASE_URL, echo=False)<br/>"
    "Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)<br/><br/>"
    "class Base(DeclarativeBase):<br/>"
    "    pass<br/><br/>"
    "class TarefaDB(Base):<br/>"
    "    __tablename__ = \"tarefas\"<br/>"
    "    id: Mapped[int] = mapped_column(primary_key=True)<br/>"
    "    titulo: Mapped[str]<br/>"
    "    concluida: Mapped[bool] = mapped_column(default=False)"
))

story.append(Paragraph("Atualizando os endpoints (main.py)", S["h3"]))
story.append(code_block(
    "from sqlalchemy import select<br/>"
    "from db import Session, TarefaDB, Base, engine<br/><br/>"
    "@app.on_event(\"startup\")<br/>"
    "async def startup():<br/>"
    "    async with engine.begin() as conn:<br/>"
    "        await conn.run_sync(Base.metadata.create_all)<br/><br/>"
    "@app.get(\"/tarefas\")<br/>"
    "async def listar():<br/>"
    "    async with Session() as s:<br/>"
    "        r = await s.execute(select(TarefaDB))<br/>"
    "        return r.scalars().all()<br/><br/>"
    "@app.post(\"/tarefas\", status_code=201)<br/>"
    "async def criar(t: Tarefa):<br/>"
    "    async with Session() as s:<br/>"
    "        nova = TarefaDB(titulo=t.titulo, concluida=t.concluida)<br/>"
    "        s.add(nova)<br/>"
    "        await s.commit()<br/>"
    "        await s.refresh(nova)<br/>"
    "        return nova"
))
story.append(Spacer(1, 4))
story.append(callout(
    "<b>O que você acabou de fazer:</b> separou config de banco (db.py) da lógica "
    "da API (main.py). Tá usando ORM com async (rapidíssimo). Endpoints continuam "
    "<i>limpos</i>. Esse é o padrão de projeto Python sério em 2026.",
    bg=PURPLE, fg=white,
))
story.append(PageBreak())

# ============================================================
# PARTE III — DOCKER
# ============================================================
story.append(Spacer(1, 2 * cm))
story.append(section_header("III", "DOCKER & CONTAINERS", "#A855F7"))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "Docker empacota sua aplicação e <b>tudo</b> que ela precisa pra rodar (Python, "
    "bibliotecas, configurações) em uma &laquo;caixinha&raquo; isolada chamada container. "
    "Roda igual no seu PC, no servidor de produção e no laptop do colega. "
    "Acabou a desculpa &laquo;funciona aqui&raquo;.",
    ParagraphStyle("intro", parent=S["bodyJ"], fontSize=12, leading=18)))
story.append(Spacer(1, 0.8 * cm))
story.append(Paragraph("<b><font color='#F97316'>Capítulos:</font></b>", S["body"]))
story.append(Paragraph(
    "&bull; Cap. 9 &mdash; Container vs VM em uma página<br/>"
    "&bull; Cap. 10 &mdash; Dockerfile + docker-compose com Postgres",
    S["body"]))
story.append(PageBreak())

# ----- CAP 9 -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 9 &mdash; Container vs VM", S["h2"]))
story.append(Paragraph(
    "<b>VM (Máquina Virtual):</b> um computador inteiro emulado dentro do seu &mdash; "
    "tem sistema operacional próprio, BIOS, kernel. <b>Pesado</b> (vários GB), "
    "demora minutos pra subir.",
    S["bodyJ"]))
story.append(Paragraph(
    "<b>Container:</b> aproveita o kernel do host (Linux), só isola processos, "
    "rede e disco. <b>Leve</b> (MBs), sobe em <b>segundos</b>. É como se você abrisse "
    "um &laquo;pacote zip&raquo; já configurado e executasse direto.",
    S["bodyJ"]))
story.append(Spacer(1, 6))

cmp_data = [
    [Paragraph("<b><font color='white'>Aspecto</font></b>",
                ParagraphStyle("h", parent=S["body"], textColor=white)),
     Paragraph("<b><font color='white'>VM</font></b>",
                ParagraphStyle("h", parent=S["body"], textColor=white)),
     Paragraph("<b><font color='white'>Container</font></b>",
                ParagraphStyle("h", parent=S["body"], textColor=white))],
    [Paragraph("Tamanho", S["body"]),
     Paragraph("GBs", S["body"]),
     Paragraph("MBs", S["body"])],
    [Paragraph("Boot", S["body"]),
     Paragraph("minutos", S["body"]),
     Paragraph("segundos", S["body"])],
    [Paragraph("Isolamento", S["body"]),
     Paragraph("Total (SO próprio)", S["body"]),
     Paragraph("Processo (kernel compartilhado)", S["body"])],
    [Paragraph("Densidade", S["body"]),
     Paragraph("10s por servidor", S["body"]),
     Paragraph("100s por servidor", S["body"])],
    [Paragraph("Casos de uso", S["body"]),
     Paragraph("SO completo, segurança máxima", S["body"]),
     Paragraph("Microsserviços, deploy ágil", S["body"])],
]
cmp_t = Table(cmp_data, colWidths=[3 * cm, 5.5 * cm, 7.5 * cm])
cmp_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), ORANGE),
    ("BACKGROUND", (0, 1), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(cmp_t)
story.append(Spacer(1, 12))

story.append(Paragraph("Conceitos-chave", S["h3"]))
story.append(Paragraph(
    "&bull; <b>Imagem:</b> a &laquo;receita&raquo; (DNA congelado) do container. Você gera com "
    "<font name='Courier-Bold'>docker build</font>.<br/>"
    "&bull; <b>Container:</b> uma instância em execução de uma imagem.<br/>"
    "&bull; <b>Registry:</b> repositório de imagens. Docker Hub, ECR, GHCR.<br/>"
    "&bull; <b>Volume:</b> pasta persistente fora do container (não some no restart).<br/>"
    "&bull; <b>Rede Docker:</b> permite que containers se enxerguem pelo <i>nome</i> "
    "do serviço, não por IP.",
    S["body"]))
story.append(PageBreak())

# ----- CAP 10 DOCKERFILE -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 10 &mdash; Dockerfile + compose", S["h2"]))
story.append(Paragraph(
    "Cria <font name='Courier-Bold' color='#F59E0B'>Dockerfile</font> na raiz do seu projeto:",
    S["body"]))
story.append(code_block(
    "FROM python:3.12-slim<br/><br/>"
    "WORKDIR /app<br/><br/>"
    "COPY requirements.txt .<br/>"
    "RUN pip install --no-cache-dir -r requirements.txt<br/><br/>"
    "COPY . .<br/><br/>"
    "EXPOSE 8000<br/>"
    "CMD [\"fastapi\", \"run\", \"main.py\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
))
story.append(Paragraph(
    "Linha por linha: parte de uma imagem Python 3.12 minimalista, vai pra "
    "<font name='Courier-Bold'>/app</font>, copia o requirements (esse cache permite que builds futuras pulem o pip "
    "install se nada mudou), instala deps, copia o resto, expõe a porta 8000 e roda.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

story.append(Paragraph("docker-compose.yml &mdash; sobe API + Postgres juntos", S["h3"]))
story.append(code_block(
    "services:<br/>"
    "&nbsp;&nbsp;api:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;build: .<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;ports: [\"8000:8000\"]<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;environment:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/tarefas<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;depends_on: [db]<br/><br/>"
    "&nbsp;&nbsp;db:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;image: postgres:16-alpine<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;environment:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;POSTGRES_USER: postgres<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;POSTGRES_PASSWORD: postgres<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;POSTGRES_DB: tarefas<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;volumes:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- pg_data:/var/lib/postgresql/data<br/><br/>"
    "volumes:<br/>"
    "&nbsp;&nbsp;pg_data:"
))
story.append(Paragraph("Sobe tudo:", S["body"]))
story.append(code_block(
    "docker compose up --build<br/><br/>"
    "# em outro terminal, testa:<br/>"
    "curl http://localhost:8000/health"
))
story.append(Spacer(1, 6))

story.append(callout(
    "<b>Reparou no truque?</b> Dentro do compose, a API conecta no banco pelo "
    "<i>nome do serviço</i> (<font name='Courier-Bold'>db</font>), não por IP. Docker resolve isso na rede interna. "
    "Mesmo padrão usado em Kubernetes &mdash; só que lá em escala.",
    bg=GREEN, fg=DARK_BG,
))
story.append(PageBreak())

# ============================================================
# PARTE IV — CI/CD + DEPLOY
# ============================================================
story.append(Spacer(1, 2 * cm))
story.append(section_header("IV", "CI/CD E DEPLOY", "#10B981"))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "&laquo;Funciona na minha máquina&raquo; é piada de junior. Agora você vai ter uma "
    "<b>esteira automática</b>: a cada git push, o GitHub Actions roda testes, gera a "
    "imagem Docker e o Render publica sua API com domínio e HTTPS automáticos. "
    "Profissional desde o dia 1.",
    ParagraphStyle("intro", parent=S["bodyJ"], fontSize=12, leading=18)))
story.append(Spacer(1, 0.8 * cm))
story.append(Paragraph("<b><font color='#F97316'>Capítulos:</font></b>", S["body"]))
story.append(Paragraph(
    "&bull; Cap. 11 &mdash; GitHub Actions: pipeline em 30 linhas<br/>"
    "&bull; Cap. 12 &mdash; Deploy no Render (free tier, HTTPS automático)<br/>"
    "&bull; Cap. 13 &mdash; Domínio próprio + monitoramento básico",
    S["body"]))
story.append(PageBreak())

# ----- CAP 11 CI -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 11 &mdash; GitHub Actions", S["h2"]))
story.append(Paragraph(
    "<b>CI</b> (Continuous Integration) é o robô que, a cada commit, verifica se o código "
    "ainda funciona &mdash; instala deps, roda testes, faz build. <b>CD</b> (Continuous "
    "Delivery/Deployment) é o robô que, se passou no CI, publica no servidor.",
    S["bodyJ"]))
story.append(Spacer(1, 6))

story.append(Paragraph("Cria o arquivo (caminho exato)", S["h3"]))
story.append(code_block(".github/workflows/ci.yml"))
story.append(code_block(
    "name: CI<br/><br/>"
    "on:<br/>"
    "&nbsp;&nbsp;push:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;branches: [main]<br/>"
    "&nbsp;&nbsp;pull_request:<br/><br/>"
    "jobs:<br/>"
    "&nbsp;&nbsp;test:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;runs-on: ubuntu-latest<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;steps:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- uses: actions/checkout@v4<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- uses: actions/setup-python@v5<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with: { python-version: '3.12' }<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- run: pip install -r requirements.txt pytest<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- run: pytest<br/><br/>"
    "&nbsp;&nbsp;docker:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;needs: test<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;runs-on: ubuntu-latest<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;steps:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- uses: actions/checkout@v4<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- run: docker build -t tarefas-api ."
))
story.append(Paragraph(
    "Crie um teste simples em <font name='Courier-Bold'>tests/test_health.py</font>:",
    S["body"]))
story.append(code_block(
    "from fastapi.testclient import TestClient<br/>"
    "from main import app<br/><br/>"
    "def test_health():<br/>"
    "    r = TestClient(app).get(\"/health\")<br/>"
    "    assert r.status_code == 200<br/>"
    "    assert r.json() == {\"status\": \"ok\"}"
))
story.append(Paragraph(
    "<b>Commita e dá push.</b> Vai na aba <i>Actions</i> do seu repo no GitHub: "
    "você vai ver o pipeline rodando em verde (ou em vermelho, e o log te diz o porquê).",
    S["bodyJ"]))
story.append(PageBreak())

# ----- CAP 12 RENDER DEPLOY -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 12 &mdash; Deploy no Render", S["h2"]))
story.append(Paragraph(
    "Por que <b>Render</b>: tem free tier de verdade, builda Docker a partir do "
    "GitHub, dá HTTPS automático, oferece Postgres gerenciado e a UI é amigável "
    "pra quem tá começando. AWS/GCP a gente vê na Trilha paga.",
    S["bodyJ"]))
story.append(Spacer(1, 6))

passos = [
    ["1.", "Entra em render.com, cria conta com seu GitHub."],
    ["2.", "Clica em <b>New &gt; PostgreSQL</b>. Plano free. Copia a Internal Database URL."],
    ["3.", "Clica em <b>New &gt; Web Service</b>, conecta seu repositório."],
    ["4.", "Em <i>Build &amp; Deploy</i>: escolhe runtime &laquo;Docker&raquo; (Render detecta seu Dockerfile)."],
    ["5.", "Em <i>Environment</i>: adiciona <font name='Courier-Bold'>DATABASE_URL</font> com o valor copiado no passo 2."],
    ["6.", "Clica em <b>Deploy</b>. Render builda a imagem, sobe e te dá uma URL: "
           "<font name='Courier-Bold' color='#F59E0B'>https://tarefas-api.onrender.com</font>"],
    ["7.", "Abre <font name='Courier-Bold'>/docs</font> nessa URL. <b>Tá no ar.</b>"],
]
passos_data = [[Paragraph(f"<b><font color='#10B981'>{n}</font></b>",
                            ParagraphStyle("pn", parent=S["body"], fontSize=12)),
                  Paragraph(t, S["body"])] for n, t in passos]
passos_t = Table(passos_data, colWidths=[1 * cm, 15 * cm])
passos_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(passos_t)

story.append(Spacer(1, 12))
story.append(callout(
    "<b>Pulou um passo?</b> Se aparecer erro 500, abre os <i>logs</i> no painel "
    "do Render. 90% das vezes é DATABASE_URL errada ou faltando. "
    "Tira-dúvidas pelo WhatsApp <b>(11) 96482-3126</b>.",
    bg=RED, fg=white,
))
story.append(Spacer(1, 8))

story.append(Paragraph("Free tier honesto", S["h3"]))
story.append(Paragraph(
    "Free tier do Render <b>desliga</b> o serviço depois de 15 minutos sem requests "
    "(boot a frio leva ~30s). Pra hobby tá ótimo. Quando quiser sempre-ligado, "
    "paga US$ 7/mês &mdash; ou já vai pra AWS/GCP (assunto da Trilha completa).",
    S["bodyJ"]))
story.append(PageBreak())

# ----- CAP 13 DOMÍNIO + MONITORAMENTO -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Cap. 13 &mdash; Domínio próprio + observar", S["h2"]))
story.append(Paragraph("Domínio próprio", S["h3"]))
story.append(Paragraph(
    "1. Compra um domínio (<font name='Courier-Bold'>registro.br</font> pra .com.br ~R$40/ano, ou <font name='Courier-Bold'>cloudflare.com</font> "
    "pra .com a preço de custo).<br/>"
    "2. No Render, vai em <i>Settings &gt; Custom Domains</i>, adiciona <font name='Courier-Bold'>api.seudominio.com.br</font>.<br/>"
    "3. Copia o CNAME que o Render mostra.<br/>"
    "4. No painel do seu registrador, cria um CNAME <font name='Courier-Bold'>api</font> apontando pro Render.<br/>"
    "5. Espera 5-30 minutos. Render gera HTTPS Let's Encrypt automaticamente.",
    S["body"]))
story.append(Spacer(1, 10))

story.append(Paragraph("Logs estruturados", S["h3"]))
story.append(Paragraph(
    "<font name='Courier-Bold'>print()</font> de junior. Logger sério registra <b>contexto</b>:",
    S["body"]))
story.append(code_block(
    "import logging, json, sys<br/><br/>"
    "logger = logging.getLogger(\"api\")<br/>"
    "handler = logging.StreamHandler(sys.stdout)<br/>"
    "handler.setFormatter(logging.Formatter(\"%(asctime)s %(levelname)s %(message)s\"))<br/>"
    "logger.addHandler(handler)<br/>"
    "logger.setLevel(\"INFO\")<br/><br/>"
    "@app.post(\"/tarefas\")<br/>"
    "async def criar(t: Tarefa):<br/>"
    "    logger.info(json.dumps({\"event\": \"criar_tarefa\", \"titulo\": t.titulo}))<br/>"
    "    # ..."
))
story.append(Spacer(1, 6))

story.append(Paragraph("Health-check + uptime grátis", S["h3"]))
story.append(Paragraph(
    "Você já tem <font name='Courier-Bold'>/health</font>. Configura no <b>UptimeRobot</b> (gratuito) pra dar ping "
    "a cada 5 minutos &mdash; se cair, recebe email/Telegram em 30 segundos. "
    "É o monitoramento mínimo viável de um produto de verdade.",
    S["bodyJ"]))
story.append(Spacer(1, 8))

story.append(callout(
    "<b>Você chegou ao fim do roteiro técnico.</b> Tem uma API Python rodando em "
    "produção, com banco, CI/CD, domínio e HTTPS &mdash; tudo grátis. "
    "Isso já te coloca à frente de <i>muito</i> dev júnior aí fora.",
    bg=GREEN, fg=DARK_BG,
))
story.append(PageBreak())

# ============================================================
# PARTE V — PRÓXIMOS PASSOS
# ============================================================
story.append(Spacer(1, 2 * cm))
story.append(section_header("V", "PRÓXIMOS PASSOS", "#A855F7"))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "Esse ebook entrega o <i>esqueleto</i>. Em produto real, você vai querer escalar, "
    "monitorar, blindar contra ataque e usar AWS/Azure/GCP de verdade. <b>Esse é o "
    "conteúdo da Trilha DEVOPSRAIZ paga.</b>",
    ParagraphStyle("intro", parent=S["bodyJ"], fontSize=12, leading=18)))
story.append(PageBreak())

# ----- O QUE VEM DEPOIS -----
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("O caminho até sênior em Cloud", S["h2"]))
story.append(Paragraph(
    "Depois de publicar sua primeira API, esses são os tópicos que separam um dev "
    "&laquo;que sabe deploy&raquo; de um engenheiro Cloud de verdade:",
    S["bodyJ"]))
story.append(Spacer(1, 8))

trilha = [
    ["Kubernetes", "Orquestra centenas de containers, faz auto-scale, "
                    "healing automático e zero-downtime deploys."],
    ["Terraform / IaC", "Define toda sua infra (servidores, bancos, redes) em "
                         "código versionado. Reproduz tudo em segundos."],
    ["AWS / Azure / GCP", "As big-3 da nuvem. Vagas pagam 30-50% a mais "
                          "pra quem domina pelo menos uma."],
    ["Observabilidade", "Métricas (Prometheus), traces (OpenTelemetry), "
                         "dashboards (Grafana). Saber <b>onde</b> dói."],
    ["Segurança & LGPD", "OWASP Top 10, gestão de secrets, IAM correto, "
                          "Zero Trust. Não é mais opcional."],
    ["IA aplicada", "RAG, agents, function calling. O mercado vai pagar caro "
                     "por dev que sabe colocar LLM em produção."],
]
trilha_data = []
for tema, desc in trilha:
    trilha_data.append([
        Paragraph(f"<b><font color='#F97316'>{tema}</font></b>",
                  ParagraphStyle("tt", parent=S["body"], fontSize=11)),
        Paragraph(desc, S["body"]),
    ])
trilha_t = Table(trilha_data, colWidths=[4 * cm, 12 * cm])
trilha_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(trilha_t)

story.append(Spacer(1, 14))
story.append(Paragraph(
    "Cada um desses tópicos é um <b>ebook completo</b> dentro da Trilha DEVOPSRAIZ &mdash; "
    "com exemplos de código, scripts copy-paste e cenários de produção real.",
    S["bodyJ"]))
story.append(PageBreak())

# ============================================================
# CTA FINAL — TRILHA PAGA
# ============================================================
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Trilha DEVOPSRAIZ completa", S["h1"]))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>6 ebooks</b> + calendário de 30 dias + tira-dúvidas pelo WhatsApp. "
    "Você sai de zero infra e chega no nível pleno em 30 dias de estudo guiado &mdash; "
    "com prazo, calendário e cobrança (estilo classroom).",
    S["bodyJ"]))
story.append(Spacer(1, 14))

trilha_paga = [
    ["Ebook 1", "Plataforma Multi-Cloud com IA (FinOps em 4 clouds)"],
    ["Ebook 2", "Docker, Kubernetes, Terraform &mdash; do zero a EKS/AKS"],
    ["Ebook 3", "De Projeto a SaaS multi-tenant com billing"],
    ["Ebook 4", "IA Avançada: RAG, Agents, Function Calling"],
    ["Ebook 5", "Observabilidade e SRE em produção"],
    ["Ebook 6", "Segurança Cloud, LGPD, Zero Trust"],
    ["+ Bônus", "Calendário de 30 dias com prazo por dia"],
    ["+ Bônus", "Tira-dúvidas direto pelo WhatsApp"],
]
tp_data = [[Paragraph(f"<b><font color='#F97316'>{a}</font></b>",
                       ParagraphStyle("t1", parent=S["body"], fontSize=11)),
             Paragraph(b, S["body"])] for a, b in trilha_paga]
tp_t = Table(tp_data, colWidths=[3 * cm, 13 * cm])
tp_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(tp_t)

story.append(Spacer(1, 18))

# Cupom destacado (3 linhas separadas pra evitar overlap)
_cup_style_top = ParagraphStyle(
    "cup_top", parent=S["body"], alignment=TA_CENTER, leading=18,
    textColor=white, fontSize=14)
_cup_style_big = ParagraphStyle(
    "cup_big", parent=S["body"], alignment=TA_CENTER, leading=44,
    textColor=white, fontSize=36, fontName="Helvetica-Bold")
_cup_style_bot = ParagraphStyle(
    "cup_bot", parent=S["body"], alignment=TA_CENTER, leading=14,
    textColor=white, fontSize=11)

cupom_table = Table(
    [
        [Paragraph('DE&nbsp;<strike>R$ 199,99</strike>&nbsp;POR', _cup_style_top)],
        [Paragraph('<b>R$ 39,99</b>', _cup_style_big)],
        [Paragraph('com o cupom <b>SEGUIDOR80</b> &mdash; 80% OFF '
                   'pra quem está lendo esse ebook', _cup_style_bot)],
    ],
    colWidths=[16 * cm],
)
cupom_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), ORANGE),
    ("TOPPADDING", (0, 0), (0, 0), 18),
    ("BOTTOMPADDING", (0, 0), (0, 0), 0),
    ("TOPPADDING", (0, 1), (0, 1), 0),
    ("BOTTOMPADDING", (0, 1), (0, 1), 4),
    ("TOPPADDING", (0, 2), (0, 2), 0),
    ("BOTTOMPADDING", (0, 2), (0, 2), 18),
]))
story.append(cupom_table)

story.append(Spacer(1, 14))

cta_link = Table(
    [[Paragraph(
        '<font color="white" size="14"><b>Pega a Trilha &raquo;</b></font><br/>'
        '<font color="#F97316" size="12">go.hotmart.com/S105313699A</font><br/>'
        '<font color="#94A3B8" size="9">Use o cupom <b>SEGUIDOR80</b> no checkout</font>',
        ParagraphStyle("link", parent=S["body"], alignment=TA_CENTER, leading=18)
    )]],
    colWidths=[16 * cm],
)
cta_link.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("TOPPADDING", (0, 0), (-1, -1), 16),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
]))
story.append(cta_link)
story.append(PageBreak())

# ============================================================
# PÁGINA FINAL — CONTATO + WHATSAPP
# ============================================================
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Falou comigo, falou com o autor", S["h2"]))
story.append(Paragraph(
    "Diferente da maioria dos cursos de DevOps por aí, aqui você fala <b>direto comigo</b>. "
    "Não tem tutor terceirizado, não tem Discord abandonado. Tira-dúvidas no WhatsApp, "
    "resposta no mesmo dia em horário útil.",
    S["bodyJ"]))
story.append(Spacer(1, 16))

# Bloco WhatsApp destacado
wa = Table(
    [[Paragraph(
        '<font color="white" size="11"><b>TIRA-DÚVIDAS</b></font><br/>'
        '<font color="white" size="28"><b>(11) 96482-3126</b></font><br/>'
        '<font color="white" size="10">WhatsApp do Tiago &mdash; print do erro + '
        'comando que rodou. Resposta em algumas horas.</font>',
        ParagraphStyle("wa", parent=S["body"], alignment=TA_CENTER, leading=22,
                       textColor=white)
    )]],
    colWidths=[16 * cm],
)
wa.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), GREEN),
    ("TOPPADDING", (0, 0), (-1, -1), 22),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
]))
story.append(wa)

story.append(Spacer(1, 20))

story.append(Paragraph("Onde me achar", S["h3"]))
contato = [
    ["Instagram", "@devopsraiz_oficial &mdash; posts diários de Cloud, DevOps e IA em PT-BR"],
    ["WhatsApp", "(11) 96482-3126 &mdash; tira-dúvidas técnico"],
    ["Hotmart", "go.hotmart.com/S105313699A &mdash; Trilha DEVOPSRAIZ"],
    ["E-mail", "tiago@tr83.com.br"],
]
ct_data = [[Paragraph(f"<b><font color='#F97316'>{a}</font></b>",
                       ParagraphStyle("c1", parent=S["body"], fontSize=11)),
             Paragraph(b, S["body"])] for a, b in contato]
ct_t = Table(ct_data, colWidths=[3.5 * cm, 12.5 * cm])
ct_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))
story.append(ct_t)

story.append(Spacer(1, 18))
story.append(Paragraph(
    "<i>&laquo;Compartilha esse ebook com aquele amigo que tá perdido em curso de "
    "JS e querendo migrar pra Cloud. Quanto mais a galera entrar no jogo, mais barato fica "
    "contratar dev bom no Brasil &mdash; e mais raiz fica nossa comunidade.&raquo;</i>",
    ParagraphStyle("final", parent=S["bodyJ"], textColor=MID, fontSize=10,
                   alignment=TA_CENTER, leading=15)))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "&mdash; Tiago, <b>@devopsraiz_oficial</b>",
    ParagraphStyle("sign", parent=S["body"], textColor=ORANGE, fontSize=11,
                   alignment=TA_CENTER, fontName="Helvetica-Bold")))

# ==============================================================================
# Build
# ==============================================================================
doc = BaseDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=2.5 * cm,
    rightMargin=2.5 * cm,
    topMargin=1.5 * cm,
    bottomMargin=1.5 * cm,
    title="Zero ao Deploy — sua primeira API Python publicada em 7 dias",
    author="Tiago Alves da Rocha",
    subject="Ebook gratuito — Trilha DEVOPSRAIZ",
    keywords="python, fastapi, docker, ci/cd, deploy, devops",
)

frame_normal = Frame(
    2.5 * cm, 1.5 * cm,
    W - 5 * cm, H - 3.3 * cm,
    leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0,
)
template_normal = PageTemplate(id="dark", frames=[frame_normal], onPage=page_dark)

frame_cover = Frame(
    2.5 * cm, 1.5 * cm,
    W - 5 * cm, H - 3.3 * cm,
    leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0,
)
template_cover = PageTemplate(id="cover", frames=[frame_cover], onPage=page_cover)

doc.addPageTemplates([template_cover, template_normal])
# Página 2 em diante muda pro template dark
from reportlab.platypus import NextPageTemplate
story.insert(1, NextPageTemplate("dark"))  # depois da primeira página, vira dark

doc.build(story)

print("OK PDF gerado")
print(str(OUT))
