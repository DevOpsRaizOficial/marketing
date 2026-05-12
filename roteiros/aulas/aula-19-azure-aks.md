    # AULA 19 — Azure AKS em 7 min: K8s grátis (controlplane)

    > **Canal:** @DevOpsRaiz · **Apresentador:** Mateo (HeyGen Avatar IV Pixar)
    > **Duração-alvo:** 5-7 minutos · **Formato:** YouTube long-form 16:9
    > **CTAs no vídeo:** ebook gratuito + PDF apoio (R$ 9,90 com CUPOM50) + Trilha (R$ 39,99 com SEGUIDOR80)

    ---

    ## 0:00 — HOOK (15s)

    AKS controlplane é grátis. Por que isso muda o jogo pra startup.

    ---

    ## 0:15 — APRESENTAÇÃO (10s)

    Eu sou o Mateo do canal DEVOPSRAIZ. Aqui a gente cai dentro de Cloud, DevOps e IA — em português, com código que roda. Bora.

    ---

    ## 0:25 — PONTO 1: AKS vs EKS vs GKE (1 min)

    Quando você ouve falar em aks vs eks vs gke pela primeira vez, parece complicado, mas tem uma analogia simples. Pensa numa entrega de pacote: cliente é quem pede, servidor é quem entrega. É só isso. Resumindo: aks vs eks vs gke é a base de toda comunicação que vai aparecer nas próximas aulas.

    [COMANDO: az aks create -g rg-devopsraiz -n aks-devopsraiz --node-count 2 | rodando no terminal pra testar]

    ---

    ## 1:25 — PONTO 2: Azure AD integration (1 min)

    Esse é o ponto que mais derruba dev júnior em entrevista. Anota: azure ad integration é o mecanismo por trás de tudo que funciona em rede. Sem isso, você não consegue chegar em nenhum site, app, ou API. Olha o comando que prova isso na sua máquina agora.

    ---

    ## 2:25 — PONTO 3: App Gateway Ingress Controller (1m30s)

    Aqui é onde a maioria aprende fazendo. Vou te mostrar o exemplo prático. Esse comando você vai precisar saber de cor — aparece em entrevista, em troubleshooting de produção e em script de automação.

    [COMANDO: az aks get-credentials -g rg-devopsraiz -n aks-devopsraiz | exemplo prático do conceito 3]

    ---

    ## 3:55 — PONTO 4: Spot nodes (-70% custo) (1m30s)

    Pra fechar, esse aqui é o ponto que separa quem só sabe a teoria de quem entende o porquê. Quando você juntar os 4 pontos, você consegue debugar 80% dos problemas reais que vai encontrar em produção.

    [COMANDO: kubectl get nodes | aprofundamento do conceito 4]

    ---

    ## 5:25 — RECAP (30s)

    Recapitulando em 6 minutos:

    1. AKS vs EKS vs GKE
2. Azure AD integration
3. App Gateway Ingress Controller
4. Spot nodes (-70% custo)

    ---

    ## 5:55 — CTAs (1 min)

    Se isso fez sentido, eu tenho 3 coisas pra te oferecer.

    Primeiro: um ebook **gratuito** que ensina do zero até publicar uma API Python na internet em 7 dias. Link na descrição.

    Segundo: o **PDF de apoio dessa aula** — com resumo, comandos, troubleshooting comum e exercícios pra você praticar. Custa R$ 9,90, mas como você tá assistindo aqui, usa o cupom **CUPOM50** e paga só R$ 4,95. Link na descrição.

    Terceiro: se você quer o caminho completo — multi-cloud, IA, segurança, observabilidade — é a Trilha DEVOPSRAIZ no Hotmart. Cupom **SEGUIDOR80** dá 80% off: de R$ 199,99 por R$ 39,99.

    Tira-dúvidas direto comigo no WhatsApp **(11) 96482-3126**. Te vejo na aula 20. Valeu raiz.

    ---

    ## METADADOS YOUTUBE

    - **Título:** Aula 19/30 · Azure AKS em 7 min: K8s grátis (controlplane)
    - **Descrição:**
        Aula 19 da série "Zero ao Deploy" do canal DEVOPSRAIZ.

        📌 RECURSOS DESSA AULA:

        🆓 Comandos e snippets (gratuito, GitHub público):
        → https://github.com/DevOpsRaizOficial/aulas-publicas/tree/main/aula-19-azure-aks

        💎 PDF de Apoio Completo (R$ 9,90 → R$ 4,95 com CUPOM50):
        → Resumo + comandos + troubleshooting + exercícios + checklist
        → https://go.hotmart.com/PDF-AULA-19

        🚀 Trilha DEVOPSRAIZ Completa (R$ 199,99 → R$ 39,99 com SEGUIDOR80):
        → 6 ebooks + 30 dias guiados + tira-dúvidas WhatsApp
        → https://go.hotmart.com/S105313699A

        📱 WhatsApp tira-dúvidas: (11) 96482-3126
        📷 Instagram: https://instagram.com/devopsraiz_oficial

        --- TIMESTAMPS ---
        00:00 Hook
        00:15 Apresentação
        00:25 AKS vs EKS vs GKE
        01:25 Azure AD integration
        02:25 App Gateway Ingress Controller
        03:55 Spot nodes (-70% custo)
        05:25 Recap
        05:55 CTAs + cupons

        --- COMANDOS USADOS ---
        # Comando 1: az aks create -g rg-devopsraiz -n aks-devopsraiz --node-count 2
# Comando 2: az aks get-credentials -g rg-devopsraiz -n aks-devopsraiz
# Comando 3: kubectl get nodes

        Veja na descrição os arquivos completos no GitHub público.

        #devops #python #cloud #aws #kubernetes #devopsraiz #azure

    - **Tags:** devops, python, cloud, aws, kubernetes, docker, terraform, fastapi, sre, devopsraiz
    - **Categoria YouTube:** 27 (Education)
    - **Thumb sugerida:** rosto Mateo close + título grande laranja sobre fundo dark #020617
    - **Cards:** aula anterior em 1:30, ebook gratuito em 5:55, PDF apoio em 6:30
    - **End screen:** próxima aula + inscrever-se
