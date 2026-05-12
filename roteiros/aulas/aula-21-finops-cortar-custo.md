    # AULA 21 — FinOps em 7 min: pare de queimar dinheiro

    > **Canal:** @DevOpsRaiz · **Apresentador:** Mateo (HeyGen Avatar IV Pixar)
    > **Duração-alvo:** 5-7 minutos · **Formato:** YouTube long-form 16:9
    > **CTAs no vídeo:** ebook gratuito + PDF apoio (R$ 9,90 com CUPOM50) + Trilha (R$ 39,99 com SEGUIDOR80)

    ---

    ## 0:00 — HOOK (15s)

    Conta AWS chegou em US$15k e ninguém sabe explicar? Acabou.

    ---

    ## 0:15 — APRESENTAÇÃO (10s)

    Eu sou o Mateo do canal DEVOPSRAIZ. Aqui a gente cai dentro de Cloud, DevOps e IA — em português, com código que roda. Bora.

    ---

    ## 0:25 — PONTO 1: Cost Explorer + Athena (1 min)

    Quando você ouve falar em cost explorer + athena pela primeira vez, parece complicado, mas tem uma analogia simples. Pensa numa entrega de pacote: cliente é quem pede, servidor é quem entrega. É só isso. Resumindo: cost explorer + athena é a base de toda comunicação que vai aparecer nas próximas aulas.

    [COMANDO: aws ce get-cost-and-usage --time-period Start=2026-04-01,End=2026-05-01 --granularity MONTHLY --metrics BlendedCost | rodando no terminal pra testar]

    ---

    ## 1:25 — PONTO 2: RI vs Savings Plans vs Spot (1 min)

    Esse é o ponto que mais derruba dev júnior em entrevista. Anota: ri vs savings plans vs spot é o mecanismo por trás de tudo que funciona em rede. Sem isso, você não consegue chegar em nenhum site, app, ou API. Olha o comando que prova isso na sua máquina agora.

    ---

    ## 2:25 — PONTO 3: Tagging strategy ROI (1m30s)

    Aqui é onde a maioria aprende fazendo. Vou te mostrar o exemplo prático. Esse comando você vai precisar saber de cor — aparece em entrevista, em troubleshooting de produção e em script de automação.

    [COMANDO: infracost breakdown --path . | exemplo prático do conceito 3]

    ---

    ## 3:55 — PONTO 4: Infracost/OpenCost/Vantage (1m30s)

    Pra fechar, esse aqui é o ponto que separa quem só sabe a teoria de quem entende o porquê. Quando você juntar os 4 pontos, você consegue debugar 80% dos problemas reais que vai encontrar em produção.

    [COMANDO: kubectl cost --window 7d | aprofundamento do conceito 4]

    ---

    ## 5:25 — RECAP (30s)

    Recapitulando em 6 minutos:

    1. Cost Explorer + Athena
2. RI vs Savings Plans vs Spot
3. Tagging strategy ROI
4. Infracost/OpenCost/Vantage

    ---

    ## 5:55 — CTAs (1 min)

    Se isso fez sentido, eu tenho 3 coisas pra te oferecer.

    Primeiro: um ebook **gratuito** que ensina do zero até publicar uma API Python na internet em 7 dias. Link na descrição.

    Segundo: o **PDF de apoio dessa aula** — com resumo, comandos, troubleshooting comum e exercícios pra você praticar. Custa R$ 9,90, mas como você tá assistindo aqui, usa o cupom **CUPOM50** e paga só R$ 4,95. Link na descrição.

    Terceiro: se você quer o caminho completo — multi-cloud, IA, segurança, observabilidade — é a Trilha DEVOPSRAIZ no Hotmart. Cupom **SEGUIDOR80** dá 80% off: de R$ 199,99 por R$ 39,99.

    Tira-dúvidas direto comigo no WhatsApp **(11) 96482-3126**. Te vejo na aula 22. Valeu raiz.

    ---

    ## METADADOS YOUTUBE

    - **Título:** Aula 21/30 · FinOps em 7 min: pare de queimar dinheiro
    - **Descrição:**
        Aula 21 da série "Zero ao Deploy" do canal DEVOPSRAIZ.

        📌 RECURSOS DESSA AULA:

        🆓 Comandos e snippets (gratuito, GitHub público):
        → https://github.com/DevOpsRaizOficial/aulas-publicas/tree/main/aula-21-finops-cortar-custo

        💎 PDF de Apoio Completo (R$ 9,90 → R$ 4,95 com CUPOM50):
        → Resumo + comandos + troubleshooting + exercícios + checklist
        → https://go.hotmart.com/PDF-AULA-21

        🚀 Trilha DEVOPSRAIZ Completa (R$ 199,99 → R$ 39,99 com SEGUIDOR80):
        → 6 ebooks + 30 dias guiados + tira-dúvidas WhatsApp
        → https://go.hotmart.com/S105313699A

        📱 WhatsApp tira-dúvidas: (11) 96482-3126
        📷 Instagram: https://instagram.com/devopsraiz_oficial

        --- TIMESTAMPS ---
        00:00 Hook
        00:15 Apresentação
        00:25 Cost Explorer + Athena
        01:25 RI vs Savings Plans vs Spot
        02:25 Tagging strategy ROI
        03:55 Infracost/OpenCost/Vantage
        05:25 Recap
        05:55 CTAs + cupons

        --- COMANDOS USADOS ---
        # Comando 1: aws ce get-cost-and-usage --time-period Start=2026-04-01,End=2026-05-01 --granul
# Comando 2: infracost breakdown --path .
# Comando 3: kubectl cost --window 7d

        Veja na descrição os arquivos completos no GitHub público.

        #devops #python #cloud #aws #kubernetes #devopsraiz #azure

    - **Tags:** devops, python, cloud, aws, kubernetes, docker, terraform, fastapi, sre, devopsraiz
    - **Categoria YouTube:** 27 (Education)
    - **Thumb sugerida:** rosto Mateo close + título grande laranja sobre fundo dark #020617
    - **Cards:** aula anterior em 1:30, ebook gratuito em 5:55, PDF apoio em 6:30
    - **End screen:** próxima aula + inscrever-se
