@echo off
cd /d "%~dp0"

echo 必要なライブラリをチェック・インストール中...
pip install --quiet requests beautifulsoup4 pandas openpyxl lxml

echo アプリを起動します...
python gui_app.py
pause
