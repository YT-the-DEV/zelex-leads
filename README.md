# Lead Generation Automation

Automated lead scraping and outreach system. Runs on GitHub Actions (free 2000 min/month).

---

## What It Does

```
GitHub Actions (scheduled)
        ↓
Scrapes businesses (OpenStreetMap, public sources)
        ↓
Checks if they have a website
        ↓
Scores website quality (mobile, HTTPS, SEO, speed)
        ↓
Saves leads → CSV in your repo
        ↓
Sends personalized emails via SendGrid (100/day free)
        ↓
Generates IG DM templates for manual sending
```

---

## Quick Start (5 Minutes)

### Step 1: Fork/Clone This Repo

```bash
git clone https://github.com/YOUR_USERNAME/lead-automation.git
cd lead-automation
```

### Step 2: Push to Your GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/lead-automation.git
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Actions

1. Go to your repo on GitHub
2. Click **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"**

### Step 4: Add Secrets

Go to: `Settings → Actions → Secrets → New repository secret`

| Name | Value |
|------|-------|
| `SENDGRID_API_KEY` | Get from [sendgrid.com](https://sendgrid.com) (free account) |
| `FROM_EMAIL` | Your email address |
| `FROM_NAME` | Your name/company name |

### Step 5: Add Variables

Go to: `Settings → Actions → Variables → New repository variable`

| Name | Value |
|------|-------|
| `NICHE` | `restaurants,cafes,salons,dentists,gyms` |
| `TARGET_CITIES` | `New York,London,Los Angeles` |

---

## Get SendGrid API Key

1. Sign up at https://sendgrid.com (free - 100 emails/day)
2. Go to **Settings → API Keys**
3. Click **Create API Key**
4. Give it a name (e.g., "Lead Outreach")
5. Copy the key → paste in GitHub Secrets

---

## How to Run

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

```bash
pip install -r requirements.txt
python scraper.py
python outreach.py
python instagram_outreach.py
```

---

## Output Files

| File | Description |
|------|-------------|
| `leads.csv` | All scraped leads with website scores |
| `leads_high_priority.csv` | Businesses without websites (best leads) |
| `outreach_log.csv` | Email sending history |
| `ig_dm_templates.txt` | Instagram DM templates (copy-paste ready) |

---

## Free Stack Limits

| Service | Free Tier | Notes |
|---------|-----------|-------|
| GitHub Actions | 2000 min/month | ~60 min/day average |
| SendGrid | 100 emails/day | Enough for small campaigns |
| OpenStreetMap | Unlimited | Rate-limited, be respectful |

---

## Customization

### Change Niches

Edit in GitHub: `Settings → Actions → Variables → NICHE`

Options: `restaurants, cafes, salons, dentists, gyms, plumbers, electricians, lawyers, accountants`

### Change Target Cities

Edit in GitHub: `Settings → Actions → Variables → TARGET_CITIES`

Focus on **US/UK cities** for higher conversion rates.

### Email Templates

Edit `outreach.py` to customize your email copy.

---

## Important Notes

### Legal Compliance

- Include unsubscribe option in emails
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

## License

MIT License - Use freely for your business.
