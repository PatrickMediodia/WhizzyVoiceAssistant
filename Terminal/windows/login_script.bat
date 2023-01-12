:: Useful Links
:: Documentation : https://learn.microsoft.com/en-us/windows/win32/winrm/installation-and-configuration-for-windows-remote-management
:: Guide : https://stackoverflow.com/questions/32324023/how-to-connect-to-remote-machine-via-winrm-in-python-pywinrm-using-domain-acco
:: Pywinrm Documentation : https://github.com/diyan/pywinrm

:: Execute the following commands below (admin)
:: cmd
::      winrm qc / winrm quickconfig
::      winrm set winrm/config/service @{AllowUnencrypted="false"}
::      winrm set winrm/config/service/auth @{Basic="false"}
::      winrm set winrm/config/client/auth @{Basic="false"}
:: powershell
::      Invoke-Expression ((New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1'))

:: Change settings in services
:: 1. windows + r
:: 2. services.msc
:: 3. locate "Windows Remote Management" service
:: 4. go to properties and set startup type from "Automatic (Delayed Start) to Automatic"
:: 5. click apply then ok

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