# Zelex Leads - Quick Setup Script
# Run this to set up your GitHub repo

Write-Host "=== Zelex Leads Setup ===" -ForegroundColor Cyan
Write-Host ""

$repoName = "zelex-leads"
$githubUser = Read-Host "Enter your GitHub username"

if (-not $githubUser) {
    Write-Host "Username required!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[1/4] Initializing git repo..." -ForegroundColor Yellow
git init
git add .
git commit -m "Initial commit: Zelex Leads automation"

Write-Host ""
Write-Host "[2/4] Creating GitHub repo..." -ForegroundColor Yellow
gh repo create "$repoName" --public --source=. --remote=origin --push

Write-Host ""
Write-Host "[3/4] Enabling GitHub Actions..." -ForegroundColor Yellow
Write-Host "Go to: https://github.com/$githubUser/$repoName/actions" -ForegroundColor Green
Write-Host "Click 'I understand my workflows, go ahead and enable them'" -ForegroundColor Green
Read-Host "Press Enter after enabling Actions..."

Write-Host ""
Write-Host "[4/4] Configure secrets in GitHub:" -ForegroundColor Yellow
Write-Host "URL: https://github.com/$githubUser/$repoName/settings/secrets/actions" -ForegroundColor Green
Write-Host ""
Write-Host "Add these secrets:" -ForegroundColor White
Write-Host "  SENDGRID_API_KEY = (get from sendgrid.com)" -ForegroundColor Gray
Write-Host "  FROM_EMAIL = hello@zelexstudio.in" -ForegroundColor Gray
Write-Host "  FROM_NAME = Zelex Studio" -ForegroundColor Gray
Write-Host ""
Write-Host "Add these variables:" -ForegroundColor White
Write-Host "  NICHE = restaurants,cafes,salons,dentists" -ForegroundColor Gray
Write-Host "  TARGET_CITIES = New York,London,Los Angeles" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to open GitHub secrets page..."
Start-Process "https://github.com/$githubUser/$repoName/settings/secrets/actions"

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Add secrets in GitHub (see above)"
Write-Host "2. Workflows run daily at 6 AM UTC"
Write-Host "3. Manual trigger: Actions tab → Run workflow"
Write-Host "4. Download leads from Actions → Artifacts"
