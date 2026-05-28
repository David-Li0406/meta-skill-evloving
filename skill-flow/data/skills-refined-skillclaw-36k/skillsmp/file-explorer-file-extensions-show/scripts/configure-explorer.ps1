# Set "Show hidden files, folders, and drives"
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "Hidden" -Value 1 -Force

# Uncheck "Hide extensions for known file types" (0 = Show extensions)
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "HideFileExt" -Value 0 -Force

Write-Host "Registry settings updated."
Write-Host "Restarting Windows Explorer to apply changes..."

# Restart Explorer
Stop-Process -ProcessName explorer
