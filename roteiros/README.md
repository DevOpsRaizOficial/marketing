# Roteiros para HeyGen

Cada arquivo `.txt` nessa pasta é um roteiro de vídeo pronto para colar no
HeyGen. Use seu avatar "Teste1" com a Voice Clone que você já treinou.

## Como gerar os vídeos (1 tarde de trabalho)

1. Abra [app.heygen.com](https://app.heygen.com) e crie um novo projeto.
2. Selecione o avatar (a sua foto atual).
3. Selecione a Voice Clone "Teste1".
4. Cole o texto do roteiro `.txt` no campo Script.
5. Ajuste velocidade para **100%** (ou 105% se quiser ritmo mais dinâmico).
6. Gere o vídeo, aguarde renderização (2-5 min cada).
7. Baixe o MP4.
8. **Renomeie o arquivo** seguindo exatamente o padrão:
   - `reel-dia-01.mp4` → vídeo de apresentação
   - `reel-dia-03.mp4` → Reel salários DevOps
   - `reel-dia-09.mp4` → Terraform em 30s
   - `reel-dia-16.mp4` → Docker 1.2GB → 150MB
   - `reel-dia-21.mp4` → time-lapse
   - `reel-dia-26.mp4` → De projeto pessoal a SaaS
   - `story-dia-NN.mp4` → stories curtos (se produzir)
9. Jogue os MP4s na pasta `marketing/videos_mp4/` (ou no repositório Git, ou
   numa pasta cloud — ver SETUP.md).

## Formato recomendado no HeyGen

- **Aspect ratio:** 9:16 (vertical, formato Reel/Story)
- **Fundo:** use um dos cenários office/tech do HeyGen, OU
  deixe transparente e sobreponha um gradiente escuro no DaVinci/CapCut
  com os PNGs de `/criativos` como background.
- **Legendas:** gere legendas automáticas (Auto Captions) e estilize
  com fonte Bold, tamanho grande, cor amarela/branca (padrão TikTok).
- **Música:** música royalty-free de fundo em -18dB (baixa). Use a
  biblioteca do próprio HeyGen ou Uppbeat.io.

## Dica de qualidade

O maior erro de avatar IA é falar monótono. Para soar humano:

- Use **pontuação dramática**: vírgulas, reticências e ponto final fortes.
- Quebre frases longas em 2-3 curtas.
- Escreva "hum," "olha," "então" entre ideias fortes.
- Evite palavras que a voice clone pronuncia mal (teste antes).

Todos os roteiros abaixo já foram escritos seguindo essas regras.

## Custos de minutos no HeyGen Creator

Aproximadamente 15 minutos/mês incluídos. Consumo estimado:

| Vídeo | Duração | Cumulativo |
|--|--|--|
| reel-dia-01 apresentação | 90s | 1.5 min |
| reel-dia-03 salários | 60s | 2.5 min |
| reel-dia-09 terraform | 40s | 3.2 min |
| reel-dia-16 docker | 55s | 4.1 min |
| reel-dia-21 time-lapse | 30s | 4.6 min |
| reel-dia-26 saas | 60s | 5.6 min |
| 7 stories curtos x 15s | 1.75 min | 7.4 min |

**Total: ~7.5 min** — cabe confortável na cota Creator.

Se quiser fazer os 30 stories, aí estoura a cota — faça 7-10 e deixe os
outros 20 como carrossel estático (já cobertos no calendário XLSX).
