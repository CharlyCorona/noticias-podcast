@echo off
REM ==========================================================
REM Pipeline Diario Automático: sIA -> GitHub -> Spotify
REM ==========================================================
cd /d "C:\Carlos\noticias_podcast"

echo [%date% %time%] Generando nuevo episodio diario con Jorge y Dalia... >> "C:\Carlos\noticias_podcast\daily_log.log" 2>&1
"C:\Carlos\noticias_podcast\venv\Scripts\python.exe" "C:\Carlos\noticias_podcast\generate_daily_episode.py" >> "C:\Carlos\noticias_podcast\daily_log.log" 2>&1

echo [%date% %time%] Sincronizando con GitHub... >> "C:\Carlos\noticias_podcast\daily_log.log" 2>&1
git add . >> "C:\Carlos\noticias_podcast\daily_log.log" 2>&1
git commit -m "Auto-update: Episodio del %date%" >> "C:\Carlos\noticias_podcast\daily_log.log" 2>&1
git push origin main >> "C:\Carlos\noticias_podcast\daily_log.log" 2>&1

echo [%date% %time%] Pipeline completado con éxito. >> "C:\Carlos\noticias_podcast\daily_log.log" 2>&1
