"""
Gera 5 slides PNG (1080x1350) pro carrossel teaser do lead magnet K8S.

Naming: extra-01-teaser-k8s-slide-NN.png
Posta como Carousel Instagram com CTA "Comenta K8S que mando o PDF".
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path("/sessions/sweet-friendly-maxwell/mnt/Ebooks-DevopsRaiz/marketing/criativos")
OUT_DIR.mkdir(exist_ok=True, parents=True)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# Paleta DevOpsRaiz
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
EBOOK_TAG = "EBOOK 2 • DOCKER/K8S"
COLOR = ORANGE  # cor do ebook 2


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


def base_canvas(slide_num, total):
    """Header DEVOPSRAIZ + pill + footer com paginação."""
    img = gradient_bg(DARKER, DARK)
    draw = ImageDraw.Draw(img)

    brand = ImageFont.truetype(FONT_BOLD, 26)
    draw.text((60, 50), "DEVOPSRAIZ", font=brand, fill=COLOR)

    pill_font = ImageFont.truetype(FONT_BOLD, 20)
    pill(draw, EBOOK_TAG, 60, 95, pill_font, WHITE, COLOR)

    draw.rectangle([60, 140, W - 60, 142], fill=COLOR)

    # Footer
    draw.rectangle([0, H - 90, W, H], fill=DARKER)
    draw.rectangle([0, H - 93, W, H - 90], fill=COLOR)

    handle_font = ImageFont.truetype(FONT_REG, 22)
    draw.text((60, H - 70), "@devopsraiz_oficial", font=handle_font, fill=LIGHT)

    page_font = ImageFont.truetype(FONT_BOLD, 22)
    page_txt = f"{slide_num} / {total}"
    bbox = draw.textbbox((0, 0), page_txt, font=page_font)
    tw = bbox[2] - bbox[0]
    draw.text((W - tw - 60, H - 70), page_txt, font=page_font, fill=MID)

    return img, draw


# =============================================================================
# Slide 1 — CAPA — "Já viu seu pod assim?"
# =============================================================================
def slide_01():
    img, draw = base_canvas(1, 5)

    # Hook título
    title_font = ImageFont.truetype(FONT_BOLD, 78)
    y = 200
    draw.text((60, y), "Já viu seu pod", font=title_font, fill=WHITE)
    y += 90
    draw.text((60, y), "assim?", font=title_font, fill=RED)

    y += 130

    # Mock terminal kubectl
    term_x, term_y, term_w, term_h = 60, y, W - 120, 480
    draw.rounded_rectangle([term_x, term_y, term_x + term_w, term_y + term_h],
                           radius=20, fill=(10, 14, 30))
    # Barra superior do "terminal"
    draw.rounded_rectangle([term_x, term_y, term_x + term_w, term_y + 50],
                           radius=20, fill=(40, 50, 70))
    # Botões macOS-style
    for cx, color in [(term_x + 30, (255, 95, 86)),
                      (term_x + 60, (255, 189, 46)),
                      (term_x + 90, (39, 201, 63))]:
        draw.ellipse([cx - 8, term_y + 17, cx + 8, term_y + 33], fill=color)

    # Conteúdo terminal
    cmd_font = ImageFont.truetype(FONT_MONO, 26)
    line_y = term_y + 80
    draw.text((term_x + 30, line_y), "$ kubectl get pods", font=cmd_font, fill=GREEN)
    line_y += 42

    pods = [
        ("api-server-7d8c", "0/1", "CrashLoopBackOff", RED),
        ("worker-queue-3a4f", "0/1", "OOMKilled", YELLOW),
        ("frontend-9bc1", "0/1", "ImagePullBackOff", RED),
        ("redis-cache-22d", "0/1", "Pending", YELLOW),
        ("notif-svc-aaa", "0/1", "Evicted", ORANGE),
    ]
    pod_font = ImageFont.truetype(FONT_MONO, 22)
    for name, ready, status, color in pods:
        draw.text((term_x + 30, line_y), f"{name:24} {ready}", font=pod_font, fill=LIGHT)
        # status colorido
        bbox = draw.textbbox((0, 0), status, font=pod_font)
        draw.text((term_x + 540, line_y), status, font=pod_font, fill=color)
        line_y += 38

    line_y += 10
    draw.text((term_x + 30, line_y), "$ _", font=cmd_font, fill=WHITE)

    # Subtítulo embaixo
    sub_y = term_y + term_h + 30
    sub_font = ImageFont.truetype(FONT_BOLD, 38)
    draw.text((60, sub_y), "10 erros que matam o cluster", font=sub_font, fill=LIGHT)

    img.save(OUT_DIR / "extra-01-teaser-k8s-slide-01.png", "PNG", optimize=True)


# =============================================================================
# Slide 2 — A DOR — Junior em K8s
# =============================================================================
def slide_02():
    img, draw = base_canvas(2, 5)

    title_font = ImageFont.truetype(FONT_BOLD, 64)
    y = 200
    draw.text((60, y), "Junior em K8s =", font=title_font, fill=WHITE)
    y += 80
    draw.text((60, y), "sangue, suor", font=title_font, fill=RED)
    y += 80
    draw.text((60, y), "e lágrimas", font=title_font, fill=RED)

    y += 130

    # Grid 2x2 de erros com cores diferentes
    erros = [
        ("CrashLoopBackOff", "container morre, K8s reinicia, loop", RED),
        ("OOMKilled", "estourou memória, kernel matou", YELLOW),
        ("Pending", "nenhum node com recurso", ORANGE),
        ("Liveness probe", "K8s mata achando que travou", PURPLE),
    ]
    box_w = (W - 60 * 2 - 30) // 2
    box_h = 180
    for i, (titulo, sub, cor) in enumerate(erros):
        col = i % 2
        row = i // 2
        bx = 60 + col * (box_w + 30)
        by = y + row * (box_h + 25)
        draw.rounded_rectangle([bx, by, bx + box_w, by + box_h], radius=18,
                               fill=(20, 26, 42), outline=cor, width=4)
        # Faixa colorida lateral
        draw.rectangle([bx, by + 18, bx + 8, by + box_h - 18], fill=cor)
        # Título
        et_font = ImageFont.truetype(FONT_BOLD, 28)
        draw.text((bx + 30, by + 28), titulo, font=et_font, fill=WHITE)
        # Subtítulo
        es_font = ImageFont.truetype(FONT_REG, 20)
        draw_multiline(draw, sub, bx + 30, by + 75, es_font, MID, box_w - 50, 6)

    # Texto inferior
    sub_y = y + 2 * box_h + 60
    sf = ImageFont.truetype(FONT_REG, 28)
    draw.text((60, sub_y), "Cada um tem causa raiz e fix diferentes.", font=sf, fill=LIGHT)

    img.save(OUT_DIR / "extra-01-teaser-k8s-slide-02.png", "PNG", optimize=True)


# =============================================================================
# Slide 3 — A OFERTA — PDF gratuito
# =============================================================================
def slide_03():
    img, draw = base_canvas(3, 5)

    title_font = ImageFont.truetype(FONT_BOLD, 76)
    y = 220
    draw.text((60, y), "Pega o PDF", font=title_font, fill=WHITE)
    y += 90
    draw.text((60, y), "aí 👇", font=title_font, fill=COLOR)

    y += 140

    # Mock capa do PDF (placeholder visual)
    pdf_w, pdf_h = 320, 420
    pdf_x = (W - pdf_w) // 2
    pdf_y = y
    # Sombra
    draw.rectangle([pdf_x + 8, pdf_y + 8, pdf_x + pdf_w + 8, pdf_y + pdf_h + 8],
                   fill=(0, 0, 0))
    # PDF cover
    draw.rectangle([pdf_x, pdf_y, pdf_x + pdf_w, pdf_y + pdf_h], fill=DARKER)
    # Top stripe
    draw.rectangle([pdf_x, pdf_y, pdf_x + pdf_w, pdf_y + 8], fill=COLOR)
    # Título no PDF
    pdf_title = ImageFont.truetype(FONT_BOLD, 26)
    pdf_y_text = pdf_y + 60
    draw.text((pdf_x + 30, pdf_y_text), "10 erros", font=pdf_title, fill=WHITE)
    pdf_y_text += 35
    draw.text((pdf_x + 30, pdf_y_text), "que mandam", font=pdf_title, fill=COLOR)
    pdf_y_text += 35
    draw.text((pdf_x + 30, pdf_y_text), "dev junior pro", font=pdf_title, fill=COLOR)
    pdf_y_text += 35
    draw.text((pdf_x + 30, pdf_y_text), "CrashLoopBackoff", font=pdf_title, fill=RED)

    pdf_sub = ImageFont.truetype(FONT_REG, 16)
    pdf_y_text += 60
    draw_multiline(draw, "Os bugs mais comuns de Kubernetes — e como resolver em 5 minutos.",
                   pdf_x + 30, pdf_y_text, pdf_sub, LIGHT, pdf_w - 60, 4)

    # Footer do PDF
    pf = ImageFont.truetype(FONT_BOLD, 14)
    draw.text((pdf_x + 30, pdf_y + pdf_h - 50), "DEVOPSRAIZ", font=pf, fill=COLOR)

    # Bullets ao lado direito
    bullets_y = pdf_y + 30
    bullet_font = ImageFont.truetype(FONT_REG, 22)
    bullets = [
        "✅ 7 páginas, técnico e direto",
        "✅ 10 erros K8s com fix completo",
        "✅ Comandos kubectl prontos",
        "✅ Recorte do Ebook 2 da Trilha",
    ]
    for b in bullets:
        draw.text((pdf_x + pdf_w + 40, bullets_y), b, font=bullet_font, fill=LIGHT)
        bullets_y += 50

    # Tag "100% gratuito"
    tag_font = ImageFont.truetype(FONT_BOLD, 24)
    pill(draw, "100% GRATUITO", pdf_x + pdf_w + 40, bullets_y + 20, tag_font, WHITE, GREEN)

    img.save(OUT_DIR / "extra-01-teaser-k8s-slide-03.png", "PNG", optimize=True)


# =============================================================================
# Slide 4 — COMO PEGAR — 4 steps
# =============================================================================
def slide_04():
    img, draw = base_canvas(4, 5)

    title_font = ImageFont.truetype(FONT_BOLD, 70)
    y = 200
    draw.text((60, y), "Como você", font=title_font, fill=WHITE)
    y += 80
    draw.text((60, y), "recebe?", font=title_font, fill=COLOR)

    y += 130

    steps = [
        ("1", "Comenta K8S nesse post", "💬"),
        ("2", "Recebe DM em 5 segundos", "📨"),
        ("3", "Manda seu email", "📧"),
        ("4", "PDF cai no seu DM", "📥"),
    ]
    sf = ImageFont.truetype(FONT_BOLD, 32)
    nf = ImageFont.truetype(FONT_BOLD, 36)
    ef = ImageFont.truetype(FONT_REG, 50)

    for n, txt, emoji in steps:
        # Box numerada
        box_size = 70
        draw.rounded_rectangle([60, y, 60 + box_size, y + box_size], radius=14, fill=COLOR)
        bbox = draw.textbbox((0, 0), n, font=nf)
        nw = bbox[2] - bbox[0]
        nh = bbox[3] - bbox[1]
        draw.text((60 + (box_size - nw) // 2, y + (box_size - nh) // 2 - 4),
                  n, font=nf, fill=WHITE)
        # Texto
        draw.text((160, y + 18), txt, font=sf, fill=LIGHT)
        # Emoji do passo
        draw.text((W - 130, y + 8), emoji, font=ef, fill=WHITE)
        y += 100

    # Ribbon final
    y += 30
    rib_h = 80
    draw.rounded_rectangle([60, y, W - 60, y + rib_h], radius=18, fill=DARK)
    rf = ImageFont.truetype(FONT_BOLD, 28)
    txt = "Em 30 segundos você tá com o PDF"
    bbox = draw.textbbox((0, 0), txt, font=rf)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y + 25), txt, font=rf, fill=COLOR)

    img.save(OUT_DIR / "extra-01-teaser-k8s-slide-04.png", "PNG", optimize=True)


# =============================================================================
# Slide 5 — CUPOM + CTA
# =============================================================================
def slide_05():
    img, draw = base_canvas(5, 5)

    title_font = ImageFont.truetype(FONT_BOLD, 64)
    y = 200
    draw.text((60, y), "Bônus pra os", font=title_font, fill=WHITE)
    y += 80
    draw.text((60, y), "100 primeiros", font=title_font, fill=COLOR)

    y += 130

    # Box gigante do cupom
    box_h = 380
    draw.rounded_rectangle([60, y, W - 60, y + box_h], radius=24, fill=COLOR)

    cupom_title = ImageFont.truetype(FONT_BOLD, 56)
    txt = "CUPOM FUNDADOR"
    bbox = draw.textbbox((0, 0), txt, font=cupom_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y + 50), txt, font=cupom_title, fill=WHITE)

    # 20% OFF gigante
    off_font = ImageFont.truetype(FONT_BOLD, 130)
    off_txt = "20% OFF"
    bbox = draw.textbbox((0, 0), off_txt, font=off_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y + 130), off_txt, font=off_font, fill=WHITE)

    # Subtítulo
    sub_font = ImageFont.truetype(FONT_BOLD, 30)
    sub_txt = "na Trilha completa"
    bbox = draw.textbbox((0, 0), sub_txt, font=sub_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y + 280), sub_txt, font=sub_font, fill=WHITE)

    # Validade
    val_font = ImageFont.truetype(FONT_REG, 22)
    val_txt = "válido só pros 100 primeiros • essa semana"
    bbox = draw.textbbox((0, 0), val_txt, font=val_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y + 330), val_txt, font=val_font, fill=WHITE)

    # CTA final
    y += box_h + 40
    cta_font = ImageFont.truetype(FONT_BOLD, 42)
    cta_txt = "Comenta K8S agora 👇"
    bbox = draw.textbbox((0, 0), cta_txt, font=cta_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), cta_txt, font=cta_font, fill=WHITE)

    img.save(OUT_DIR / "extra-01-teaser-k8s-slide-05.png", "PNG", optimize=True)


if __name__ == "__main__":
    print("Gerando 5 slides do teaser K8S...")
    slide_01()
    print("  ✓ Slide 1 — capa")
    slide_02()
    print("  ✓ Slide 2 — dor")
    slide_03()
    print("  ✓ Slide 3 — oferta")
    slide_04()
    print("  ✓ Slide 4 — como pegar")
    slide_05()
    print("  ✓ Slide 5 — cupom + CTA")
    print(f"\nArquivos em {OUT_DIR}")
    for f in sorted(OUT_DIR.glob("extra-01-teaser-k8s-slide-*.png")):
        print(f"  - {f.name} ({f.stat().st_size // 1024} KB)")
