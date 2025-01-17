:: Old
::      windows + r
::      shell:common startup
::      paste shortcut of cmd file into startup folder
::      goto properties -> shortcut -> advanced -> select "run as administrator"

:: New
::      open task scheduler
::      create basic task
::      start on "When I log on"
::      action is "Start a program"
::      select the program/script
::      after creation, click the created task
::      click on "Change User or Group"
::      input "Users" so that it will run for all users
::      select "Run only when user is logged on"
::      check "Run with highest privileges"
::      triggers tab -> click trigger -> select "any user"
::      conditions tab -> power -> start uncheck power checkboxes

:: turn off AutoAdminLogin on next startup
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 0 /f

:: delete registry entries of credentials
reg delete "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /f
reg delete "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /f