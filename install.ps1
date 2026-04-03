# Big-Jay AI-OS Smart Installer
$InstallPath = "C:\Big-Jay-AI-OS"
Write-Host "Cloning latest Big-Jay AI-OS from GitHub..."
git clone https://github.com/YOUR_USERNAME/Big-Jay-AI-OS.git $InstallPath

Write-Host "Setting up Python Environment..."
cd $InstallPath\Agents
python -m venv venv
.\venv\Scripts\pip.exe install -r ..\requirements.txt -q

Write-Host "Creating Desktop Shortcut..."
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$HOME\Desktop\Big-Jay AI-OS.lnk")
$Shortcut.TargetPath = "$InstallPath\START-BIG-JAY.bat"
$Shortcut.WorkingDirectory = "$InstallPath"
$Shortcut.IconLocation = "shell32.dll,25"
$Shortcut.Save()

Write-Host "Done! Launching Big-Jay..."
Start-Process "$InstallPath\START-BIG-JAY.bat"