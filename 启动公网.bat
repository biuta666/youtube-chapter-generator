@echo off
chcp 65001 >nul
title YouTube Chapter Generator

echo ============================================
echo   YouTube Chapter Generator
echo   公网部署: 零注册 零登录
echo ============================================
echo.

:: 先杀死旧进程
echo [1] 清理旧进程...
taskkill /f /im cloudflared.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: 启动Streamlit
echo [2] 启动本地服务...
start /B python -m streamlit run "F:\KTV视频自动化程序备份\creator_toolkit\app.py" --server.port 8501 --server.headless true
timeout /t 10 /nobreak >nul

:: 启动Cloudflare Tunnel
echo [3] 创建公网隧道...
echo.
echo ============================================
echo   下方出现 https://xxx.trycloudflare.com
echo   就是你的公网地址，发给任何人即可访问
echo ============================================
echo.

"F:\temp\cloudflared.exe" tunnel --url http://localhost:8501
