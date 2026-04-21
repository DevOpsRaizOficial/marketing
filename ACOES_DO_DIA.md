# Ações do dia — 21/04 (Dia 1 do lançamento)

> Roteiro prático de 45 minutos pra executar HOJE. Faz nesta ordem.

---

## ✅ Já executado pelo robô

- Dia 1 (carrossel "Quem sou eu") publicado às ~11h30 BRT no @devopsraiz_oficial
- Seguindo @lucasmontano (criador-alvo 1/12)

---

## ⏳ Pendente executar pelo robô (19:00 BRT hoje)

- Reel Dia 1 (apresentação em vídeo com seu avatar HeyGen) — **publicado automaticamente** às 19:00 BRT via workflow `publish-reel-oneshot.yml` com cron único
- Dependências: (1) o `build-videos` precisa ter terminado; (2) commit do workflow no repo

---

## 🔥 O que VOCÊ faz agora (30 min)

### 1. Commit do workflow do Reel 1 (2 min)

```powershell
cd "C:\Users\TiagoAlvesdaRocha\OneDrive - TR99\Documentos\Claude\Projects\Ebooks-DevopsRaiz\marketing"
git add .github/workflows/publish-reel-oneshot.yml ENGAJAMENTO.md ACOES_DO_DIA.md
git commit -m "feat: reel oneshot + guia engajamento"
git push
```

Sem isso, o cron de 19:00 não dispara hoje.

### 2. Seguir os 11 criadores-alvo restantes (10 min)

**Regra importante:** **NÃO** segue todos de uma vez. Intervalo de 1-3 minutos
entre cada. Olha 1-2 posts do criador antes de seguir (comportamento humano).

Lista (eu já segui o lucasmontano):

- [ ] @codigofontetv
- [ ] @rocketseat
- [ ] @devsoutinho
- [ ] @gustavoguanabara
- [ ] @pachicodes
- [ ] @awsbrasil
- [ ] @microsoftbr
- [ ] @googlecloudbrasil
- [ ] @cncfofficial
- [ ] @linuxfoundation
- [ ] @techwithnana

Bonus (se tiver tempo):
- [ ] @devquestoes
- [ ] @hashtagtreinamentos

### 3. Deixar 10 comentários úteis em posts recentes (15 min)

Esta é a atividade mais importante. O algoritmo vê seus comentários em
posts de criadores grandes e **recomenda seu perfil pra gente que interage
com aqueles posts**.

**Como fazer direito:**

1. Abre o feed de cada criador que você acabou de seguir
2. Acha o post **mais recente** (< 24h ideal)
3. Evita posts com > 500 comentários (o seu some)
4. Escreve comentário técnico útil **de 15+ palavras**

**Exemplos de comentários que funcionam** (adapte ao contexto de cada post):

> Bom ponto sobre [X]. No nosso setup aqui, a gente usa [tecnologia] e
> a maior dor é [problema X]. Faz sentido o que você disse sobre [ponto].

> Ótimo conteúdo. Só complementando: quem está começando, a maior pegadinha
> pra mim foi [detalhe técnico]. Salvei pra revisitar.

> Valeu pelo conteúdo. Pergunta: em [cenário X], ainda faz sentido usar
> [Y] ou já passou da hora de migrar pra [Z]?

**Comentários ruins (que não geram reach):**

- ❌ "top! 🔥"
- ❌ "salvo"
- ❌ "⭐⭐⭐⭐⭐"
- ❌ "vou testar"

### 4. Responder TODOS os comentários do SEU post do Dia 1 (5 min)

1. Abre seu post (carrossel apresentação)
2. Responde cada comentário com 10+ palavras
3. Faz pergunta pro autor do comentário (mantém a conversa)

Exemplo de resposta:

> Comentário: "Massa, comprei a trilha!"
> Sua resposta: "Valeu demais! Me conta quando terminar o Ebook 1 qual parte foi mais útil pra você. Abri o DM pra qualquer dúvida técnica também 🙏"

---

## 🤖 Setup ManyChat (uma vez, 15 min — faz amanhã se não der hoje)

ManyChat é o único "robô" legítimo permitido pelo Instagram — transforma
comentários em DMs automáticos. Quando alguém comentar uma palavra-chave
(ex: "DOCKER"), ele manda o capítulo grátis automaticamente.

### Setup passo-a-passo

1. Acessa https://manychat.com → **Sign up free**
2. Conecta com seu Instagram `@devopsraiz_oficial`
3. Vai em **Automation → New Automation → Instagram Comment**
4. Configura:
   - **Trigger**: "Specific keyword(s)" → `DOCKER,docker`
   - **Action**:
     - Comment reply (público): "Te mandei no DM 👋"
     - DM message (privado):
       ```
       Oi! Obrigado por comentar.

       Aqui está o capítulo 1 do Ebook 2 (Docker) grátis pra você:
       https://go.hotmart.com/S105313699A?dp=1

       Se quiser os 6 ebooks completos, acima tá o link da trilha.

       Qualquer dúvida técnica é só me chamar aqui no direct!
       Tiago
       ```
5. Ativa e testa comentando a palavra DOCKER no seu último post (use outra conta)

**Por que isso multiplica engajamento por 10x:**
- Gera comentários (o que boost o alcance)
- Conversão pra DM é muito maior que pra link
- No DM você tem rapport 1-a-1

### Palavras-chave sugeridas (crie uma por ebook)

| Comentário | Resposta automática |
|---|---|
| `DOCKER` ou `docker` | Cap 1 do Ebook 2 grátis |
| `IA` ou `RAG` | Cap 1 do Ebook 4 grátis |
| `SRE` ou `SLO` | Cap 1 do Ebook 5 grátis |
| `FINOPS` ou `AWS` | Cap 1 do Ebook 1 grátis |
| `TRILHA` | Link direto pro checkout |

---

## 📊 Métricas pra acompanhar (anota no fim do dia)

- [ ] Quantos novos seguidores ganhou: ___
- [ ] Quantos comentários recebeu no carrossel Dia 1: ___
- [ ] Quantos saves no carrossel: ___
- [ ] Quantos DMs recebidos: ___
- [ ] Quantos comentários você deixou em outros perfis: ___

Se bateu:
- 5+ novos seguidores ✓
- 3+ saves ✓
- 1+ DMs ✓

Primeiro dia está saudável. Se bateu metade disso, aumenta comentários em
perfis externos amanhã.

---

## 📅 Rotina diária dos próximos 6 dias

| Horário | Ação |
|---|---|
| 08:00-08:15 | Story com foto do setup ou dica rápida |
| 08:15-08:30 | Comenta em 5 posts de criadores grandes |
| 12:00-12:15 | Publica post do dia (se for horário) OU enquete no story |
| 12:15-12:30 | Responde comentários recentes |
| 19:00-19:15 | Publica post da noite (19h é pico de engajamento) |
| 19:15-20:30 | **Responde TODOS os comentários do post** |
| 20:30-21:00 | Última leva de comentários em outros perfis |

---

## 🎯 Meta da semana

**21/04 → 28/04:**
- De 17 pra **80+ seguidores**
- 5 novos saves por dia em média
- 3 DMs por dia
- 1-2 vendas atribuídas via Hotmart (ok se for zero, semana 1 é aprendizado)

Se bateu meta: excelente, replica o ritmo.
Se não bateu: aumenta comentários externos pra 20 por dia semana 2.
