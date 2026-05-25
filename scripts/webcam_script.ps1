# 1. Voice prompt
(New-Object -ComObject SAPI.SpVoice).Speak('Hello you behind the Screen, I am inside your PC.')

# 2. Path Setup
$savePath = "$env:USERPROFILE\Pictures\Camera_Snapshot.bmp"
$toolPath = "$env:TEMP\CommandCam.exe"

# Ensure output directory exists
$dir = Split-Path $savePath
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }

# 3. Clean & Safe Download Configuration
if (-not (Test-Path $toolPath)) {
    Write-Host "Downloading CommandCam cleanly from the repository..." -ForegroundColor Cyan
    $sourceUrl = "https://github.com/tedburke/CommandCam/raw/refs/heads/master/CommandCam.exe"
    
    # Force modern security protocols to ensure a secure, encrypted download
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $sourceUrl -OutFile $toolPath -UseBasicParsing
}

# 4. Fully Automated Capture Sequence
if (Test-Path $toolPath) {
    Write-Host "Camera initializing. Get ready to smile!" -ForegroundColor Green
    
    # Runs CommandCam:
    # /filename sets where the image is saved
    # /delay 3000 adds a 3-second delay and opens a preview window so you can see yourself!
    & $toolPath /filename "$savePath" /preview /delay 3000
    
    Start-Sleep -Seconds 2
} else {
    Write-Host "Download failed. Please check your network connection." -ForegroundColor Red
    Exit
}

# 5. Clean up the tool immediately after capture so nothing is left behind
if (Test-Path $toolPath) { 
    Remove-Item $toolPath -Force 
    Write-Host "Temporary helper utility removed safely." -ForegroundColor Yellow
}

# 6. Load Win32 Wallpaper Sync Engine
$wpCode = @'
using System;
using System.Runtime.InteropServices;
public class Wallpaper {
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
}
'@

if (-not ([System.Management.Automation.PSTypeName]'Wallpaper').Type) {
    Add-Type -TypeDefinition $wpCode
}

# 7. Instantly apply the auto-captured photo as your background
if (Test-Path $savePath) {
    Set-ItemProperty -Path 'HKCU:\Control Panel\Desktop\' -Name 'Wallpaper' -Value $savePath

    $SPI_SETDESKWALLPAPER = 0x0014
    $SPIF_UPDATEINIFILE   = 0x01
    $SPIF_SENDCHANGE      = 0x02
    $fWinIni = $SPIF_UPDATEINIFILE -bor $SPIF_SENDCHANGE

    [Wallpaper]::SystemParametersInfo($SPI_SETDESKWALLPAPER, 0, $savePath, $fWinIni) | Out-Null
    Write-Host "Success! Your new wallpaper has been set automatically without a black screen." -ForegroundColor Green
} else {
    Write-Host "Could not generate camera snapshot." -ForegroundColor Red
}