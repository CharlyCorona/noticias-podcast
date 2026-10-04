@echo off
title Subir Podcast a GitHub
cd /d "C:\Carlos\noticias_podcast"
echo ======================================================
echo    SUBIENDO PODCAST A GITHUB (noticias-podcast)
echo ======================================================
echo.
git push -u origin main
echo.
echo ======================================================
echo    PROCESO COMPLETADO
echo ======================================================
pause
