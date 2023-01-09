set wshShell= CreateObject("WScript.Shell")
WScript.Sleep 10000
wshShell.SendKeys "{ENTER}"
WScript.sleep 50
wshShell.SendKeys "password"
WScript.sleep 50
wshShell.SendKeys "{ENTER}"