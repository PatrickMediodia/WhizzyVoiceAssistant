taskkill /F /IM Teams.exe
taskkill /F /IM msteams.exe
taskkill /F /IM Microsoft.AAD.BrokerPlugin.exe
del C:\Users\%username%\AppData\Roaming\Microsoft\Teams\desktop-config.json /q
rmdir C:\Users\%username%\AppData\Local\Packages\Microsoft.AAD.BrokerPlugin_cw5n1h2txyewy /s /q

:: Deletes all the teams cache
::del C:\Users\%username%\AppData\Roaming\Microsoft\Teams\ /s /q 