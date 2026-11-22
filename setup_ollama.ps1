<#
    setup_ollama.ps1 -- ONE file that sets up Ollama for TraceLite.

    It does everything in order:
      1. Installs Ollama into a folder you choose   (default: F:\Ollama)
      2. Stores AI models on a drive you choose      (default: F:\ollama-models)
      3. Starts the Ollama server
      4. Downloads the model you choose              (default: llama3.2)

    How to run it (from the project folder):
      powershell -ExecutionPolicy Bypass -File .\setup_ollama.ps1

    It is safe to run again: it skips steps that are already done.
#>

param(
    [string]$InstallDir = "F:\Ollama",
    [string]$ModelsDir  = "F:\ollama-models",
    [string]$Model      = "llama3.2",
    [string]$SetupPath  = "F:\OllamaSetup.exe"
)

$ErrorActionPreference = "Stop"
$ollamaExe = Join-Path $InstallDir "ollama.exe"

# --- 1. Install Ollama (only if not already there) -------------------------
if (-not (Test-Path $ollamaExe)) {
    if (-not (Test-Path $SetupPath)) {
        Write-Host "Ollama is not installed, and the installer was not found at:"
        Write-Host "  $SetupPath"
        Write-Host "Download it from https://ollama.com/download, then run this again"
        Write-Host "(or pass a custom path with -SetupPath)."
        exit 1
    }
    Write-Host "Installing Ollama into $InstallDir ..."
    Start-Process -FilePath $SetupPath -ArgumentList "/DIR=$InstallDir" -Wait
} else {
    Write-Host "Ollama is already installed at $InstallDir"
}

# --- 2. Put AI models on the chosen drive ----------------------------------
New-Item -ItemType Directory -Force -Path $ModelsDir | Out-Null
[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $ModelsDir, "User")
$env:OLLAMA_MODELS = $ModelsDir
Write-Host "Models will be stored in $ModelsDir"

# --- 3. Start the server (with the env var set, so it uses our folder) ------
Write-Host "Starting the Ollama server ..."
Start-Process -FilePath $ollamaExe -ArgumentList "serve" -WindowStyle Hidden

$up = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 2
    try {
        Invoke-RestMethod -Uri http://localhost:11434/api/tags -TimeoutSec 3 | Out-Null
        $up = $true
        break
    } catch { }
}
if ($up) { Write-Host "Server is up at http://localhost:11434" }
else     { Write-Host "Warning: the server has not answered yet; continuing anyway." }

# --- 4. Download the model -------------------------------------------------
Write-Host "Downloading model '$Model' (this can take a while) ..."
& $ollamaExe pull $Model

Write-Host ""
Write-Host "All done."
Write-Host "  Program : $ollamaExe"
Write-Host "  Models  : $ModelsDir"
Write-Host "  Server  : http://localhost:11434"
