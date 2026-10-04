# Script para registrar la tarea diaria en Windows Task Scheduler
param(
    [string]$Hora = "06:00"
)

$TaskName = "NoticIAs_Duo_Daily_Podcast"
$BatchPath = "C:\Carlos\noticias_podcast\run_daily_podcast.bat"

Write-Host "Configurando tarea programada '$TaskName' a las $Hora todos los días..."

$Action = New-ScheduledTaskAction -Execute $BatchPath
$Trigger = New-ScheduledTaskTrigger -Daily -At $Hora
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Genera automáticamente el podcast diario NoticIAs Dúo para Spotify"
    Write-Host "[OK] Tarea programada registrada exitosamente para ejecutarse a las $Hora diariamente." -ForegroundColor Green
} catch {
    Write-Host "Error al registrar la tarea: $($_.Exception.Message)" -ForegroundColor Red
}
