# Zelex Leads - Automated Lead Generation System

Fully automated lead generation for Zelex Studio web dev agency. Runs on **GitHub Actions** (free, 2000 min/month).

## What It Does

```
┌─────────────────────────────────────────────────────────────┐
│  Schedule (GitHub Actions)                                  │
│       ↓                                                     │
│  Scrape businesses (OpenStreetMap, public sources)          │
│       ↓                                                     │
│  Check if they have a website                               │
│       ↓                                                     │
│  Score website quality (mobile, HTTPS, SEO, speed)          │
│       ↓                                                     │
│  Save leads → CSV in your repo                              │
│       ↓                                                     │
│  Send personalized emails via SendGrid (100/day free)       │
│       ↓                                                     │
│  Generate IG DM templates for manual sending                │
└─────────────────────────────────────────────────────────────┘
```

## What It Does

1. **Scrapes** businesses from Google Maps / Yelp
2. **Verifies** if they have a poor/no website
3. **Scores** leads based on quality signals
4. **Outreach** via email (SendGrid) + social media

## Free Stack

- **Hosting:** GitHub Actions (2000 min/month free)
- **Email:** SendGrid (100 emails/day free)
- **Storage:** Google Sheets API / CSV in repo
- **Scraping:** Playwright + BeautifulSoup

## Quick Setup (5 minutes)

### Option A: Automated Setup

```powershell
cd "C:\Users\YATHARTH PC\zelex-leads"
.\setup.ps1
```

This will:
1. Initialize git repo
2. Create GitHub repo
3. Open secrets page for you

### Option B: Manual Setup

**Step 1: Push to GitHub**

```powershell
cd "C:\Users\YATHARTH PC\zelex-leads"
git init
git add .
git commit -m "Initial commit"
# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/zelex-leads.git
git push -u origin main
```

**Step 2: Enable GitHub Actions**

1. Go to your repo on GitHub
2. Click **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"**

**Step 3: Add Secrets**

Go to: `Settings → Actions → Secrets → New repository secret`

| Name | Value |
|------|-------|
| `SENDGRID_API_KEY` | Get from [sendgrid.com](https://sendgrid.com) (free account) |
| `FROM_EMAIL` | `hello@zelexstudio.in` |
| `FROM_NAME` | `Zelex Studio` |

**Step 4: Add Variables**

Go to: `Settings → Actions → Variables → New repository variable`

| Name | Value |
|------|-------|
| `NICHE` | `restaurants,cafes,salons,dentists,gyms` |
| `TARGET_CITIES` | `New York,London,Los Angeles,Chicago,Miami` |

### Get SendGrid API Key

1. Sign up at https://sendgrid.com (free - 100 emails/day)
2. Go to **Settings → API Keys**
3. Click **Create API Key**
4. Give it a name (e.g., "Zelex Leads")
5. Copy the key → paste in GitHub Secrets

## Usage

### Automatic (Scheduled)

Workflows run automatically:
- **Daily at 6 AM UTC** - Scrapes new leads
- **Daily at 8 AM UTC** - Sends outreach emails

### Manual Trigger

1. Go to **Actions** tab in your GitHub repo
2. Click **"Daily Lead Scraping"** or **"Daily Outreach"**
3. Click **"Run workflow"**
4. Wait 2-3 minutes
5. Download leads from **Artifacts** section

### Run Locally (Testing)

```powershell
pip install -r requirements.txt
python scraper.py
python outreach.py
python instagram_outreach.py
```

## Output Files

| File | Description |
|------|-------------|
| `leads.csv` | All scraped leads with website scores |
| `leads_high_priority.csv` | Businesses without websites (best leads) |
| `outreach_log.csv` | Email sending history |
| `ig_dm_templates.txt` | Instagram DM templates (copy-paste ready) |

## Free Limits

| Service | Free Tier | Notes |
|---------|-----------|-------|
| GitHub Actions | 2000 min/month | ~60 min/day average |
| SendGrid | 100 emails/day | Enough for small campaigns |
| OpenStreetMap | Unlimited | Rate-limited, be respectful |

## Customization

### Change Niches

Edit in GitHub: `Settings → Actions → Variables → NICHE`

Options: `restaurants, cafes, salons, dentists, gyms, plumbers, electricians, lawyers, accountants`

### Change Target Cities

Edit in GitHub: `Settings → Actions → Variables → TARGET_CITIES`

Focus on **US/UK cities** for higher conversion rates.

### Email Templates

Edit `outreach.py` to customize your email copy. Current templates:
- No website → "Quick question about your online presence"
- Poor website → "Idea to improve your website"

## Important Notes

### Legal Compliance

- Include unsubscribe option in emails (add manually)
- Only contact businesses you genuinely believe need your services
- Follow CAN-SPAM / GDPR rules for your region
- This tool is for **lead research**, not spam

### Best Practices

1. **Start small** - 20-30 emails/day to test
2. **Personalize** - Add specific details about each business
3. **Follow up** - Send 2-3 emails over 2 weeks
4. **Track responses** - Update `status` column in leads.csv
5. **Warm up your domain** - Don't send 100 emails day 1

### Instagram DM Tips

- Send 10-20 DMs/day max (avoid flagging)
- Use casual tone, not salesy
- Add value first (free mockup offer)
- Follow up after 3-4 days if no response

---

**Built for Zelex Studio** | https://zelexstudio.in
