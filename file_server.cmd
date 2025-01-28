@echo off
python -m http.server -d ./assets 2>nul
if %ERRORLEVEL%==0 exit /b 0

python3 -m http.server -d ./assets 2>nul
if %ERRORLEVEL%==0 exit /b 0

echo 无法搭建文件服务器：没有检测到命令行python
pause
exit