#!/usr/bin/env bash
# Script bash para adicionar entrada no crontab (Linux/macOS)
# que publica automaticamente todo dia às 08:00 no @devopsraiz_oficial.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$(command -v python3)"
CRON_LINE="0 8 * * * cd ${SCRIPT_DIR} && ${PYTHON_BIN} ${SCRIPT_DIR}/instagram_publisher.py publish --today >> ${SCRIPT_DIR}/publish.log 2>&1"

# Adiciona a linha somente se ainda não existir
(crontab -l 2>/dev/null | grep -v "instagram_publisher.py"; echo "${CRON_LINE}") | crontab -

echo "OK — cron agendado:"
echo "  ${CRON_LINE}"
echo ""
echo "Verificar:  crontab -l"
echo "Remover:    crontab -e  # apague a linha do instagram_publisher.py"
