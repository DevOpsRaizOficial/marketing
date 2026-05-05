"""
Gera 3 PNGs (1080x1350) pros posts únicos:
- Day 18: Frase Junior vs Senior
- Day 23: Checklist 10 skills DevOps Pleno
- Day 28: Testemunho 3 razões da Trilha

Naming: NN-tipo-tema.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path("/sessions/sweet-friendly-maxwell/mnt/Ebooks-DevopsRaiz/marketing/criativos")
OUT_DIR.mkdir(exist_ok=True, parents=True)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

DARKER = (2, 6, 23)
DARK = (15, 23, 42)
SLATE = (30, 41, 59)
LIGHT = (226, 232, 240)
MID = (100, 116, 139)
WHITE = (255, 255, 255)
ORANGE = (249, 115, 22)
RED = (239, 68, 68)
YELLOW = (245, 158, 11)
GREEN = (16, 185, 129)
BLUE = (59, 130, 246)
PURPLE = (168, 85, 247)

W, H = 1080, 1350


def gradient_bg(color_top, color_bot):
    img = Image.new("RGB", (W, H), color_top)
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(color_top[0] * (1 - t) + color_bot[0] * t)
        g = int(color_top[1] * (1 - t) + color_bot[1] * t)
        b = int(color_top[2] * (1 - t) + color_bot[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img


def wrap(text, font, max_w, draw):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_multiline(draw, text, x, y, font, color, max_w, line_sp=10):
    for line in wrap(text, font, max_w, draw):
        draw.text((x, y), line, font=font, fill=color)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + line_sp
    return y


def pill(draw, text, x, y, font, text_color, bg_color, pad_x=22, pad_y=10):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0] + pad_x * 2
    h = bbox[3] - bbox[1] + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg_color)
    draw.text((x + pad_x, y + pad_y - 4), text, font=font, fill=text_color)
    return x + w


def header_footer(draw, ebook_tag, color):
    """Header com marca + pill + footer com handle."""
    brand = ImageFont.truetype(FONT_BOLD, 26)
    draw.text((60, 50), "DEVOPSRAIZ", font=brand, fill=color)

    pill_font = ImageFont.truetype(FONT_BOLD, 20)
    pill(draw, ebook_tag, 60, 95, pill_font, WHITE, color)

    draw.rectangle([60, 140, W - 60, 142], fill=color)

    draw.rectangle([0, H - 90, W, H], fill=DARKER)
    draw.rectangle([0, H - 93, W, H - 90], fill=color)

    handle_font = ImageFont.truetype(FONT_REG, 22)
    draw.text((60, H - 70), "@devopsraiz_oficial", font=handle_font, fill=LIGHT)

    cta_font = ImageFont.truetype(FONT_BOLD, 22)
    cta = "Trilha • link na bio"
    bbox = draw.textbbox((0, 0), cta, font=cta_font)
    tw = bbox[2] - bbox[0]
    draw.text((W - tw - 60, H - 70), cta, font=cta_font, fill=color)


# =============================================================================
# Day 18 — Frase Junior vs Senior (replace 08-frase-junior-vs-senior.png role)
# =============================================================================
def day_18_junior_senior():
    img = gradient_bg(DARKER, DARK)
    draw = ImageDraw.Draw(img)

    color = YELLOW  # Ebook 5 SRE
    header_footer(draw, "EBOOK 5 • OBSERVABILIDADE/SRE", color)

    # Layout: 3 níveis em escada (Junior → Pleno → Sênior)
    title_font = ImageFont.truetype(FONT_BOLD, 56)
    y = 200
    draw.text((60, y), "A diferença entre", font=title_font, fill=WHITE)
    y += 70
    draw.text((60, y), "Junior e Sênior", font=title_font, fill=color)
    y += 70
    draw.text((60, y), "não é stack.", font=title_font, fill=WHITE)
    y += 70
    draw.text((60, y), "É maturidade", font=title_font, fill=color)
    y += 70
    draw.text((60, y), "operacional.", font=title_font, fill=color)

    y += 130

    # 3 caixas com nível + frase
    niveis = [
        ("JUNIOR", "\"Funciona na minha máquina\"", RED),
        ("PLENO", "\"Funciona em staging\"", YELLOW),
        ("SÊNIOR", "\"Tem métrica, alerta, runbook, rollback,\nteste de carga, e não acorda às 3am\"", GREEN),
    ]

    for label, frase, cor in niveis:
        # Pill de nível
        lf = ImageFont.truetype(FONT_BOLD, 24)
        pill(draw, label, 60, y, lf, WHITE, cor)
        # Frase abaixo
        ff = ImageFont.truetype(FONT_REG, 26)
        for line in frase.split("\n"):
            draw.text((60, y + 60), line, font=ff, fill=LIGHT)
            y += 35
        y += 50

    img.save(OUT_DIR / "18-frase-junior-pleno-senior.png", "PNG", optimize=True)
    print(f"  ✓ 18-frase-junior-pleno-senior.png")


# =============================================================================
# Day 23 — Checklist 10 skills DevOps Pleno
# =============================================================================
def day_23_checklist_pleno():
    img = gradient_bg(DARKER, DARK)
    draw = ImageDraw.Draw(img)

    color = BLUE
    header_footer(draw, "TRILHA DEVOPSRAIZ", color)

    title_font = ImageFont.truetype(FONT_BOLD, 60)
    y = 195
    draw.text((60, y), "10 skills pra virar", font=title_font, fill=WHITE)
    y += 75
    draw.text((60, y), "DevOps Pleno", font=title_font, fill=color)
    y += 75
    draw.text((60, y), "em 2026", font=title_font, fill=color)

    y += 90

    sub_font = ImageFont.truetype(FONT_BOLD, 26)
    draw.text((60, y), "Marca 7/10? Já tá pronto pro pleito.", font=sub_font, fill=YELLOW)

    y += 70

    skills = [
        "Docker + Compose + Dockerfile otimizado",
        "Kubernetes (kubectl, helm, services)",
        "Terraform (providers, modules, state)",
        "Cloud principal (AWS / Azure / GCP)",
        "CI/CD (GitHub Actions / GitLab)",
        "Observabilidade (Prometheus + Grafana)",
        "Linux fluente (systemctl, journalctl)",
        "SQL + NoSQL básico em prod",
        "Hardening: TLS, RBAC, Network Policies",
        "Inglês técnico pra ler RFC e issues",
    ]

    sf = ImageFont.truetype(FONT_REG, 26)
    for i, s in enumerate(skills, 1):
        # Checkbox
        box_x = 60
        box_y = y + 4
        draw.rounded_rectangle([box_x, box_y, box_x + 30, box_y + 30],
                               radius=6, outline=color, width=3)
        # Numero ao lado da box
        num_font = ImageFont.truetype(FONT_BOLD, 22)
        draw.text((box_x + 50, y), f"{i:02}.", font=num_font, fill=color)
        # Skill
        draw.text((box_x + 105, y), s, font=sf, fill=LIGHT)
        y += 50

    img.save(OUT_DIR / "23-checklist-devops-pleno.png", "PNG", optimize=True)
    print(f"  ✓ 23-checklist-devops-pleno.png")


# =============================================================================
# Day 28 — Testemunho 3 razões
# =============================================================================
def day_28_testemunho_trilha():
    img = gradient_bg(DARKER, DARK)
    draw = ImageDraw.Draw(img)

    color = ORANGE
    header_footer(draw, "TRILHA DEVOPSRAIZ", color)

    title_font = ImageFont.truetype(FONT_BOLD, 56)
    y = 200
    draw.text((60, y), "Por que criei", font=title_font, fill=WHITE)
    y += 70
    draw.text((60, y), "uma Trilha", font=title_font, fill=color)
    y += 70
    draw.text((60, y), "(e não um curso)", font=title_font, fill=color)

    y += 100

    sub_font = ImageFont.truetype(FONT_BOLD, 30)
    draw.text((60, y), "3 razões diretas:", font=sub_font, fill=YELLOW)

    y += 80

    razoes = [
        ("01", "Ebook você lê no seu ritmo",
         "Curso você aperta play e finge entender. Ebook você para, relê, testa.", PURPLE),
        ("02", "Código em texto você COPIA",
         "Pro vídeo você pausa e redigita? Tempo perdido. No ebook é Ctrl+C.", GREEN),
        ("03", "Preço justo",
         "Curso de DevOps no mercado custa R$1.500. A Trilha completa é uma fração.", ORANGE),
    ]

    for num, titulo, desc, cor in razoes:
        # Número numa box grande
        box_size = 80
        draw.rounded_rectangle([60, y, 60 + box_size, y + box_size],
                               radius=16, fill=cor)
        nf = ImageFont.truetype(FONT_BOLD, 38)
        bbox = draw.textbbox((0, 0), num, font=nf)
        nw = bbox[2] - bbox[0]
        nh = bbox[3] - bbox[1]
        draw.text((60 + (box_size - nw) // 2, y + (box_size - nh) // 2 - 4),
                  num, font=nf, fill=WHITE)
        # Título
        tf = ImageFont.truetype(FONT_BOLD, 28)
        draw.text((170, y + 10), titulo, font=tf, fill=WHITE)
        # Descrição
        df = ImageFont.truetype(FONT_REG, 22)
        draw_multiline(draw, desc, 170, y + 50, df, MID, W - 240, 4)
        y += 130

    img.save(OUT_DIR / "28-testemunho-trilha.png", "PNG", optimize=True)
    print(f"  ✓ 28-testemunho-trilha.png")


if __name__ == "__main__":
    print("Gerando PNGs preventivos pros posts únicos:")
    day_18_junior_senior()
    day_23_checklist_pleno()
    day_28_testemunho_trilha()
    print("\nPróximo passo: atualizar creative_filename_for em instagram_publisher.py:")
    print("  18: '18-frase-junior-pleno-senior.png',")
    print("  23: '23-checklist-devops-pleno.png',")
    print("  28: '28-testemunho-trilha.png',")
