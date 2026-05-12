# AULA BÔNUS — Docker → Azure DevOps → AKS em 12 minutos

> **Canal:** @DevOpsRaiz  ·  **Apresentador:** Mateo (HeyGen)
> **Duração-alvo:** 12 minutos  ·  **Formato:** YouTube long-form 16:9
> **Plataforma destino:** apenas YouTube (sem Instagram/Shorts)
> **Categoria:** Tutorial técnico hands-on

---

## 0:00 — HOOK (15s)

Imagina dar `git push` na branch main e em 4 minutos a sua API tá rodando em produção, num cluster Kubernetes da Microsoft, com HTTPS, com 2 réplicas, com health-check, com rollback se algo der errado. Hoje eu monto isso do zero. Acompanha.

[PIXAR: foguete decolando de um laptop pequeno e pousando em um castelo de nuvem azul com bandeira AKS — câmera dramática estilo Pixar, faísca laranja DEVOPSRAIZ]

---

## 0:15 — APRESENTAÇÃO (15s)

E aí, eu sou o Mateo do canal DEVOPSRAIZ. Aqui a gente cai dentro de Cloud, DevOps e IA — sem rodeios, em português, com código real que roda. Aula de hoje é bônus: vou montar uma pipeline Azure DevOps que builda Docker, sobe pro ACR, e faz deploy no AKS com rolling update.

[PIXAR: logo DEVOPSRAIZ subindo do chão, faísca laranja, depois zoom out mostrando 3 caixinhas conectadas: "DOCKER" → "AZURE DEVOPS" → "AKS"]

---

## 0:30 — A ARQUITETURA EM 90 SEGUNDOS

Antes de meter mão no código, deixa eu te mostrar o desenho do que a gente vai construir.

Tem 4 pedaços. Da esquerda pra direita: seu repositório Git (Azure Repos ou GitHub), conectado ao Azure DevOps Pipelines — que é o orquestrador. Esse pipeline tem 2 stages: o stage 1 builda a imagem Docker e empurra pro **Azure Container Registry**, o ACR; o stage 2 pega essa imagem do ACR e aplica os manifestos Kubernetes no **AKS** — Azure Kubernetes Service. O AKS roda em 2 nodes pequenos, com o Application Gateway na frente fazendo HTTPS e roteando pra service interno.

Custo médio dessa stack pra hobby? Cerca de US$80 a US$120 por mês. Não é grátis, mas é o piso pra você dizer "tenho experiência real com AKS" numa entrevista.

[PIXAR: diagrama Pixar 3D dos 4 componentes, com pacote brilhante percorrendo as setinhas em câmera lenta]

---

## 2:00 — STEP 1: SUA APP COM DOCKERFILE BEM FEITO (2 min)

Primeiro: o Dockerfile da sua aplicação Python. Não é só `FROM python` e pronto. A diferença entre uma imagem de **800 MB** e uma de **80 MB** está no que eu vou te mostrar agora.

Multi-stage build. Funciona assim: você usa uma imagem "builder" pra instalar suas dependências, e depois copia só o que é necessário pra uma imagem "final" enxuta. O resultado é uma imagem 10 vezes menor, que sobe 10 vezes mais rápido no AKS — e que cobra menos do seu plano de ACR.

Olha o Dockerfile completo no link da descrição. Os pontos-chave: usuário não-root pra segurança, healthcheck integrado pro Docker engine, e `python:3.12-slim` como base — não é Alpine porque Alpine quebra wheels do pandas e bibliotecas científicas. Slim é o sweet spot.

[PIXAR: tartaruga Pixar fazendo "cura emagrecimento" numa baleia gigante de Docker — antes pesa 800kg, depois pesa 80kg]

---

## 4:00 — STEP 2: AZURE DEVOPS — CRIANDO PROJECT E CONNECTIONS (2 min)

Bora pro portal Azure DevOps. Cria um projeto novo. Dentro dele, vai em **Project Settings → Service Connections**. Você precisa criar 2.

**Service Connection 1:** Docker Registry, escolhe "Azure Container Registry", autentica com sua conta Azure e seleciona o ACR. Dá o nome de `devopsraiz-acr-connection` — esse nome vai bater com o YAML.

**Service Connection 2:** Kubernetes, escolhe "Azure Subscription", seleciona o cluster AKS, e o namespace `production`. Nome: `devopsraiz-aks-connection`.

Esses 2 connections é o que dá permissão pro pipeline conversar com seu ACR e seu AKS. Sem eles, o pipeline quebra com 401. Anota.

[PIXAR: 2 chaves girando em fechaduras coloridas — uma azul ACR, outra roxa AKS, ambas se abrem com som de "click" satisfatório]

---

## 6:00 — STEP 3: O YAML DA PIPELINE (3 min — peça central)

Agora a peça central da aula. O `azure-pipelines.yml` mora na raiz do seu repositório. Quando você commita esse arquivo, o Azure DevOps detecta automaticamente e cria o pipeline.

Olha o que esse YAML faz em 3 estágios:

**Stage Build** — roda em um agent Ubuntu 22.04. Faz login no ACR usando o service connection, faz `docker build` da imagem, e dá `docker push` com 2 tags: o BuildId único e `latest`. Por que 2 tags? Porque o BuildId é a sua "fonte da verdade" pra rollback, e o `latest` é conveniência pra dev local. Depois publica os manifestos Kubernetes como artifact pra próxima stage consumir.

**Stage Deploy** — agora a mágica. A task `KubernetesManifest@1` pega os YAMLs do artifact, substitui o `image:` pelo valor com a tag do build atual, e aplica no AKS via `kubectl apply --record`. O Kubernetes detecta a mudança da tag de imagem e faz **rolling update**: sobe um pod novo, espera ele ficar `Ready` (via readinessProbe), aí derruba um pod antigo. Zero downtime.

Por último, a task `Kubernetes@1` faz `kubectl rollout status` com timeout de 3 minutos. Se o rollout não terminar nesse tempo, o pipeline falha — e a Azure DevOps marca o deploy como "failed". Você fica sabendo na hora.

[PIXAR: esteira fabril Pixar com pacote de código entrando bagunçado, passando por 2 portas mágicas "BUILD" e "DEPLOY", e saindo brilhante voando pra um castelo "AKS"]

---

## 9:00 — STEP 4: OS MANIFESTOS KUBERNETES (2 min)

3 arquivos. Todos na pasta `k8s/` do seu repo.

**deployment.yaml** — descreve o `Deployment` com 2 réplicas, strategy `RollingUpdate` com `maxUnavailable: 0` (pra zero downtime de verdade), resources com `requests` e `limits`, e os 2 probes — `readinessProbe` no `/health` pra tirar do load balancer enquanto sobe, `livenessProbe` no mesmo endpoint pra reiniciar se travar. O `imagePullSecrets` aponta pro secret `acr-pull-secret` que o AKS já tem provisionado se você fez `az aks update --attach-acr` na hora do setup.

**service.yaml** — Service tipo `ClusterIP` na porta 80, mapeando pra `targetPort: 8000` do container. Por que ClusterIP e não LoadBalancer? Porque na frente vem o Ingress, próximo ponto.

**ingress.yaml** — usa o Application Gateway Ingress Controller, o AGIC, que vem como add-on do AKS. Define o host `api.devopsraiz.com.br`, redireciona HTTP pra HTTPS, configura o healthcheck no `/health` e usa cert-manager pra gerar certificado Let's Encrypt automaticamente.

Os 3 arquivos completos tão na descrição. Copia e cola — só troca os nomes de domínio e namespace.

[PIXAR: 3 blueprints Pixar 3D girando em volta de um castelo AKS, cada um se encaixando em uma parte específica do castelo]

---

## 11:00 — O DEPLOY REAL: `git push` + 4 MINUTOS

Hora da verdade. Você commita o azure-pipelines.yml e os manifestos.

```
git add azure-pipelines.yml Dockerfile k8s/
git commit -m "feat: pipeline AKS"
git push origin main
```

Azure DevOps detecta o push, dispara o pipeline. Stage Build em ~1m30s. Stage Deploy em ~2 minutos. Total: menos de 4 minutos da sua máquina até o AKS rodando a nova versão.

Você pode acompanhar tudo em tempo real no Azure DevOps Pipelines, ou rodando no terminal:

```
kubectl get pods -n production -w
```

Quando você ver os pods com idade pequena e status `Running`, parabéns — você acabou de fazer um deploy enterprise-grade.

[PIXAR: cronômetro Pixar girando rápido, contagem de 4 minutos, "DEPLOY OK" aparecendo em verde no final com som de fanfarra]

---

## 11:45 — CTA EBOOK + TRILHA + CUPOM (45s)

Se essa aula te ajudou, segue o canal aí no botão vermelho — toda semana sai aula desse nível.

Tenho um **ebook gratuito** que te leva do zero até essa publicação em FastAPI (a parte da aplicação que essa pipeline está empacotando). Link na descrição.

E se você quer o caminho completo — multi-cloud, IA, segurança, observabilidade — é a Trilha DEVOPSRAIZ no Hotmart. Como você tá assistindo aqui, usa o cupom **SEGUIDOR80** no checkout e pega 80% off: de R$ 199,99 por **R$ 39,99**.

Tira-dúvidas direto comigo no WhatsApp **(11) 96482-3126**.

Valeu raiz, e te vejo na próxima.

[PIXAR: Mateo acenando com cupom laranja 80% off girando ao lado dele e WhatsApp aparecendo embaixo, faísca laranja final]

---

## METADADOS YOUTUBE

- **Título:** Docker → Azure DevOps → AKS em 12 minutos | Pipeline completa com YAML pronto

- **Descrição:**

    Como montar uma pipeline Azure DevOps que builda Docker, sobe imagem
    pro Azure Container Registry (ACR) e faz deploy no AKS com rolling
    update e healthcheck. Tudo testado, com YAML pronto pra copiar.

    ⬇ ARQUIVOS COMPLETOS PRA COPIAR ⬇

    ▸ azure-pipelines.yml: https://github.com/DevOpsRaizOficial/marketing/blob/main/roteiros/bonus_azuredevops_aks/azure-pipelines.yml
    ▸ Dockerfile: https://github.com/DevOpsRaizOficial/marketing/blob/main/roteiros/bonus_azuredevops_aks/Dockerfile
    ▸ k8s/deployment.yaml: https://github.com/DevOpsRaizOficial/marketing/blob/main/roteiros/bonus_azuredevops_aks/k8s/deployment.yaml
    ▸ k8s/service.yaml: https://github.com/DevOpsRaizOficial/marketing/blob/main/roteiros/bonus_azuredevops_aks/k8s/service.yaml
    ▸ k8s/ingress.yaml: https://github.com/DevOpsRaizOficial/marketing/blob/main/roteiros/bonus_azuredevops_aks/k8s/ingress.yaml

    ► EBOOK GRATUITO: https://devopsraiz.com.br/ebook-gratis
    ► TRILHA COMPLETA com 80% OFF (cupom SEGUIDOR80): https://go.hotmart.com/S105313699A
    ► WhatsApp tira-dúvidas: (11) 96482-3126
    ► Instagram: https://instagram.com/devopsraiz_oficial

    📂 ESTRUTURA DE PASTAS ESPERADA NO SEU REPO:

        /
        ├─ azure-pipelines.yml
        ├─ Dockerfile
        ├─ main.py            (sua app FastAPI)
        ├─ requirements.txt
        └─ k8s/
            ├─ deployment.yaml
            ├─ service.yaml
            └─ ingress.yaml

    🕒 TIMESTAMPS:
    00:00 Hook
    00:30 Arquitetura
    02:00 Dockerfile multi-stage
    04:00 Service Connections Azure DevOps
    06:00 azure-pipelines.yml explicado
    09:00 Manifestos Kubernetes
    11:00 Deploy real em 4 minutos
    11:45 Ebook + cupom SEGUIDOR80

    🔧 PRÉ-REQUISITOS:
    - Conta Azure com permissão Owner ou Contributor
    - AKS provisionado (qualquer SKU, mesmo Free)
    - ACR provisionado e anexado ao AKS (`az aks update --attach-acr`)
    - Azure DevOps Organization (gratuito até 5 usuários)
    - Aplicação FastAPI (ver ebook gratuito pra construir do zero)

    🧪 TESTADO EM:
    - Azure DevOps Services (maio/2026)
    - AKS v1.30, região eastus2
    - ACR Basic tier
    - Application Gateway Ingress Controller v1.7

    #azuredevops #aks #kubernetes #docker #devops #cicd #devopsraiz #azure #cloud

- **Tags:** azure devops, aks, kubernetes, docker, ci cd, devops, azure, cloud, devopsraiz, pipeline, yaml, deploy, fastapi, python, container, microsserviços

- **Categoria YouTube:** 27 (Education)

- **Thumb sugerida:**
    - Fundo dark #020617
    - À esquerda: logo Docker, seta laranja, logo Azure DevOps, seta laranja, logo Kubernetes — tudo em ícones 3D estilo Pixar
    - À direita: texto grande em Helvetica-Bold "AZURE DEVOPS + AKS" branco com sublinhado laranja
    - Embaixo: "12 MIN · YAML PRONTO" em barra laranja
    - Mateo close no canto inferior direito apontando pra setinha

- **Cards YouTube:**
    - 2:00 → card pro ebook gratuito (capa)
    - 6:00 → card pro vídeo "Docker do zero" (Aula 06 da série 30 dias)
    - 11:00 → card pra Trilha completa

- **End screen:**
    - Próximo vídeo: "Kubernetes em 10 min" (Aula 08)
    - Inscrever-se @DevOpsRaiz
    - Link externo: ebook gratuito

- **Playlist destino:** "Bônus técnicos" (criar nova playlist no canal)
- **Publishing:** unlisted primeiro, public depois de revisão
- **Comments:** ativados, com fixed pin "Cupom SEGUIDOR80 dá 80% off na Trilha"
