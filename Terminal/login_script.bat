:: run commands below on terminal
:: winrm qc
:: winrm set winrm/config/service @{AllowUnencrypted="true"}

@echo off
setlocal enabledelayedexpansion

:: change registry values
:: get data as parameters; irst (%1) -> username, second (%2) -> password, third (%3) -> domain
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d %1 /f
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d %2 /f
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultDomainName /t REG_SZ /d %3 /f

:: reboot system to use new credentials loaded
shutdown /r /t 00