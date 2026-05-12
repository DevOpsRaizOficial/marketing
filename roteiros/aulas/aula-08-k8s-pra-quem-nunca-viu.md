    # AULA 08 — Kubernetes em 7 min: orquestra dos containers

    > **Canal:** @DevOpsRaiz · **Apresentador:** Mateo (HeyGen Avatar IV Pixar)
    > **Duração-alvo:** 5-7 minutos · **Formato:** YouTube long-form 16:9
    > **CTAs no vídeo:** ebook gratuito + PDF apoio (R$ 9,90 com CUPOM50) + Trilha (R$ 39,99 com SEGUIDOR80)

    ---

    ## 0:00 — HOOK (15s)

    Docker é o instrumento. Kubernetes é a orquestra. Você não roda 1000 containers manualmente.

    ---

    ## 0:15 — APRESENTAÇÃO (10s)

    Eu sou o Mateo do canal DEVOPSRAIZ. Aqui a gente cai dentro de Cloud, DevOps e IA — em português, com código que roda. Bora.

    ---

    ## 0:25 — PONTO 1: Pod, Deployment, Service, ConfigMap (1 min)

    Quando você ouve falar em pod, deployment, service, configmap pela primeira vez, parece complicado, mas tem uma analogia simples. Pensa numa entrega de pacote: cliente é quem pede, servidor é quem entrega. É só isso. Resumindo: pod, deployment, service, configmap é a base de toda comunicação que vai aparecer nas próximas aulas.

    [COMANDO: kubectl get pods -A | rodando no terminal pra testar]

    ---

    ## 1:25 — PONTO 2: kubectl get/describe/logs/exec (1 min)

    Esse é o ponto que mais derruba dev júnior em entrevista. Anota: kubectl get/describe/logs/exec é o mecanismo por trás de tudo que funciona em rede. Sem isso, você não consegue chegar em nenhum site, app, ou API. Olha o comando que prova isso na sua máquina agora.

    ---

    ## 2:25 — PONTO 3: Self-healing e auto-scale (1m30s)

    Aqui é onde a maioria aprende fazendo. Vou te mostrar o exemplo prático. Esse comando você vai precisar saber de cor — aparece em entrevista, em troubleshooting de produção e em script de automação.

    [COMANDO: kubectl describe pod <nome> | exemplo prático do conceito 3]

    ---

    ## 3:55 — PONTO 4: minikube/kind/EKS/AKS/GKE (1m30s)

    Pra fechar, esse aqui é o ponto que separa quem só sabe a teoria de quem entende o porquê. Quando você juntar os 4 pontos, você consegue debugar 80% dos problemas reais que vai encontrar em produção.

    [COMANDO: kubectl logs -f <pod-name> | aprofundamento do conceito 4]

    ---

    ## 5:25 — RECAP (30s)

    Recapitulando em 6 minutos:

    1. Pod, Deployment, Service, ConfigMap
2. kubectl get/describe/logs/exec
3. Self-healing e auto-scale
4. minikube/kind/EKS/AKS/GKE

    ---

    ## 5:55 — CTAs (1 min)

    Se isso fez sentido, eu tenho 3 coisas pra te oferecer.

    Primeiro: um ebook **gratuito** que ensina do zero até publicar uma API Python na internet em 7 dias. Link na descrição.

    Segundo: o **PDF de apoio dessa aula** — com resumo, comandos, troubleshooting comum e exercícios pra você praticar. Custa R$ 9,90, mas como você tá assistindo aqui, usa o cupom **CUPOM50** e paga só R$ 4,95. Link na descrição.

    Terceiro: se você quer o caminho completo — multi-cloud, IA, segurança, observabilidade — é a Trilha DEVOPSRAIZ no Hotmart. Cupom **SEGUIDOR80** dá 80% off: de R$ 199,99 por R$ 39,99.

    Tira-dúvidas direto comigo no WhatsApp **(11) 96482-3126**. Te vejo na aula 09. Valeu raiz.

    ---

    ## METADADOS YOUTUBE

    - **Título:** Aula 08/30 · Kubernetes em 7 min: orquestra dos containers
    - **Descrição:**
        Aula 08 da série "Zero ao Deploy" do canal DEVOPSRAIZ.

        📌 RECURSOS DESSA AULA:

        🆓 Comandos e snippets (gratuito, GitHub público):
        → https://github.com/DevOpsRaizOficial/aulas-publicas/tree/main/aula-08-k8s-pra-quem-nunca-viu

        💎 PDF de Apoio Completo (R$ 9,90 → R$ 4,95 com CUPOM50):
        → Resumo + comandos + troubleshooting + exercícios + checklist
        → https://go.hotmart.com/PDF-AULA-08

        🚀 Trilha DEVOPSRAIZ Completa (R$ 199,99 → R$ 39,99 com SEGUIDOR80):
        → 6 ebooks + 30 dias guiados + tira-dúvidas WhatsApp
        → https://go.hotmart.com/S105313699A

        📱 WhatsApp tira-dúvidas: (11) 96482-3126
        📷 Instagram: https://instagram.com/devopsraiz_oficial

        --- TIMESTAMPS ---
        00:00 Hook
        00:15 Apresentação
        00:25 Pod, Deployment, Service, ConfigMap
        01:25 kubectl get/describe/logs/exec
        02:25 Self-healing e auto-scale
        03:55 minikube/kind/EKS/AKS/GKE
        05:25 Recap
        05:55 CTAs + cupons

        --- COMANDOS USADOS ---
        # Comando 1: kubectl get pods -A
# Comando 2: kubectl describe pod <nome>
# Comando 3: kubectl logs -f <pod-name>

        Veja na descrição os arquivos completos no GitHub público.

        #devops #python #cloud #aws #kubernetes #devopsraiz #azure

    - **Tags:** devops, python, cloud, aws, kubernetes, docker, terraform, fastapi, sre, devopsraiz
    - **Categoria YouTube:** 27 (Education)
    - **Thumb sugerida:** rosto Mateo close + título grande laranja sobre fundo dark #020617
    - **Cards:** aula anterior em 1:30, ebook gratuito em 5:55, PDF apoio em 6:30
    - **End screen:** próxima aula + inscrever-se
