:: windows + r
:: shell:common startup
:: paste cmd file into startup folder

:: run python script
python C:\Users\Pat\Documents\WhizzyVoiceAssistant\Terminal\server.py

:: turn off AutoAdminLogin on next startup
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 0 /f