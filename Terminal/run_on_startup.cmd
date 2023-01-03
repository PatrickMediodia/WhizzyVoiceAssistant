:: windows + r
:: shell:startup
:: paste cmd file into startup folder

:: run python scripts
python C:\Users\Pat\Documents\WhizzyVoiceAssistant\Terminal\server.py

:: turn off AutoAdminLogin on next startup
reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 0 /f