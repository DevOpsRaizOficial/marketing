"""
Gera UM PDF de Apoio por aula da serie de 30 dias DEVOPSRAIZ.

Conteudo de cada PDF (4-6 paginas):
  1. Capa com numero da aula + titulo + cupom CUPOM50
  2. Resumo executivo (o que voce aprende em 7 min)
  3. Comandos passo-a-passo com explicacao
  4. Troubleshooting comum
  5. Exercicio pratico
  6. CTA: trilha completa + WhatsApp

Saida: pdf-apoio/pdf-apoio-aula-XX.pdf

Uso:
    # gera todos os 30
    python build_pdf_apoio.py

    # gera so 1 aula
    python build_pdf_apoio.py --day 1
"""
import argparse
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Table, TableStyle, KeepTogether,
)

# Reusa lista mestre de aulas
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "roteiros"))
from generate_30_aulas import AULAS  # noqa: E402

ROOT = Path(__file__).resolve().parent
ROOT.mkdir(parents=True, exist_ok=True)

# ===== Paleta DevOpsRaiz =====
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

W, H = A4


def page_dark(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, H - 6, W, 6, fill=1, stroke=0)
    canvas.setFillColor(DARK_2)
    canvas.rect(0, 0, W, 30, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, 30, W, 2, fill=1, stroke=0)
    canvas.setFillColor(LIGHT)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(40, 12, "@DevOpsRaiz  -  PDF de Apoio")
    canvas.setFillColor(MID)
    canvas.drawRightString(W - 40, 12, f"pag. {canvas.getPageNumber()}")
    canvas.restoreState()


styles = getSampleStyleSheet()
S = {
    "h1": ParagraphStyle("h1", parent=styles["Title"], textColor=white,
                          fontSize=32, leading=38, alignment=TA_LEFT,
                          spaceAfter=10, fontName="Helvetica-Bold"),
    "h2": ParagraphStyle("h2", parent=styles["Heading1"], textColor=ORANGE,
                          fontSize=20, leading=26, alignment=TA_LEFT,
                          spaceAfter=10, fontName="Helvetica-Bold"),
    "h3": ParagraphStyle("h3", parent=styles["Heading2"], textColor=white,
                          fontSize=14, leading=20, spaceAfter=6,
                          fontName="Helvetica-Bold"),
    "body": ParagraphStyle("body", parent=styles["Normal"], textColor=LIGHT,
                            fontSize=11, leading=16, spaceAfter=8,
                            fontName="Helvetica"),
    "bodyJ": ParagraphStyle("bodyJ", parent=styles["Normal"], textColor=LIGHT,
                             fontSize=11, leading=16, alignment=TA_JUSTIFY,
                             spaceAfter=8, fontName="Helvetica"),
    "code": ParagraphStyle("code", parent=styles["Code"], textColor=GREEN,
                            fontSize=10, leading=14, fontName="Courier-Bold",
                            backColor=DARK_2, leftIndent=12, rightIndent=12,
                            spaceBefore=6, spaceAfter=10, borderPadding=8),
}


def code_block(txt):
    safe = (txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return Paragraph(f"<font name='Courier-Bold'>$ {safe}</font>", S["code"])


def callout(text, bg=YELLOW, fg=DARK_BG):
    t = Table(
        [[Paragraph(text, ParagraphStyle(
            "co", parent=S["body"], textColor=fg, fontSize=10, leading=14))]],
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


# ===== Conteudo extra (troubleshooting + exercicios) por aula =====
# Para evitar texto generico, defino um pequeno banco de troubleshooting
# e exercicios reaproveitaveis baseado em padroes comuns.
TROUBLESHOOTING_PADRAO = {
    1: [
        ("nslookup retorna SERVFAIL",
         "Servidor DNS configurado nao responde. Troca por 8.8.8.8 ou 1.1.1.1."),
        ("curl -I demora e da timeout",
         "Firewall corporativo ou proxy. Confere variaveis HTTP_PROXY/HTTPS_PROXY."),
    ],
    2: [
        ("git push pede senha sempre",
         "SSH nao configurado. Roda 'ssh-add ~/.ssh/id_ed25519' e adiciona chave publica no GitHub."),
        ("permission denied (publickey)",
         "Chave SSH nao reconhecida. Testa com 'ssh -T git@github.com'."),
    ],
    3: [
        ("ModuleNotFoundError: No module named X",
         "venv nao ativado. Roda 'source .venv/bin/activate' antes do pip install."),
        ("pip install falha com SSL error",
         "Atualiza pip primeiro: 'pip install --upgrade pip certifi'."),
    ],
    4: [
        ("ImportError: cannot import name 'FastAPI'",
         "FastAPI nao instalado no venv ativo. Roda 'pip install fastapi[standard]'."),
        ("/docs retorna 404",
         "Voce esta na porta errada. Default e localhost:8000."),
    ],
    5: [
        ("connection refused na 5432",
         "Postgres nao subiu. Confere com 'docker ps' e 'docker logs <id>'."),
        ("password authentication failed",
         "POSTGRES_PASSWORD nao bate. Mata o container, recria com a senha certa."),
    ],
    6: [
        ("docker: command not found",
         "Docker Desktop nao instalado/iniciado. Reinicia o servico."),
        ("error during build: failed to solve",
         "Provavel Dockerfile com path errado no COPY. Confere paths relativos."),
    ],
    7: [
        ("Render build falha com pip error",
         "requirements.txt desatualizado. Roda 'pip freeze > requirements.txt' local."),
        ("Custom domain nao propaga",
         "CNAME pode demorar 30 min. Testa com 'dig api.dominio.com'."),
    ],
    8: [
        ("kubectl get pods - connection refused",
         "kubeconfig nao apontando. Roda 'kubectl config use-context <nome>'."),
        ("CrashLoopBackOff sem causa clara",
         "Roda 'kubectl logs <pod> --previous' pra ver logs do crash anterior."),
    ],
    9: [
        ("terraform plan trava sem feedback",
         "Provavel rate limit do provider. Define TF_LOG=INFO pra ver."),
        ("State lock acquisition error",
         "Outro 'terraform apply' rodando. Espera ou usa 'terraform force-unlock'."),
    ],
    10: [
        ("aws: An error occurred (UnauthorizedOperation)",
         "IAM sem permissao. Confere a policy do user/role atual."),
        ("aws cli nao encontra credenciais",
         "Roda 'aws configure' ou exporta AWS_PROFILE corretamente."),
    ],
}


def get_troubleshooting(dia):
    return TROUBLESHOOTING_PADRAO.get(dia, [
        ("Comando nao encontrado",
         "Confere se o binario esta no PATH e se a versao bate."),
        ("Permission denied",
         "Roda com sudo (Linux) ou Administrador (Windows), conforme contexto."),
    ])


def build_pdf(dia, slug, titulo, hook_short, punchline_short,
               conceitos, comandos, out_path):
    story = []
    # CAPA
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(f"TEMA {dia:02d} / 30", S["h2"]))
    story.append(Paragraph(titulo, S["h1"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "<i>PDF de Apoio</i>  ·  Canal @DevOpsRaiz  ·  Trilha DEVOPSRAIZ",
        ParagraphStyle("sub", parent=S["body"], fontSize=12,
                       textColor=MID, leading=18)))
    story.append(Spacer(1, 1.5 * cm))
    story.append(callout(
        f"<b>Voce comprou o PDF mais barato do mercado.</b><br/>"
        f"Preco normal: R$ 9,90 - Com cupom <b>CUPOM50</b>: R$ 4,95<br/>"
        f"Veja la no final como destravar a Trilha completa (6 ebooks + 30 dias) "
        f"com 80% off pelo cupom <b>SEGUIDOR80</b>.",
        bg=ORANGE, fg=white,
    ))
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(
        "Tiago Alves da Rocha<br/>"
        "Engenheiro de Software · 15 anos em Cloud, DevOps e IA<br/>"
        "WhatsApp tira-duvidas: <b>(11) 96482-3126</b>",
        ParagraphStyle("aut", parent=S["body"], fontSize=10, textColor=MID,
                       leading=14)))
    story.append(PageBreak())

    # VOCE VIU NO SHORT
    story.append(Paragraph("Voce viu no short", S["h2"]))
    story.append(Spacer(1, 4))
    story.append(callout(
        f"<b>Hook (3s):</b><br/>{hook_short}<br/><br/>"
        f"<b>Punchline (5s):</b><br/>{punchline_short}",
        bg=DARK_2, fg=LIGHT,
    ))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Aqui esta tudo que o short prometeu", S["h2"]))
    story.append(Paragraph(
        "O short tem 10 segundos. Esse PDF tem o conteudo completo "
        "pra voce aplicar agora.",
        S["bodyJ"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("O que voce vai dominar nesse material:", S["body"]))
    bullets = "<br/>".join(f"&bull; <b>{c}</b>" for c in conceitos)
    story.append(Paragraph(bullets, S["body"]))
    story.append(Spacer(1, 12))
    story.append(callout(
        "<b>Como usar esse PDF:</b><br/>"
        "1. Assiste o short no canal @devopsraiz<br/>"
        "2. Abre esse PDF lado a lado<br/>"
        "3. Roda os 3 comandos enquanto le a explicacao<br/>"
        "4. Faz o exercicio no final pra fixar<br/>"
        "5. Trava? WhatsApp (11) 96482-3126",
        bg=BLUE, fg=white,
    ))
    story.append(PageBreak())

    # COMANDOS
    story.append(Paragraph("Comandos passo-a-passo", S["h2"]))
    story.append(Paragraph(
        "Cada comando abaixo aparece no video, no overlay terminal verde. Voce pode copiar daqui ou do repositorio GitHub publico (link na ultima pagina).",
        S["bodyJ"]))
    story.append(Spacer(1, 8))
    for i, cmd in enumerate(comandos):
        first_line = cmd.splitlines()[0]
        story.append(Paragraph(f"<b>{i+1}. {first_line[:80]}</b>", S["h3"]))
        story.append(code_block(cmd))
        story.append(Paragraph(
            f"<i>O que faz:</i> testa/demonstra o conceito de "
            f"<b>{conceitos[min(i, len(conceitos)-1)]}</b> "
            f"na pratica. Saida esperada deve ser nao-vazia.",
            S["body"]))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # TROUBLESHOOTING
    story.append(Paragraph("Troubleshooting comum", S["h2"]))
    story.append(Paragraph(
        "Quando o comando nao funciona, ai vai a lista dos erros mais frequentes "
        "que aparecem nessa aula e como resolver em segundos:",
        S["bodyJ"]))
    story.append(Spacer(1, 6))
    for err, fix in get_troubleshooting(dia):
        story.append(callout(
            f"<b>{err}</b><br/>{fix}",
            bg=DARK_2, fg=LIGHT,
        ))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Outros erros que nao estao na lista: manda print no WhatsApp "
        "<b>(11) 96482-3126</b> com:<br/>"
        "1. Comando exato que rodou<br/>"
        "2. Mensagem de erro completa<br/>"
        "3. Sistema operacional + versao",
        S["body"]))
    story.append(PageBreak())

    # EXERCICIO
    story.append(Paragraph("Exercicio pratico", S["h2"]))
    story.append(Paragraph(
        f"Faca esse exercicio em 10 minutos. Se travar, manda print no WhatsApp.",
        S["bodyJ"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Desafio", S["h3"]))
    story.append(Paragraph(
        f"Reproduza os comandos da aula no seu ambiente. Adicione UM passo extra "
        f"baseado em <b>{conceitos[-1]}</b> que nao foi mostrado na aula. "
        f"Documenta o que voce fez num README.md no seu repositorio.",
        S["bodyJ"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Checklist de conclusao", S["h3"]))
    story.append(Paragraph(
        "&bull; [ ] Comandos da aula rodaram sem erro<br/>"
        "&bull; [ ] Entendi <b>por que</b> cada um faz o que faz<br/>"
        "&bull; [ ] Implementei o passo extra<br/>"
        "&bull; [ ] Commitei no GitHub e mandei o link no WhatsApp",
        S["body"]))
    story.append(Spacer(1, 14))
    story.append(callout(
        "<b>Bonus:</b> manda o link do seu repositorio no WhatsApp "
        "<b>(11) 96482-3126</b> que eu reviso e dou feedback tecnico personalizado.",
        bg=GREEN, fg=DARK_BG,
    ))
    story.append(PageBreak())

    # CTA FINAL
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("Proximo passo: Trilha completa", S["h2"]))
    story.append(Paragraph(
        "Esse PDF cobre <b>1 aula</b>. A Trilha DEVOPSRAIZ completa tem:",
        S["bodyJ"]))
    story.append(Spacer(1, 6))
    trilha_items = [
        ("Ebook 1", "Plataforma Multi-Cloud com IA"),
        ("Ebook 2", "Docker, Kubernetes, Terraform"),
        ("Ebook 3", "De Projeto a SaaS multi-tenant"),
        ("Ebook 4", "IA Avancada: RAG, Agents"),
        ("Ebook 5", "Observabilidade e SRE"),
        ("Ebook 6", "Seguranca Cloud, LGPD"),
        ("+ Bonus", "Calendario 30 dias com prazo"),
        ("+ Bonus", "Tira-duvidas WhatsApp"),
    ]
    rows = [[Paragraph(f"<b><font color='#F97316'>{a}</font></b>", S["body"]),
              Paragraph(b, S["body"])] for a, b in trilha_items]
    t = Table(rows, colWidths=[3 * cm, 13 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_2),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, SLATE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))
    story.append(callout(
        '<font color="white" size="11">DE</font> '
        '<font color="white"><strike>R$ 199,99</strike></font> '
        '<font color="white" size="11">POR</font><br/>'
        '<font color="white" size="32"><b>R$ 39,99</b></font><br/>'
        '<font color="white" size="11">com o cupom <b>SEGUIDOR80</b></font>',
        bg=ORANGE, fg=white,
    ))
    story.append(Spacer(1, 12))
    story.append(callout(
        '<font color="white" size="11"><b>Pega a Trilha:</b></font><br/>'
        '<font color="#F97316" size="12">go.hotmart.com/S105313699A</font><br/>'
        '<font color="#94A3B8" size="9">Use cupom SEGUIDOR80 no checkout</font>',
        bg=DARK_2, fg=white,
    ))

    # Build
    doc = BaseDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=2.5 * cm, rightMargin=2.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        title=f"PDF Apoio Aula {dia:02d} - {titulo}",
        author="Tiago Alves da Rocha",
        subject="PDF de Apoio - Trilha DEVOPSRAIZ",
    )
    frame = Frame(2.5 * cm, 1.5 * cm, W - 5 * cm, H - 3.3 * cm,
                   leftPadding=0, bottomPadding=0,
                   rightPadding=0, topPadding=0)
    template = PageTemplate(id="dark", frames=[frame], onPage=page_dark)
    doc.addPageTemplates([template])
    doc.build(story)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--day", type=int, help="numero do dia (1-30)")
    args = p.parse_args()

    targets = ([a for a in AULAS if a[0] == args.day] if args.day else AULAS)
    if not targets:
        print(f"Tema {args.day} nao encontrado")
        return

    for dia, slug, titulo, hook, punch, conceitos, comandos in targets:
        out = ROOT / f"pdf-apoio-{dia:02d}-{slug}.pdf"
        build_pdf(dia, slug, titulo, hook, punch, conceitos, comandos, out)
        size_kb = out.stat().st_size / 1024
        print(f"  OK {out.name} ({size_kb:.1f} KB)")

    print(f"\n{len(targets)} PDF(s) gerado(s) em {ROOT}")


if __name__ == "__main__":
    main()
