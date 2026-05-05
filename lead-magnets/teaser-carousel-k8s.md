# Carrossel teaser do lead magnet K8S

**Quando postar:** logo após terminar o setup do ManyChat. Ideal num horário de pico (8h ou 19h BRT). É um post EXTRA fora do calendário fixo de 30 dias — substitui um Story ou complementa.

**Formato:** Carrossel 5 slides 1080x1350.
**Pilar:** Educacional + Captura
**Hashtags:** #devops #kubernetes #docker #k8s #crashloopbackoff #devopsraiz

## Legenda completa (pra colar no Instagram)

```
TODO dev junior já pegou um desses no kubectl describe pod:

→ CrashLoopBackOff
→ ImagePullBackOff
→ OOMKilled
→ Pending (Unschedulable)
→ Evicted

Cada um tem causa raiz diferente. E uma forma RÁPIDA de diagnosticar.

Eu compilei os 10 erros mais comuns de Kubernetes num PDF gratuito de 7 páginas, com:

✅ O que é cada erro
✅ Por que rola na prática
✅ Como resolver em 5 minutos (com comandos kubectl prontos)

É um recorte do Ebook 2 da Trilha DEVOPSRAIZ.

Quer pegar de graça?

💬 Comenta K8S nesse post que mando o PDF direto no seu DM 📨

Bônus: quem entrar na lista pelo K8S agora ganha cupom FUNDADOR 20% off na Trilha completa (válido só pros 100 primeiros).

#devops #cloud #aws #kubernetes #k8s #docker #terraform #devbrasil #carreiratech #devopsraiz
```

**CTA principal:** Comentar `K8S`
**CTA secundário:** Salvar + Marcar amigo dev

## Slides (visual + texto)

### Slide 1 — Capa (HOOK forte)
- Fundo: gradient escuro + acentos vermelhos (sangue dos erros K8s)
- Header: pill "EBOOK 2 · DOCKER/K8S" laranja
- Título grande: **"Já viu seu pod assim?"**
- Subtitle: "10 erros que matam o cluster"
- Mock visual: terminal com `kubectl get pods` mostrando todos em estado de erro (CrashLoopBackOff, OOMKilled, etc)

### Slide 2 — A dor real
- Título: **"Junior em K8s = sangue suor e lágrimas"**
- 4 boxes coloridos (vermelho/amarelo/laranja/roxo) cada um com 1 erro:
  - 🔴 CrashLoopBackOff
  - 🟡 OOMKilled
  - 🟠 Pending (Unschedulable)
  - 🟣 Liveness probe matando o pod
- Texto inferior: "Cada um tem causa raiz diferente. E fix diferente."

### Slide 3 — A oferta (PDF gratuito)
- Título: **"Pega o PDF aí"**
- Mock de capa do PDF (renderiza o cover real)
- Bullet list:
  - 7 páginas, técnico e direto
  - 10 erros K8s + diagnóstico + fix
  - Comandos kubectl prontos pra copy-paste
  - Recorte real do Ebook 2 da Trilha
- Tag laranja: "100% gratuito"

### Slide 4 — Como pegar
- Título: **"Como você recebe?"**
- Step 1: 💬 Comenta `K8S` nesse post
- Step 2: 📨 Recebe DM em 5s
- Step 3: 📧 Manda seu email
- Step 4: 📥 PDF cai no seu DM
- Texto inferior: "Em 30 segundos você tá com o PDF"

### Slide 5 — Bônus + CTA final
- Título: **"Bônus pra primeiros 100"**
- Box laranja grande:
  - **CUPOM FUNDADOR 20% OFF**
  - Trilha completa (6 ebooks)
  - Válido só essa semana
- Footer:
  - "Comenta K8S agora 👇"
  - @devopsraiz_oficial

## Arquivos visuais a gerar

Quando aprovar essa estrutura, eu rodo o script de geração de slides
(`build_carousel_teaser_k8s.py`) que cria os 5 PNGs em `/criativos/`
seguindo o mesmo padrão visual dos outros carrosséis. Naming:

- `extra-01-teaser-k8s-slide-01.png` (capa)
- `extra-01-teaser-k8s-slide-02.png` (a dor)
- `extra-01-teaser-k8s-slide-03.png` (oferta PDF)
- `extra-01-teaser-k8s-slide-04.png` (como pegar)
- `extra-01-teaser-k8s-slide-05.png` (cupom + CTA)

Pra publicar via API: usa `instagram_publisher.py publish` apontando
pra esses arquivos manualmente, ou adiciona ao `CAROUSEL_SLIDES_MAP`
como `0` (post extra).
