:: logouts the current teams user
taskkill /IM "Teams.exe" /F 
taskkill /IM "Microsoft.AAD.BrokerPlugin.exe" /F 
del C:\Users\%username%\AppData\Roaming\Microsoft\Teams\desktop-config.json /q 
rd C:\Users\%username%\AppData\Local\Packages\Microsoft.AAD.BrokerPlugin_cw5n1h2txyewy /s /q