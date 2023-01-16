# Open Powershell in administrator mode
# Install-Module -Name PowerShellGet -Force -AllowClobber (update to latest powershellget)
# Install-Module -Name MicrosoftTeams -Force -AllowClobber

'''
$username = "pmediodia@live.mcl.edu.ph"
$passwd = "Dominican1234@"
$secpasswd = ConvertTo-SecureString -String $passwd -AsPlainText -Force
$cred = New-Object Management.Automation.PSCredential ($username, $secpasswd)
Connect-MicrosoftTeams -Credential $cred
'''

Connect-MicrosoftTeams