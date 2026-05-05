"""
Gera o meme do Dia 6 — dev junior vs Kubernetes (1080x1350).
Save em /criativos/06-meme-k8s-junior.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("/sessions/sweet-friendly-maxwell/mnt/Ebooks-DevopsRaiz/marketing/criativos/06-meme-k8s-junior.png")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

W, H = 1080, 1350
DARKER = (2, 6, 23)
DARK = (15, 23, 42)
LIGHT = (226, 232, 240)
MID = (100, 116, 139)
WHITE = (255, 255, 255)
ORANGE = (249, 115, 22)
RED = (239, 68, 68)
YELLOW = (245, 158, 11)
GREEN = (16, 185, 129)


def gradient(c1, c2):
    img = Image.new("RGB", (W, H), c1)
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
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


img = gradient(DARKER, DARK)
draw = ImageDraw.Draw(img)

# Header marca
brand = ImageFont.truetype(FONT_BOLD, 28)
draw.text((60, 50), "DEVOPSRAIZ", font=brand, fill=ORANGE)

# Pill ebook
pill_font = ImageFont.truetype(FONT_BOLD, 20)
pill_text = "EBOOK 2 • DOCKER/K8S"
bbox = draw.textbbox((0, 0), pill_text, font=pill_font)
pw, ph = bbox[2] - bbox[0] + 44, bbox[3] - bbox[1] + 20
draw.rounded_rectangle([60, 95, 60 + pw, 95 + ph], radius=ph // 2, fill=ORANGE)
draw.text((82, 99), pill_text, font=pill_font, fill=WHITE)

# Divisor
draw.rectangle([60, 145, W - 60, 147], fill=ORANGE)

# Título top do meme
title_font = ImageFont.truetype(FONT_BOLD, 44)
y = 200
title = "Todo dev júnior na primeira vez que roda"
for line in wrap(title, title_font, W - 120, draw):
    draw.text((60, y), line, font=title_font, fill=WHITE)
    bbox = draw.textbbox((0, 0), line, font=title_font)
    y += (bbox[3] - bbox[1]) + 8
y += 16

# Comando em mono num retângulo
cmd_font = ImageFont.truetype(FONT_MONO, 38)
cmd_text = "$ kubectl describe pod"
bbox = draw.textbbox((0, 0), cmd_text, font=cmd_font)
cw = bbox[2] - bbox[0]
ch = bbox[3] - bbox[1]
box_w = cw + 60
box_h = ch + 36
draw.rounded_rectangle([60, y, 60 + box_w, y + box_h], radius=14, fill=(30, 41, 59))
draw.text((90, y + 14), cmd_text, font=cmd_font, fill=GREEN)
y += box_h + 50

# "E aparece..."
sub_font = ImageFont.truetype(FONT_REG, 32)
draw.text((60, y), "E aparece...", font=sub_font, fill=MID)
y += 60

# Erros K8s — cada um numa pill colorida
errors = [
    ("CrashLoopBackOff", RED),
    ("ImagePullBackOff", RED),
    ("OOMKilled", YELLOW),
    ("Pending (Unschedulable)", YELLOW),
    ("Evicted", ORANGE),
]
err_font = ImageFont.truetype(FONT_MONO, 32)
for txt, col in errors:
    bbox = draw.textbbox((0, 0), txt, font=err_font)
    pw = bbox[2] - bbox[0] + 40
    ph = bbox[3] - bbox[1] + 24
    draw.rounded_rectangle([60, y, 60 + pw, y + ph], radius=ph // 2, fill=col)
    draw.text((80, y + 8), txt, font=err_font, fill=WHITE)
    y += ph + 18

y += 20

# Reação meme
reac_font = ImageFont.truetype(FONT_BOLD, 36)
draw.text((60, y), "👨‍💻 \"Achei que era só `npm start`...\"", font=reac_font, fill=LIGHT)

# Footer
draw.rectangle([0, H - 90, W, H], fill=DARKER)
draw.rectangle([0, H - 93, W, H - 90], fill=ORANGE)

handle_font = ImageFont.truetype(FONT_REG, 22)
draw.text((60, H - 70), "@devopsraiz_oficial", font=handle_font, fill=LIGHT)

cta_font = ImageFont.truetype(FONT_BOLD, 22)
cta = "Ebook 2 • Trilha DEVOPSRAIZ"
bbox = draw.textbbox((0, 0), cta, font=cta_font)
tw = bbox[2] - bbox[0]
draw.text((W - tw - 60, H - 70), cta, font=cta_font, fill=ORANGE)

img.save(OUT, "PNG", optimize=True)
print(f"✓ Meme salvo: {OUT}")
