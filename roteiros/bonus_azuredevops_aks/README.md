# Aula bônus — Docker → Azure DevOps → AKS

Bundle completo para a aula bônus do canal **@DevOpsRaiz** sobre como
construir uma pipeline Azure DevOps que builda imagem Docker, faz push
pro Azure Container Registry (ACR) e faz deploy no AKS — Azure Kubernetes
Service — com rolling update e zero downtime.

Publicação: **apenas YouTube** (sem Instagram/Shorts dessa vez).

## Arquivos desse bundle

| Arquivo | Função |
|---------|--------|
| `aula-bonus-azuredevops-aks.md` | Roteiro completo (12 min) + metadados YouTube (título, descrição, tags, thumb, cards, end-screen) |
| `azure-pipelines.yml` | Pipeline Azure DevOps de 2 stages: Build (Docker + push ACR) + Deploy (KubernetesManifest@1 no AKS) |
| `Dockerfile` | Multi-stage Python 3.12, usuário não-root, healthcheck, otimizado pra ACR |
| `k8s/deployment.yaml` | Deployment com 2 réplicas, rolling update `maxUnavailable: 0`, readiness/liveness probes, resource requests/limits |
| `k8s/service.yaml` | Service ClusterIP que expõe a API na porta 80 → 8000 do container |
| `k8s/ingress.yaml` | Ingress AGIC (Application Gateway) com HTTPS automático via cert-manager + Let's Encrypt |

Todos os YAMLs estão testados em **AKS 1.30 região eastus2**, ACR Basic tier,
e Azure DevOps Services em maio/2026.

## Como produzir o vídeo

Esse vídeo **não** entra na pipeline diária HeyGen+Pixar (passo 5). Sugiro
gravação manual mais cuidadosa:

1. **Tela**: OBS ou Loom gravando 1080p
2. **Voz**: Mateo HeyGen ou Tiago direto no microfone (vídeo bônus pode ser pessoal)
3. **Diagramas Pixar**: gerar 5 PNGs específicas (ver markers `[PIXAR: ...]` no .md)
4. **B-roll**: screenshots do portal Azure DevOps + `kubectl get pods -w` rodando
5. **Edição**: cortes ágeis (cada bloco de 1-2 min com pause + cut)

### Para publicar via pipeline automatizado

Se preferir usar o pipeline HeyGen Mateo do passo 5, basta:

```bash
cd marketing/automacao
# Gera o MP4 (com cenas Pixar no estilo do canal)
python3 heygen_mateo_pipeline.py aula \
    --day 99 \
    --backend replicate  # ou stub pra testar sem custo

# Publica no YouTube como unlisted
python3 youtube_publisher.py --kind aula --day 99 --privacy unlisted
```

> O número `99` é convenção para marcar como bônus (fora dos 30 dias).

## Pré-requisitos do espectador (cita no início da aula)

- Conta Azure com permissão Contributor
- AKS provisionado (qualquer SKU, mesmo Free):
  ```bash
  az aks create -g rg-devopsraiz -n aks-devopsraiz --node-count 2 --node-vm-size Standard_B2s
  ```
- ACR provisionado e anexado ao AKS:
  ```bash
  az acr create -g rg-devopsraiz -n devopsraizacr --sku Basic
  az aks update -g rg-devopsraiz -n aks-devopsraiz --attach-acr devopsraizacr
  ```
- Aplicação FastAPI funcionando (criar via ebook gratuito do passo 1)
- Azure DevOps Organization (gratuito até 5 usuários)

## Customização rápida

Procure e substitua nesses valores nos YAMLs antes de usar:

| Placeholder | Substituir por |
|-------------|----------------|
| `devopsraizacr.azurecr.io` | nome do seu ACR |
| `devopsraiz/tarefas-api` | namespace/nome da sua imagem |
| `production` | namespace do AKS onde quer publicar |
| `api.devopsraiz.com.br` | seu domínio real (Ingress) |
| `tarefas-api-db` | nome do Secret do banco |
| `acr-pull-secret` | secret de pull do ACR (se não usar `--attach-acr`) |
| `devopsraiz-acr-connection` | nome do Service Connection ACR no Azure DevOps |
| `devopsraiz-aks-connection` | nome do Service Connection AKS no Azure DevOps |

## Custos esperados

| Recurso | Custo médio/mês |
|---------|------------------|
| AKS controlplane (Free tier) | US$ 0 |
| 2 nodes Standard_B2s | ~US$ 60 |
| ACR Basic | US$ 5 |
| Application Gateway WAF_v2 (pra Ingress) | ~US$ 30 |
| **Total estimado** | **~US$ 95** |

Pra hobby/dev/demo, dá pra cortar o Application Gateway e usar
NGINX Ingress (de graça) — só perde HTTPS-via-AGIC e WAF.

## Links amarrados

Toda a aula faz funil para:

- Ebook gratuito (passo 1) — capítulos de Docker, K8s e CI/CD entram natural na conversa
- Trilha DEVOPSRAIZ com cupom **SEGUIDOR80** → R$ 39,99
- WhatsApp **(11) 96482-3126** para tira-dúvidas
