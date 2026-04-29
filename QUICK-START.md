# ZELEX LEADS - Simple Setup (3 Steps)

> Your PC = just pushes code
> GitHub's cloud = does all scraping/emailing (FREE)

---

## Step 1: Create GitHub Account (if you don't have)

Go to: https://github.com/signup

---

## Step 2: Run These Commands

Open PowerShell and run:

```powershell
cd "C:\Users\YATHARTH PC\zelex-leads"

# Initialize git
git init
git add .
git commit -m "Zelex leads setup"

# Create new repo on GitHub (replace YOUR_USERNAME with your GitHub username)
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/zelex-leads.git
git push -u origin main
```

**How to create repo on GitHub:**
1. Go to https://github.com/new
2. Repo name: `zelex-leads`
3. Click **Create repository**
4. Copy the commands shown there (git remote add...)

---

## Step 3: Enable Automation on GitHub

1. Go to your repo: `https://github.com/YOUR_USERNAME/zelex-leads`
2. Click **Settings** (top right)
3. Click **Actions** (left sidebar) → **General**
4. Scroll down → Click **Allow all actions**
5. Go back to **Actions** tab → Click **Enable workflows**

---

## Step 4: Add SendGrid Key (For Emails)

**Get free API key:**
1. Go to https://sendgrid.com
2. Sign up (free)
3. Go to **Settings → API Keys**
4. Click **Create API Key**
5. Name: `Zelex Leads`, Permissions: **Full Access**
6. Copy the key

**Add to GitHub:**
1. Go to your repo → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `SENDGRID_API_KEY`
4. Value: (paste the key you copied)
5. Click **Add secret**

---

## Step 5: Done! Wait for Leads

- **Every day at 6 AM** → GitHub scrapes businesses automatically
- **Every day at 8 AM** → GitHub sends emails automatically
- Check your repo's `leads.csv` file for new leads
- Check `outreach_log.csv` for sent emails

---

## Manual Trigger (If You Want Leads NOW)

1. Go to your repo → **Actions** tab
2. Click **Daily Lead Scraping**
3. Click **Run workflow** (green button)
4. Wait 2-3 minutes
5. Refresh → Download leads from **Artifacts**

---

## That's It!

Your lead machine is running 24/7 on GitHub's servers (free).

**You just:**
- Check `leads.csv` daily
- Follow up with replies
- Close clients 💰

---

Questions? Message me!
