@echo off
REM Script de ejecución diaria para NoticIAs Dúo Podcast
cd /d "C:\Carlos\noticias_podcast"
"C:\Carlos\conciliacion_financiera\venv\Scripts\python.exe" "C:\Carlos\noticias_podcast\generate_daily_episode.py" >> "C:\Carlos\noticias_podcast\daily_log.log" 2>&1
