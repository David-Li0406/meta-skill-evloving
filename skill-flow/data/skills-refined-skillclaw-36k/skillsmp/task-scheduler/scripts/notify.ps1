param(
    [Parameter(Mandatory=$true)]
    [string]$title,
    [Parameter(Mandatory=$true)]
    [string]$content,
    [string]$icon
)

# Install and import BurntToast if not available
if (!(Get-Module -Name BurntToast -ListAvailable)) {
    try {
        Install-Module BurntToast -Force -Scope CurrentUser
    } catch {
        Write-Host "Failed to install BurntToast module: $_"
        exit
    }
}
Import-Module BurntToast

# Handle icon types
$iconPath = $null
if ($icon) {
    if ($icon -match "^(info|warning|error|success)$") {
        $index = switch ($icon) {
            "info" { 76 }
            "warning" { 102 }
            "error" { 100 }
            "success" { 101 }
        }
        Add-Type -AssemblyName System.Drawing
        $signature = @"
[DllImport("shell32.dll")]
public static extern IntPtr ExtractIcon(IntPtr hInst, string pszExeFileName, uint nIconIndex);
"@
        $type = Add-Type -MemberDefinition $signature -Name Shell32 -Namespace Win32 -PassThru
        $iconDll = [Environment]::SystemDirectory + "\imageres.dll"
        $iconHandle = $type::ExtractIcon([IntPtr]::Zero, $iconDll, $index)
        if ($iconHandle -ne [IntPtr]::Zero) {
            $sysIcon = [System.Drawing.Icon]::FromHandle($iconHandle)
            $tempDir = [System.IO.Path]::GetTempPath()
            $tempFile = Join-Path $tempDir ("notify_icon_" + [guid]::NewGuid().ToString() + ".png")
            $bitmap = $sysIcon.ToBitmap()
            $bitmap.Save($tempFile, [System.Drawing.Imaging.ImageFormat]::Png)
            $iconPath = $tempFile
        }
    } else {
        $iconPath = $icon
    }
}

# Show the toast notification
try {
    $text1 = New-BTText -Content $title
    $text2 = New-BTText -Content $content
    $binding = New-BTBinding -Children $text1, $text2
    if ($iconPath) {
        $image = New-BTImage -Source $iconPath -AppLogoOverride
        $binding = New-BTBinding -Children $text1, $text2 -AppLogoOverride $image
    }
    $visual = New-BTVisual -BindingGeneric $binding
    $toastContent = New-BTContent -Visual $visual -ActivationType Protocol -Launch 'powershell.exe -WindowStyle Hidden -Command exit'
    Submit-BTNotification -Content $toastContent
} catch {
    # Write-Host "Error showing toast: $_"
}