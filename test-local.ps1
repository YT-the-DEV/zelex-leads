# Test Zelex Leads Locally
# Run this to test before pushing to GitHub

Write-Host "=== Zelex Leads - Local Test ===" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/3] Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python not found! Install from python.org" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "[2/3] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run scraper
Write-Host ""
Write-Host "[3/3] Running scraper (test mode)..." -ForegroundColor Yellow
$env:NICHE = "cafes"
$env:TARGET_CITIES = "New York"
python scraper.py

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Green
Write-Host ""

if (Test-Path "leads.csv") {
    Write-Host "Leads found!" -ForegroundColor Green
    $leads = Import-Csv "leads.csv"
    Write-Host "Total: $($leads.Count)" -ForegroundColor Cyan

    $priority = Import-Csv "leads_high_priority.csv" -ErrorAction SilentlyContinue
    if ($priority) {
        Write-Host "High Priority (no website): $($priority.Count)" -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "Preview first 5 leads:" -ForegroundColor Cyan
    $leads | Select-Object -First 5 name, website, needs_website, website_quality_score | Format-Table
} else {
    Write-Host "No leads generated - check scraper output" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review leads.csv"
Write-Host "2. Run: python outreach.py (dry-run mode without SENDGRID_API_KEY)"
Write-Host "3. Push to GitHub for automated daily runs"
