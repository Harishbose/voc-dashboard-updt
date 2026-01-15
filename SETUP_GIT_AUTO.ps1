# Automated Git Setup for VOC Dashboard
# This script initializes git, configures it, and pushes to GitHub

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  VOC DASHBOARD - AUTOMATED GIT SETUP" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Get current directory
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath
Write-Host "Project Path: $projectPath" -ForegroundColor Yellow
Write-Host ""

# Check if git is installed
Write-Host "Checking Git installation..." -ForegroundColor Green
$gitCheck = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Git found: $gitCheck" -ForegroundColor Green
Write-Host ""

# Get GitHub credentials
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  GITHUB CONFIGURATION" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$githubUsername = Read-Host "Enter your GitHub username (e.g., Harishbose)"
$githubEmail = Read-Host "Enter your GitHub email"
$githubToken = Read-Host "Enter your GitHub Personal Access Token (paste from github.com/settings/tokens)" -AsSecureString

# Convert secure string to plain text for use
$tokenPlainText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicodePtr($githubToken))

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  INITIALIZING GIT REPOSITORY" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git repo already exists
if (Test-Path "$projectPath\.git") {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "Initializing new git repository..." -ForegroundColor Yellow
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to initialize git repo" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}
Write-Host ""

# Configure git user
Write-Host "Configuring git user..." -ForegroundColor Yellow
git config user.name "$githubEmail"
git config user.email "$githubEmail"
Write-Host "✓ Git user configured" -ForegroundColor Green
Write-Host ""

# Add all files
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to add files" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Files added" -ForegroundColor Green
Write-Host ""

# Create initial commit
Write-Host "Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: VOC Dashboard - Automated setup"
if ($LASTEXITCODE -eq 1) {
    Write-Host "Note: Commit may have been skipped (files already committed)" -ForegroundColor Yellow
}
Write-Host "✓ Commit created/verified" -ForegroundColor Green
Write-Host ""

# Set main branch
Write-Host "Setting branch to main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✓ Branch set to main" -ForegroundColor Green
Write-Host ""

# Add remote
Write-Host "Adding remote repository..." -ForegroundColor Yellow
$remoteUrl = "https://$($githubUsername):$($tokenPlainText)@github.com/$($githubUsername)/voc-dashboard.git"

# Check if remote already exists
$existingRemote = git remote get-url origin 2>&1
if ($existingRemote -match "voc-dashboard") {
    Write-Host "Remote already exists, updating..." -ForegroundColor Yellow
    git remote remove origin
}

git remote add origin $remoteUrl
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to add remote" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Remote repository configured" -ForegroundColor Green
Write-Host ""

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "(This may take a moment...)" -ForegroundColor Gray
git push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
    Write-Host "Possible issues:" -ForegroundColor Yellow
    Write-Host "  - Invalid GitHub token" -ForegroundColor Yellow
    Write-Host "  - Repository doesn't exist at github.com/$githubUsername/voc-dashboard" -ForegroundColor Yellow
    Write-Host "  - Token has expired or insufficient permissions" -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Yellow
    Write-Host "Solution: Create the repo first at https://github.com/new" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
Write-Host ""

# Display summary
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your repository is now live at:" -ForegroundColor Green
Write-Host "  https://github.com/$githubUsername/voc-dashboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step - Deploy to Render:" -ForegroundColor Yellow
Write-Host "  1. Go to https://render.com" -ForegroundColor Yellow
Write-Host "  2. Click 'New +' → 'Web Service'" -ForegroundColor Yellow
Write-Host "  3. Connect your GitHub account" -ForegroundColor Yellow
Write-Host "  4. Select voc-dashboard repository" -ForegroundColor Yellow
Write-Host "  5. Configure:" -ForegroundColor Yellow
Write-Host "     - Build Command: pip install -r requirements.txt" -ForegroundColor Yellow
Write-Host "     - Start Command: gunicorn app:app" -ForegroundColor Yellow
Write-Host ""
Write-Host "Your app will be live in 5-10 minutes!" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
