:: run commands below on terminal
:: winrm qc
:: winrm set winrm/config/service @{AllowUnencrypted="true"}

@echo off
setlocal enabledelayedexpansion

set count=0

for /f "tokens=*" %%x in (login_credentials.txt) do (
    set /a count+=1
    set var[!count!]=%%x
)

:: change registry values
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d Pat /f
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultDomainName /t REG_SZ /d DESKTOP-0K06L79 /f
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d Password /f

:: reboot system to use new credentials loaded
:: shutdown /r /t 00