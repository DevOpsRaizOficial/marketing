"""
Generator de roteiros dos 30 dias DEVOPSRAIZ.

V3 (atual): foco em SHORTS de 10s com impacto alto pra dev iniciando.
            Sem video aulas long-form. PDF de Apoio entrega o conteudo
            que o short prometeu.

Funil:
  1. Short (gratuito, 10s) -> capta atencao
  2. PDF de Apoio (R$ 9,90, cupom CUPOM50 = R$ 4,95) -> entrega o conteudo
  3. Trilha completa (R$ 199,99, cupom SEGUIDOR80 = R$ 39,99) -> upsell

Saida:
  - ../roteiros/shorts/short-XX-slug.md (10s)
  - ../posts_prontos/v2_python_zero_deploy/ig-XX-slug.md

Uso:
    cd marketing/roteiros && python generate_30_aulas.py
"""

from pathlib import Path
from textwrap import dedent

OUT_DIR = Path(__file__).parent
SHORTS_DIR = OUT_DIR / "shorts"
IG_DIR = OUT_DIR.parent / "posts_prontos" / "v2_python_zero_deploy"
for d in (SHORTS_DIR, IG_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# Estrutura dos 30 dias
# Cada item: (dia, slug, titulo, hook_short, punchline_short, conceitos_pdf[4], comandos_pdf[3])
#   - hook_short:    pergunta/dor de 1 linha (max 80 chars), pra abrir o short
#   - punchline_short: insight de 1 frase resolvendo a dor (max 110 chars)
#   - conceitos_pdf: 4 topicos que o PDF cobre (entrega completa do tema)
#   - comandos_pdf:  3 comandos pratichos pro PDF (com explicacao)
#
# Total speech do short = hook (3s) + punchline (5s) + cta (2s) = ~150 chars.
# ==============================================================================
AULAS = [
    (1, "internet-cliente-servidor",
     "Internet em 10 segundos",
     "Você sabe o que acontece quando digita um site no celular?",
     "Cliente pede. DNS traduz. Servidor entrega. Em 0,2 segundos.",
     ["Cliente vs servidor", "DNS: domínio vira IP", "HTTP métodos GET/POST/PUT/DELETE", "Códigos 2xx/4xx/5xx"],
     ["nslookup instagram.com",
      "curl -I https://google.com",
      "ping 8.8.8.8"]),

    (2, "linux-essencial-git",
     "Linux + Git pra júnior",
     "Vaga de júnior pede Git e você nunca abriu o terminal?",
     "8 comandos resolvem 95% do dia. cd, ls, git add, git commit, git push.",
     ["Navegação: pwd, ls, cd", "Edição: cat, grep, nano", "Git: init, add, commit, push, pull", "SSH no GitHub"],
     ["ls -la ~/",
      "git init && git add . && git commit -m 'inicial'",
      "ssh-keygen -t ed25519 -C 'voce@email.com'"]),

    (3, "python-em-30-minutos",
     "Python em 10 segundos",
     "Python é a linguagem #1 do mercado. E você ainda não sabe?",
     "Variável, função, lista. Em 30 minutos você lê código real de empresa.",
     ["Variáveis e tipos", "Listas e dicionários", "If/for/funções", "venv + pip install"],
     ["python3 --version",
      "python3 -m venv .venv && source .venv/bin/activate",
      "pip install fastapi"]),

    (4, "primeira-api-fastapi",
     "API REST em 15 linhas",
     "Acha que API REST precisa de framework gigante e meses de estudo?",
     "FastAPI faz com 15 linhas. E gera documentação automática.",
     ["pip install fastapi", "Endpoints GET e POST", "Pydantic + validação automática", "Swagger UI em /docs"],
     ["pip install 'fastapi[standard]'",
      "fastapi dev main.py",
      "curl -X POST http://localhost:8000/tarefas -H 'Content-Type: application/json' -d '{\"titulo\":\"deploy\"}'"]),

    (5, "postgresql-async",
     "Banco que não perde dados",
     "Sua API perde tudo quando reinicia? Bem-vindo ao mundo real.",
     "Postgres + SQLAlchemy async. Dados salvos pra sempre, query rápida.",
     ["SQLAlchemy async + asyncpg", "DeclarativeBase e mapped_column", "AsyncSession e select()", "Migration vs create_all"],
     ["pip install 'sqlalchemy[asyncio]' asyncpg",
      "docker run -d -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16",
      "psql -h localhost -U postgres -c '\\dt'"]),

    (6, "docker-do-zero",
     "Docker em 10 segundos",
     "Funciona na sua máquina mas quebra na do colega?",
     "Container = pacote zip da sua app. Roda igual em qualquer máquina.",
     ["Container vs VM", "Dockerfile linha por linha", "docker-compose com Postgres", "Cache de layers"],
     ["docker --version",
      "docker build -t tarefas-api .",
      "docker compose up --build"]),

    (7, "deploy-render-https",
     "Sai do localhost",
     "Sua API roda só no localhost? Tá invisível pro mundo.",
     "Render publica de graça com HTTPS. git push e tá no ar.",
     ["GitHub Actions CI", "Web Service no Render", "Custom domain + Let's Encrypt", "UptimeRobot health"],
     ["git push origin main",
      "curl https://tarefas-api.onrender.com/health",
      "dig api.devopsraiz.com.br"]),

    (8, "k8s-pra-quem-nunca-viu",
     "Kubernetes sem dor",
     "Kubernetes assusta? Pensa numa orquestra de músicos.",
     "Pod = músico. Deployment = partitura. Kubectl = maestro.",
     ["Pod, Deployment, Service, ConfigMap", "kubectl get/describe/logs/exec", "Self-healing e auto-scale", "minikube/kind/EKS/AKS/GKE"],
     ["kubectl get pods -A",
      "kubectl describe pod <nome>",
      "kubectl logs -f <pod-name>"]),

    (9, "terraform-iac",
     "Infra que vive pra sempre",
     "Você cria servidor clicando? Vai perder o histórico.",
     "Terraform é infra em código. Versionada, reproduzível, eterna.",
     ["Resource, provider, variable", "terraform init/plan/apply", "State file: onde guardar", "Workspaces e módulos"],
     ["terraform init",
      "terraform plan -out=tfplan",
      "terraform apply tfplan"]),

    (10, "aws-conta-zero",
     "AWS em 10 segundos",
     "AWS tem 200 serviços. Você precisa de 4 pra começar.",
     "EC2 servidor. S3 arquivo. RDS banco. IAM permissão. Resto vem depois.",
     ["EC2: VMs com cost-per-hour", "S3: storage infinito", "RDS: banco gerenciado", "IAM: o que derruba junior"],
     ["aws s3 ls",
      "aws ec2 describe-instances --output table",
      "aws iam list-users"]),

    (11, "ci-cd-github-actions",
     "Adeus 'funciona aqui'",
     "Funciona na minha máquina é piada. CI/CD é a prova real.",
     "git push roda testes e faz deploy automático. Zero clique humano.",
     ["Jobs, steps, runners", "pytest no pipeline", "docker build + push GHCR", "Deploy automático no merge"],
     ["cat .github/workflows/ci.yml",
      "gh workflow run ci.yml",
      "gh run watch"]),

    (12, "logs-e-monitoramento",
     "Veja o bug antes do cliente",
     "Cliente reclama do bug e você descobre depois?",
     "Logs estruturados + Grafana. Você vê o problema antes dele aparecer.",
     ["3 pilares: logs/métricas/traces", "Logs estruturados JSON", "Prometheus + Grafana", "OpenTelemetry"],
     ["docker run -p 9090:9090 prom/prometheus",
      "curl http://localhost:9090/metrics",
      "kubectl logs -l app=api --tail=50 -f"]),

    (13, "seguranca-owasp-top-10",
     "Seu código tem buraco",
     "Seu código tem SQL injection e XSS? Você não faz ideia.",
     "OWASP Top 10. A checklist que separa júnior de pleno.",
     ["Injection, Broken Auth, XSS", "SSRF e Insecure Design", "Mitigações práticas", "Tools: ZAP, Trivy, Snyk"],
     ["trivy image python:3.12-slim",
      "docker run -t owasp/zap2docker-stable zap-baseline.py -t https://exemplo.com",
      "snyk test"]),

    (14, "ia-rag-em-producao",
     "ChatGPT nos SEUS docs",
     "Queria ChatGPT que lê só os SEUS documentos?",
     "RAG. Busca semântica + IA. Custa centavos por consulta.",
     ["O que é RAG (retrieval + generation)", "Vector DB: Pinecone/pgvector", "Embeddings + similarity search", "Custo por 1k consultas"],
     ["pip install langchain openai pgvector",
      "python ingest_docs.py --dir ./docs/",
      "curl -X POST localhost:8000/chat -d '{\"q\":\"como deploy?\"}'"]),

    (15, "saas-multi-tenant",
     "1 código pra 1000 clientes",
     "Como Salesforce isola 1000 clientes no mesmo software?",
     "Row-Level Security no Postgres + JWT com tenant_id. Simples assim.",
     ["Schema-per-tenant vs row-level", "Row-level security PostgreSQL", "JWT com tenant_id", "Billing com Stripe"],
     ["CREATE POLICY tenant_isolation ON tasks USING (tenant_id = current_setting('app.tenant')::uuid);",
      "SET LOCAL app.tenant = 'uuid-do-cliente';",
      "stripe customers create --email cliente@x.com"]),

    (16, "docker-otimizacao",
     "Docker 10x mais leve",
     "Imagem Docker de 2GB demora 5 min pra subir?",
     "Multi-stage build derruba pra 80MB. 10x mais rápido em produção.",
     ["Multi-stage build", "Alpine vs Slim vs Distroless", "Cache de layers (ordem importa)", "Scan com Trivy"],
     ["docker build -t app:slim .",
      "docker images app",
      "trivy image app:slim"]),

    (17, "k8s-helm-kustomize",
     "YAML não escala manual",
     "100 microsserviços em YAML manual? Você desiste no terceiro.",
     "Helm Chart é template. Argo CD é GitOps. Vida saudável.",
     ["Helm Chart: values, templates", "Kustomize: bases + overlays", "Quando usar cada um", "Argo CD GitOps"],
     ["helm install api ./chart --values prod.yaml",
      "kustomize build overlays/prod | kubectl apply -f -",
      "argocd app sync devopsraiz"]),

    (18, "aws-eks-na-pratica",
     "EKS vale pra você?",
     "AWS EKS custa US$72/mês só de controlplane.",
     "Vale se já paga vaga sênior. Pra hobby, usa kind ou Cloud Run.",
     ["Provisionar EKS com Terraform", "Node groups managed/Fargate", "IRSA: IAM pra pods sem secrets", "Add-ons essenciais"],
     ["eksctl create cluster --name devopsraiz --region us-east-1",
      "aws eks update-kubeconfig --name devopsraiz",
      "kubectl get nodes -o wide"]),

    (19, "azure-aks",
     "AKS grátis pra startup",
     "Quer K8s gerenciado sem pagar controlplane?",
     "AKS da Azure é grátis o controlplane. Você paga só os nodes.",
     ["AKS vs EKS vs GKE", "Azure AD integration", "App Gateway Ingress Controller", "Spot nodes (-70% custo)"],
     ["az aks create -g rg-devopsraiz -n aks-devopsraiz --node-count 2",
      "az aks get-credentials -g rg-devopsraiz -n aks-devopsraiz",
      "kubectl get nodes"]),

    (20, "gcp-cloud-run",
     "Serverless de container",
     "Sem servidor pra gerenciar, paga só por requisição.",
     "Cloud Run sobe seu Docker e escala de 0 a milhares. 2 cliques.",
     ["O que é serverless de container", "gcloud run deploy", "Custom domain + IAM segundos", "Cloud Run Jobs batch"],
     ["gcloud run deploy api --source . --region us-central1",
      "gcloud run services list",
      "gcloud run jobs execute migracao-db --wait"]),

    (21, "finops-cortar-custo",
     "Pare de queimar dinheiro",
     "Conta AWS chegou em US$15k e ninguém sabe explicar?",
     "Tags + Cost Explorer + Spot. Corta 50% sem perder nada.",
     ["Cost Explorer + Athena", "RI vs Savings Plans vs Spot", "Tagging strategy ROI", "Infracost/OpenCost/Vantage"],
     ["aws ce get-cost-and-usage --time-period Start=2026-04-01,End=2026-05-01 --granularity MONTHLY --metrics BlendedCost",
      "infracost breakdown --path .",
      "kubectl cost --window 7d"]),

    (22, "observabilidade-prometheus",
     "3 métricas. Só isso.",
     "Você tem 200 métricas e não sabe qual olhar?",
     "Rate. Errors. Duration. RED method. Resto é ruído.",
     ["Métricas RED: Rate/Errors/Duration", "PromQL básico", "Alertmanager", "Grafana dashboard inicial"],
     ["promtool query instant http://localhost:9090 'rate(http_requests_total[5m])'",
      "promtool check rules alerts.yml",
      "curl -s localhost:9090/api/v1/query?query=up"]),

    (23, "sre-slo-slis",
     "O jogo dos 9s",
     "99,9% é 8h46min de downtime por ano. Você sabia?",
     "SLO é matemática. Error budget é a sua moeda como SRE.",
     ["SLI, SLO, SLA na prática", "Error budget: moeda do SRE", "Burn rate alerts", "Postmortem culpa-zero"],
     ["echo 'SLO 99.9% = 43min downtime/mes'",
      "curl -s api/health | jq .uptime",
      "kubectl get pdb -A"]),

    (24, "zero-trust-network",
     "Castelo morreu em 2010",
     "Firewall e VPN te dão segurança? Não dão mais.",
     "Zero Trust: nunca confie, sempre verifique. mTLS + SPIFFE.",
     ["Modelo Zero Trust", "BeyondCorp, mTLS, SPIFFE", "Service Mesh: Istio/Linkerd", "Implementação time pequeno"],
     ["istioctl install --set profile=demo -y",
      "kubectl label namespace prod istio-injection=enabled",
      "openssl x509 -in cert.pem -noout -subject"]),

    (25, "lgpd-dev",
     "LGPD pra dev",
     "Empresa pode tomar multa de 50 milhões. Por causa do seu DELETE.",
     "DELETE de verdade. Anonymization. ROPA. Você precisa entender.",
     ["Princípios que afetam código", "Direito ao esquecimento (DELETE)", "Anonymization vs pseudonymization", "DPO, ROPA, relatório impacto"],
     ["UPDATE users SET email = MD5(email), nome = '***' WHERE id = $1;",
      "psql -c 'DELETE FROM logs WHERE created_at < NOW() - INTERVAL 90 DAY'",
      "grep -r 'cpf\\|rg\\|cartao' src/ | wc -l"]),

    (26, "agents-llm-em-producao",
     "ChatGPT que AGE",
     "Hoje ChatGPT só responde. Em breve, ele AGE.",
     "Agents LLM compram, agendam, decidem. Function calling + ReAct.",
     ["Chat vs RAG vs Tools vs Agents", "ReAct e Plan-and-Execute", "Function calling FastAPI", "Guardrails (NÃO deixar doido)"],
     ["pip install langchain-openai langgraph",
      "python agent.py --task 'comprar passagem mais barata'",
      "curl localhost:8000/agent -d '{\"goal\":\"agendar reuniao terca\"}'"]),

    (27, "kafka-event-driven",
     "Quando REST não escala",
     "Sua API REST trava com 10 mil reqs/s. Próximo passo?",
     "Kafka. Producer publica, consumer escuta. Rio de mensagens.",
     ["Topic, partition, consumer group", "Producer + consumer aiokafka", "Schema registry compatibility", "Quando NÃO usar Kafka"],
     ["kafka-topics --bootstrap-server localhost:9092 --create --topic eventos --partitions 3",
      "kafka-console-producer --topic eventos --bootstrap-server localhost:9092",
      "kafka-consumer-groups --bootstrap-server localhost:9092 --list"]),

    (28, "secrets-vault",
     "Senha no .env já era",
     "Você guarda senha de produção em variável de ambiente?",
     "Vault gera, roda, audita. Secret Manager pra cloud-native.",
     ["Por que .env é só o primeiro passo", "Vault vs Secrets Manager vs Sealed Secrets", "External Secrets Operator K8s", "Rotation automática"],
     ["vault kv put secret/api db_pass=$(openssl rand -hex 16)",
      "kubectl create secret generic api-db --from-literal=pass=$VAULT_PASS",
      "aws secretsmanager rotate-secret --secret-id prod/api/db"]),

    (29, "carreira-junior-senior",
     "O salário em DevOps",
     "Júnior R$5k. Pleno R$12k. Sênior R$22k. Staff R$35k.",
     "A diferença não é tempo de casa. É autonomia técnica e impacto.",
     ["O que diferencia JR/PL/SR", "Salário médio 2026 (BRL e USD)", "Como negociar com RH", "Mentoria > 2 anos perdidos"],
     ["# JR R$5-9k | PL R$10-18k | SR R$18-35k | Staff R$30-50k",
      "linkedin learning paths",
      "git log --since='1 year' --author='me' | wc -l"]),

    (30, "trilha-completa-fechamento",
     "30 dias. Tá pronto?",
     "30 dias. 30 conceitos. Você acompanhou ou só consumiu?",
     "Trilha DEVOPSRAIZ completa: cupom SEGUIDOR80 = R$ 39,99. Bora.",
     ["Recap dos 29 dias anteriores", "Stack final: AWS+Azure+GCP+IA", "O que está na Trilha completa", "Cupom SEGUIDOR80: como pegar"],
     ["echo 'Trilha completa: 30 dias guiado'",
      "echo 'Cupom SEGUIDOR80 = 80% off'",
      "echo 'WhatsApp tira-duvidas: (11) 96482-3126'"]),
]


# ==============================================================================
# Templates
# ==============================================================================
def template_short(dia, slug, titulo, hook_short, punchline_short,
                    conceitos_pdf, comandos_pdf):
    """Roteiro Short de no max 10s, impacto alto, comunicacao direta."""
    return dedent(f"""\
    # SHORT {dia:02d} — {titulo}

    > **Duracao MAX:** 10 segundos  ·  **Formato:** 9:16 vertical 1080x1920
    > **Avatar:** Mateo HeyGen (Pixar 3D, talking_style expressive)
    > **Publico-alvo:** dev iniciando carreira em Cloud/DevOps
    > **Estilo:** direto, sem jargao, sem rodeios

    ---

    ## 0:00–0:03 — HOOK (~3s)

    {hook_short}

    ## 0:03–0:08 — PUNCHLINE (~5s)

    {punchline_short}

    ## 0:08–0:10 — CTA (~2s)

    PDF de apoio R$ 4,95 com cupom CUPOM50. Link na bio.

    ---

    ## METADADOS

    - **Titulo Short:** {titulo}
    - **Caption:** {hook_short} | {punchline_short} | PDF de apoio R$ 4,95 cupom **CUPOM50** | Trilha completa R$ 39,99 cupom **SEGUIDOR80** | @devopsraiz | #devopsraiz #devops #cloud #devjr #carreiratech
    - **Trilha sonora:** lo-fi tech trending 60-90 BPM
    - **Texto na tela (overlay):**
        - 0:00-0:03 — "{hook_short}" (white sobre dark, font bold)
        - 0:03-0:08 — emoji + insight curto destacando palavra-chave
        - 0:08-0:10 — "PDF apoio R$ 4,95 - CUPOM50" (laranja sobre dark)
    """)


def template_ig(dia, slug, titulo, hook_short, punchline_short,
                 conceitos_pdf, comandos_pdf):
    """Legenda IG diaria amarrando ao short + PDF + Trilha."""
    return dedent(f"""\
    # POST INSTAGRAM DIA {dia:02d}

    > **Formato:** Reel 9:16 (mesmo MP4 do Short YouTube) OU carrossel 5 slides
    > **Horarios:** 12:00 (almoco) e 19:30 BRT (volta pra casa)
    > **Tema:** {titulo}

    ---

    ## LEGENDA COMPLETA

    {hook_short}

    {punchline_short}

    💡 Hoje no canal @devopsraiz o short do dia ja saiu - link na bio.

    Quer o conteudo COMPLETO sobre {titulo.lower()}?

    📘 **PDF de Apoio: R$ 9,90 → R$ 4,95 com cupom CUPOM50**
    Inclui:
    ▸ {conceitos_pdf[0]}
    ▸ {conceitos_pdf[1]}
    ▸ {conceitos_pdf[2]}
    ▸ {conceitos_pdf[3]}
    + 3 comandos copy-paste prontos + troubleshooting + exercicio.

    🚀 **Trilha completa DEVOPSRAIZ: R$ 199,99 → R$ 39,99 com cupom SEGUIDOR80**
    6 ebooks + 30 dias guiado + tira-duvidas WhatsApp.

    📱 Tira-duvidas direto comigo: **(11) 96482-3126**

    Comenta aí: você ja tinha pensado nisso?

    ---

    ## HASHTAGS

    #devopsraiz #devops #python #fastapi #docker #kubernetes #aws #cloud
    #devjr #carreiratech #devbr #devopsbr #pythonbrasil #programacao #tecnologia

    ---

    ## CTA STORIES (24h)

    1. Story 1: print do thumb do short + seta "TÁ NO AR ↑"
    2. Story 2: enquete "voce ja sabia disso?" sim/nao
    3. Story 3: print do PDF + "CUPOM50 = 50% off" com sticker link na bio
    4. Story 4: depoimento de aluno (rotaciona conforme estoque)
    """)


# ==============================================================================
# Geracao
# ==============================================================================
def main():
    total = 0
    for dia, slug, titulo, hook, punch, conceitos, comandos in AULAS:
        short_path = SHORTS_DIR / f"short-{dia:02d}-{slug}.md"
        short_path.write_text(
            template_short(dia, slug, titulo, hook, punch, conceitos, comandos),
            encoding="utf-8")
        total += 1

        ig_path = IG_DIR / f"ig-{dia:02d}-{slug}.md"
        ig_path.write_text(
            template_ig(dia, slug, titulo, hook, punch, conceitos, comandos),
            encoding="utf-8")
        total += 1

        print(f"  OK Dia {dia:02d}: {slug}")

    print(f"\n{total} arquivos gerados ({len(AULAS)} shorts + {len(AULAS)} IGs).")
    print("Aulas long-form foram removidas do funil — agora so shorts + PDF + Trilha.")


if __name__ == "__main__":
    main()
