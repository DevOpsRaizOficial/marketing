# ============================================================
# PUSH inicial do kit marketing pro repo DevOpsRaizOficial/marketing
# ============================================================
# Rode UMA vez no PowerShell (pode ser o mesmo do projeto):
#   cd "C:\Users\Tiago\OneDrive - TR99\Documentos\Claude\Projects\Ebooks-DevopsRaiz\marketing"
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#   .\PUSH_REPO.ps1
#
# O script:
#  1. Inicializa git local se ainda não inicializou
#  2. Aponta origin pro seu repo GitHub
#  3. Verifica que o .env NÃO está sendo commitado (segurança)
#  4. Faz commit e push
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host "Preparando push para DevOpsRaizOficial/marketing..." -ForegroundColor Cyan

# 1) Garante que está na pasta marketing/
if (-not (Test-Path "automacao" -PathType Container)) {
    Write-Host "ERRO: rode este script DE DENTRO da pasta 'marketing/'" -ForegroundColor Red
    exit 1
}

# 2) Inicializa git se ainda não é repo
if (-not (Test-Path ".git" -PathType Container)) {
    Write-Host "→ Inicializando git local..." -ForegroundColor Yellow
    git init
    git branch -M main
}

# 3) Adiciona remote se ainda não tem
$currentRemote = git remote get-url origin 2>$null
if (-not $currentRemote) {
    Write-Host "→ Configurando remote origin..." -ForegroundColor Yellow
    git remote add origin https://github.com/DevOpsRaizOficial/marketing.git
}
elseif ($currentRemote -notmatch "DevOpsRaizOficial/marketing") {
    Write-Host "⚠ Remote origin aponta pra outro repo: $currentRemote" -ForegroundColor Yellow
    Write-Host "   Atualizando para DevOpsRaizOficial/marketing..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/DevOpsRaizOficial/marketing.git
}

# 4) VERIFICAÇÃO DE SEGURANÇA - não deixar .env escapar
$dotEnvStaged = git status --porcelain automacao/.env 2>$null
if ($dotEnvStaged) {
    Write-Host "⚠ .env está sendo rastreado! Removendo do index..." -ForegroundColor Yellow
    git rm --cached automacao/.env 2>$null
}

# 5) Adiciona arquivos
Write-Host "→ Adicionando arquivos..." -ForegroundColor Yellow
git add .
git status --short

# 6) Confirma que .env NÃO está no commit
$envInCommit = git diff --cached --name-only | Select-String "\.env$"
if ($envInCommit) {
    Write-Host "❌ ABORTANDO: .env está no commit!" -ForegroundColor Red
    Write-Host "   Arquivo: $envInCommit"
    Write-Host "   Rode: git rm --cached automacao/.env"
    exit 1
}

# 7) Commit
Write-Host "→ Criando commit..." -ForegroundColor Yellow
git commit -m "feat: kit completo de marketing DEVOPSRAIZ

- calendario-editorial-30-dias.xlsx (30 posts planejados)
- 11 criativos PNG prontos para Instagram
- roteiros para vídeos HeyGen (5 Reels + 10 Stories)
- scripts Python: instagram_publisher, reels_publisher, heygen_client
- GitHub Actions workflow publish-daily.yml
- posts_prontos/ com legendas formatadas para Business Suite
- documentação: README, SETUP, CAMPANHAS_PAGAS, BUSINESS_SUITE"

# 8) Push (pode abrir prompt de autenticação GitHub)
Write-Host "→ Fazendo push para main..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "✓ Push concluído!" -ForegroundColor Green
Write-Host ""
Write-Host "PRÓXIMO PASSO:" -ForegroundColor Cyan
Write-Host "  Volta pro Chrome e recarrega a aba de 'New release'."
Write-Host "  A tag v1.0.0 agora vai apontar pro commit que acabou de subir."
Write-Host "  Publica o release e aí subimos os PNGs como assets."
