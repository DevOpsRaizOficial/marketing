# Script PowerShell para criar uma Tarefa Agendada no Windows que publica
# automaticamente todo dia no horário definido no calendário.
#
# Rode uma vez como Administrador:
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#   .\agendar_task_windows.ps1
#
# A tarefa será criada com o nome "DEVOPSRAIZ - Publicar Instagram".
# Modifique HORA abaixo para o horário que você quer que o post saia.

$HORA = "08:00"
$SCRIPT_DIR = $PSScriptRoot
$PYTHON = (Get-Command python).Source
$ARGS = "`"$SCRIPT_DIR\instagram_publisher.py`" publish --today"

$action = New-ScheduledTaskAction -Execute $PYTHON -Argument $ARGS -WorkingDirectory $SCRIPT_DIR
$trigger = New-ScheduledTaskTrigger -Daily -At $HORA
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable

Register-ScheduledTask `
    -TaskName "DEVOPSRAIZ - Publicar Instagram" `
    -Description "Publica automaticamente o post do dia no @devopsraiz_oficial" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Force

Write-Host "OK — tarefa criada. Verifique em: Agendador de Tarefas do Windows."
Write-Host "Para testar agora:  python instagram_publisher.py dry-run --day 1"
