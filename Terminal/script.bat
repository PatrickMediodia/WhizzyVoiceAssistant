@echo off
setlocal enabledelayedexpansion

set count=0

for /f "tokens=*" %%x in (credentials.txt) do (
    set /a count+=1
    set var[!count!]=%%x
)
echo %var[1]%
echo %var[2]%

reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f
reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d %var[1]% /f
reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultDomainName /t REG_SZ /d DESKTOP-H5PK9AA /f
reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d %var[2]%@ /f