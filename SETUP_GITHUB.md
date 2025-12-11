# GitHub Actions Setup - Automatic Job Alerts

## 🚀 One-time Setup (5 minutes)

### 1. Create GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/linkedin-jobs-ai.git
git push -u origin main
```

### 2. Add Secrets (GitHub Repository → Settings → Secrets and variables → Actions)

**Secrets:**
- `OPENAI_API_KEY` = your_openai_api_key
- `RESEND_API_KEY` = your_resend_api_key  
- `FROM_EMAIL` = your_email@domain.com
- `TO_EMAIL` = recipient@domain.com

**Variables:**
- `JOB_KEYWORDS` = software engineer,developer,python
- `LOCATION` = remote,new york

### 3. Enable Actions
- Go to repository → Actions tab
- Click "I understand my workflows, go ahead and enable them"

## ✅ That's it! 

Your job alerts will now run automatically:
- **Daily at 9 AM UTC** (Monday-Friday)
- **Completely free** (GitHub Actions free tier: 2000 minutes/month)
- **No maintenance** required

## 🔧 Manual Test
- Go to Actions tab → "Daily Job Alerts" → "Run workflow"

## 📧 Results
You'll receive emails only when matching jobs are found. No spam!