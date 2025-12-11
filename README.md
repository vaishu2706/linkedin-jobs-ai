# LinkedIn Jobs AI - Automated Job Matching System

Replaces your n8n workflow with a standalone Python application that fetches jobs, matches them using AI, and sends email alerts.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables in `.env`:**
   ```
   OPENAI_API_KEY=your_openai_api_key
   RESEND_API_KEY=your_resend_api_key
   FROM_EMAIL=your_email@domain.com
   TO_EMAIL=recipient@domain.com
   JOB_KEYWORDS=software engineer,developer,full stack
   LOCATION=remote,new york
   SCHEDULE=09:00
   ```

3. **Get API Keys:**
   - **OpenAI**: https://platform.openai.com/api-keys
   - **Resend**: https://resend.com/api-keys (free tier: 100 emails/day)

## Usage

**Run once:**
```bash
python main.py
```

**Install as Windows service (auto-start):**
```bash
install_service.bat
```

**Run service manually:**
```bash
python service.py
```

## Features

- ✅ Fetches jobs from Indeed & RemoteOK (free alternatives to Apify)
- ✅ AI-powered job matching using OpenAI
- ✅ AI-generated personalized emails
- ✅ Duplicate prevention
- ✅ Automated scheduling
- ✅ Email delivery via Resend API

## Customization

Edit the `user_profile` in `main.py` to match your preferences:

```python
self.user_profile = """
Your experience, skills, preferences...
"""
```

## Cost

- **OpenAI**: ~$0.01 per run (GPT-3.5-turbo)
- **Resend**: Free tier (100 emails/day)
- **Job APIs**: Free

Total: ~$0.30/month for daily runs