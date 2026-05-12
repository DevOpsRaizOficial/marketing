"""
Gera 2 diagramas explicativos da aula bônus Docker→AzureDevOps→AKS.

Saídas:
  - arquitetura.png   (1920x1080, usar como tela cheia em 0:30-2:00)
  - pipeline-flow.png (1920x1080, usar como tela cheia em 6:00-9:00)

Paleta DevOpsRaiz: dark theme + laranja accent.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).parent
DARK_BG = "#020617"
DARK_2 = "#0F172A"
SLATE = "#1E293B"
LIGHT = "#E2E8F0"
MID = "#94A3B8"
ORANGE = "#F97316"
BLUE = "#3B82F6"
GREEN = "#10B981"
PURPLE = "#A855F7"
YELLOW = "#F59E0B"


def setup_axes():
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 56)
    ax.axis("off")
    return fig, ax


def caixa(ax, x, y, w, h, texto, cor=DARK_2, borda=ORANGE, txt_cor=LIGHT,
           tamanho=14, bold=True):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.5",
        linewidth=2, edgecolor=borda, facecolor=cor,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, texto,
             ha="center", va="center", color=txt_cor,
             fontsize=tamanho, fontweight="bold" if bold else "normal",
             family="sans-serif")


def seta(ax, x1, y1, x2, y2, label="", cor=ORANGE):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=22,
        linewidth=2.5, color=cor,
    )
    ax.add_patch(arr)
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.2, label,
                 ha="center", va="bottom", color=cor,
                 fontsize=11, fontweight="bold", style="italic")


# ==============================================================================
# Diagrama 1 — Arquitetura geral
# ==============================================================================
def diagrama_arquitetura():
    fig, ax = setup_axes()

    # Título
    ax.text(50, 52, "Docker → Azure DevOps → AKS",
             ha="center", color=LIGHT, fontsize=30, fontweight="bold")
    ax.text(50, 48.5,
             "Pipeline completa: do git push ao deploy em ~4 minutos",
             ha="center", color=MID, fontsize=14, style="italic")

    # Linha superior: o fluxo principal
    # 1. Dev / Git
    caixa(ax, 3, 28, 14, 10,
          "DEV LOCAL\n\ngit push origin main",
          cor=DARK_2, borda=BLUE, tamanho=12)

    # 2. Azure Repos
    caixa(ax, 22, 28, 14, 10,
          "AZURE REPOS\n(ou GitHub)\n\nbranch: main",
          cor=DARK_2, borda=BLUE, tamanho=12)

    # 3. Azure DevOps Pipelines (caixa maior, conectando aos 2 destinos)
    caixa(ax, 41, 22, 18, 22,
          "AZURE DEVOPS\nPIPELINES\n\n— Stage 1: Build —\n— Stage 2: Deploy —",
          cor=DARK_2, borda=ORANGE, tamanho=13)

    # 4. ACR (em cima)
    caixa(ax, 65, 36, 14, 8,
          "AZURE\nCONTAINER\nREGISTRY",
          cor=DARK_2, borda=PURPLE, tamanho=12)

    # 5. AKS (em baixo)
    caixa(ax, 65, 22, 14, 8,
          "AKS\nKubernetes Service\nnamespace: production",
          cor=DARK_2, borda=GREEN, tamanho=11)

    # 6. App Gateway + Ingress (mais à direita)
    caixa(ax, 84, 30, 13, 14,
          "APPLICATION\nGATEWAY\n+ INGRESS\n\nHTTPS via\nLet's Encrypt",
          cor=DARK_2, borda=YELLOW, tamanho=11)

    # Setas do fluxo
    seta(ax, 17, 33, 22, 33)
    seta(ax, 36, 33, 41, 33, label="trigger")
    seta(ax, 59, 40, 65, 40, label="docker push")
    seta(ax, 65, 39, 60, 30, cor=PURPLE)  # ACR → Pipeline puxa imagem
    seta(ax, 59, 26, 65, 26, label="kubectl apply")
    seta(ax, 79, 26, 84, 35, label="expose 80→8000", cor=GREEN)

    # Bloco inferior — recursos
    ax.text(50, 17, "STACK", ha="center", color=ORANGE,
             fontsize=18, fontweight="bold")

    stack = [
        ("DOCKERFILE", "Python 3.12-slim multi-stage\nUsuário não-root + healthcheck", BLUE),
        ("PIPELINE", "azure-pipelines.yml\n2 stages, 3 tasks", ORANGE),
        ("MANIFESTOS", "deployment.yaml + service.yaml\n+ ingress.yaml (AGIC)", PURPLE),
        ("CUSTO/MÊS", "~US$ 95 produção\n~US$ 30 hobby (sem App GW)", GREEN),
    ]
    for i, (titulo, corpo, cor) in enumerate(stack):
        x = 3 + i * 24
        caixa(ax, x, 4, 22, 11, f"{titulo}\n\n{corpo}",
              cor=DARK_2, borda=cor, tamanho=11)

    # Footer
    ax.text(50, 1, "@DevOpsRaiz  ·  Trilha DEVOPSRAIZ  ·  Cupom SEGUIDOR80",
             ha="center", color=ORANGE, fontsize=11, fontweight="bold")

    out = OUT / "arquitetura.png"
    fig.savefig(out, dpi=100, facecolor=DARK_BG, bbox_inches="tight",
                 pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {out}")


# ==============================================================================
# Diagrama 2 — Pipeline flow (2 stages explicados)
# ==============================================================================
def diagrama_pipeline_flow():
    fig, ax = setup_axes()

    # Título
    ax.text(50, 53, "azure-pipelines.yml em 2 stages",
             ha="center", color=LIGHT, fontsize=28, fontweight="bold")

    # Stage 1 — Build (esquerda)
    ax.text(25, 47, "STAGE 1 — BUILD", ha="center", color=ORANGE,
             fontsize=18, fontweight="bold")
    ax.text(25, 44.5, "(~ 1m30s)", ha="center", color=MID, fontsize=11,
             style="italic")

    steps_build = [
        "1. checkout: self (clona repo)",
        "2. Docker@2 login no ACR",
        "3. Docker@2 buildAndPush:\n     • tag = $(Build.BuildId)\n     • tag = latest",
        "4. publish: k8s/ como artifact\n     (alimenta Stage 2)",
    ]
    for i, txt in enumerate(steps_build):
        y = 40 - i * 8
        caixa(ax, 5, y, 40, 6, txt, cor=DARK_2, borda=BLUE,
              tamanho=11, bold=False)
        if i < len(steps_build) - 1:
            seta(ax, 25, y, 25, y - 2, cor=BLUE)

    # Stage 2 — Deploy (direita)
    ax.text(75, 47, "STAGE 2 — DEPLOY", ha="center", color=ORANGE,
             fontsize=18, fontweight="bold")
    ax.text(75, 44.5, "(~ 2 min)  ·  só roda se Build = ok",
             ha="center", color=MID, fontsize=11, style="italic")

    steps_deploy = [
        "1. download: artifact 'manifests'",
        "2. KubernetesManifest@1 apply:\n     • deployment.yaml\n     • service.yaml\n     • ingress.yaml",
        "3. substitui $(imageTag) no YAML\n     com tag do BuildId atual",
        "4. Kubernetes@1 rollout status\n     com --timeout=180s\n     (zero downtime garantido)",
    ]
    for i, txt in enumerate(steps_deploy):
        y = 40 - i * 8
        caixa(ax, 55, y, 40, 6, txt, cor=DARK_2, borda=GREEN,
              tamanho=11, bold=False)
        if i < len(steps_deploy) - 1:
            seta(ax, 75, y, 75, y - 2, cor=GREEN)

    # Seta horizontal Stage 1 → Stage 2
    seta(ax, 45, 32, 55, 32, label="dependsOn", cor=ORANGE)

    # Bloco inferior: o que acontece no AKS durante o rollout
    ax.text(50, 11, "DURANTE O ROLLING UPDATE (zero downtime)",
             ha="center", color=ORANGE, fontsize=14, fontweight="bold")

    pods = [
        ("POD v1\nrunning", GREEN),
        ("POD v1\nrunning", GREEN),
        ("POD v2\nready ↑", YELLOW),
        ("POD v2\nrunning", GREEN),
    ]
    for i, (txt, cor) in enumerate(pods):
        x = 22 + i * 14
        caixa(ax, x, 3, 12, 6, txt, cor=DARK_2, borda=cor, tamanho=10)
        if i < len(pods) - 1:
            seta(ax, x + 12, 6, x + 14, 6, cor=MID)

    ax.text(50, 0.5, "@DevOpsRaiz  ·  maxUnavailable: 0  ·  Cupom SEGUIDOR80",
             ha="center", color=ORANGE, fontsize=10, fontweight="bold")

    out = OUT / "pipeline-flow.png"
    fig.savefig(out, dpi=100, facecolor=DARK_BG, bbox_inches="tight",
                 pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {out}")


if __name__ == "__main__":
    diagrama_arquitetura()
    diagrama_pipeline_flow()
