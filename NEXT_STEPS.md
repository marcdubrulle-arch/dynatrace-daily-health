# ✅ Configuration Status & Next Steps

## ✅ What's Done

### 1. Dynatrace API Setup
- ✅ Dynatrace instance configured: `https://uxw82338.live.dynatrace.com`
- ✅ API token created and configured in GitHub Secrets

### 2. GitHub Repository Setup
- ✅ Repository: `marcdubrulle-arch/dynatrace-daily-health`
- ✅ Workflow file: `.github/workflows/daily-health.yml`
- ✅ Schedule: Daily at 18:00 UTC (plus manual trigger)
- ✅ Python scripts: `run_daily.py`, `src/dynatrace_client.py`, `src/email_sender.py`

### 3. New Helper Tools
- ✅ `TRIGGER_WORKFLOW_GUIDE.md` - Step-by-step guide to run workflow
- ✅ `GITHUB_SECRETS_CHECKLIST.md` - Checklist of all required secrets
- ✅ `trigger-workflow.ps1` - PowerShell script to trigger via API
- ✅ `verify_setup.py` - Python script to verify configuration

### 4. GitHub Secrets
- ✅ `DYNATRACE_API_TOKEN` - CONFIGURED (you just updated this!)
- ⚠️ `DYNATRACE_BASE_URL` - NEEDS TO BE CONFIGURED
- ⚠️ Other email secrets - OPTIONAL but recommended

---

## ⚠️ Next Steps (REQUIRED)

### Step 1: Configure Remaining GitHub Secrets

**Go to:** https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions

**Add these secrets:**

1. **DYNATRACE_BASE_URL**
   - Name: `DYNATRACE_BASE_URL`
   - Value: `https://uxw82338.live.dynatrace.com`
   - Click "Add secret"

2. **(Optional but Recommended) SMTP_SERVER**
   - Name: `SMTP_SERVER`
   - Value: `smtp.orange.com`

3. **(Optional but Recommended) SMTP_PORT**
   - Name: `SMTP_PORT`
   - Value: `587`

4. **(Optional but Recommended) EMAIL_FROM**
   - Name: `EMAIL_FROM`
   - Value: `marc.dubrulle@orange.com`

5. **(Optional but Recommended) EMAIL_TO**
   - Name: `EMAIL_TO`
   - Value: `marc.dubrulle@orange.com`

**For complete list, see:** `GITHUB_SECRETS_CHECKLIST.md`

### Step 2: Trigger a Test Workflow Run

**Option A (Easiest - via GitHub UI):**
1. Go to: https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions
2. Click "Daily Dynatrace Health" workflow
3. Look for "Run workflow" button
4. Click it, confirm branch is "main", click "Run workflow"

**Option B (via PowerShell script):**
```powershell
# First, get a GitHub Personal Access Token from:
# https://github.com/settings/tokens
# (Select "repo" and "workflow" scopes)

$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"
.\trigger-workflow.ps1
```

**Option C (via GitHub CLI, if installed):**
```bash
gh workflow run daily-health.yml --repo marcdubrulle-arch/dynatrace-daily-health
```

**See:** `TRIGGER_WORKFLOW_GUIDE.md` for detailed instructions

### Step 3: Verify Workflow Success

1. **Watch the workflow run:**
   - Go to: https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions
   - Click the latest run

2. **Check for success:**
   - Status should show: ✅ (green checkmark)
   - All steps should pass:
     - ✅ Checkout
     - ✅ Setup Python
     - ✅ Install dependencies
     - ✅ Generate report
     - ✅ Upload reports

3. **Verify logs show Dynatrace data:**
   - Click "Generate report" step
   - Look for lines like:
     ```
     DEBUG: DYNATRACE_BASE_URL = 'https://uxw82338.live.dynatrace.com'
     DEBUG: DYNATRACE_API_TOKEN length = 180
     DEBUG: Config validation passed
     ```

4. **Check email (if SMTP configured):**
   - You should receive an HTML email at `marc.dubrulle@orange.com`
   - Subject: `[Dynatrace] Daily Health Report`
   - Contains: Problems, Availability, Synthetic Tests data

---

## 📋 Configuration Reference

### What Each Secret Does

| Secret | Required? | Value | Example |
|--------|-----------|-------|---------|
| `DYNATRACE_API_TOKEN` | ✅ YES | Dynatrace API token | `dt0c01.xxxxx` |
| `DYNATRACE_BASE_URL` | ✅ YES | Dynatrace URL | `https://uxw82338.live.dynatrace.com` |
| `SMTP_SERVER` | ⚠️ Optional | Email server | `smtp.orange.com` |
| `SMTP_PORT` | ⚠️ Optional | Email port | `587` |
| `SMTP_USER` | ⚠️ Optional | Email username | your email |
| `SMTP_PASSWORD` | ⚠️ Optional | Email password | your password |
| `EMAIL_FROM` | ⚠️ Optional | Sender email | `marc.dubrulle@orange.com` |
| `EMAIL_TO` | ⚠️ Optional | Recipient email(s) | `marc.dubrulle@orange.com` |

### What Each Variable Does (Optional)

| Variable | Purpose | Default |
|----------|---------|---------|
| `DYNATRACE_PROBLEM_SELECTOR` | Filter which problems to include | (all problems) |
| `DYNATRACE_AVAILABILITY_METRIC_SELECTOR` | Filter availability metrics | builtin:service.availability |

---

## 🔧 Troubleshooting

### If Workflow Fails

1. **Click the failed run** in GitHub Actions
2. **Go to "Logs" tab**
3. **Find the error message**
4. **Compare with:** `DIAGNOSTIC_AND_SOLUTION.md`

### Common Errors

| Error | Solution |
|-------|----------|
| `DYNATRACE_API_TOKEN is required` | Add `DYNATRACE_API_TOKEN` secret |
| `HTTP 403 Forbidden` | Token is invalid or lacks permissions |
| `Connection refused` | Wrong `DYNATRACE_BASE_URL` |
| `ValueError: invalid literal for int()` | Empty `SMTP_PORT` secret (should be `587`) |
| `SMTP connection failed` | Wrong SMTP settings or Orange email auth issue |

---

## 📅 Automation

Once configured, the workflow runs **automatically**:

- **Daily at 18:00 UTC** (3.00 PM GMT-4) via schedule
- **On every push to main** (via push trigger)
- **On manual trigger** (via workflow_dispatch)

Each run:
1. Fetches data from Dynatrace API for last 24h and 7d
2. Analyzes problems, availability, synthetic tests
3. Generates markdown and JSON reports
4. Sends HTML email report (if SMTP configured)
5. Stores artifacts for download

---

## 📞 Getting Help

- **Configuration issues:** See `SETUP_GITHUB_SECRETS.md`
- **Workflow troubleshooting:** See `DIAGNOSTIC_AND_SOLUTION.md`
- **How to trigger workflow:** See `TRIGGER_WORKFLOW_GUIDE.md`
- **Checklist of all secrets:** See `GITHUB_SECRETS_CHECKLIST.md`

---

## 🎯 Summary

You have successfully:
1. ✅ Set up Dynatrace API integration
2. ✅ Created GitHub Actions workflow
3. ✅ Configured `DYNATRACE_API_TOKEN` in GitHub Secrets
4. ✅ Built helper tools for easy testing

**You are here:** Ready for testing! ← YOU ARE HERE

**Next:** Configure `DYNATRACE_BASE_URL` in GitHub Secrets, then trigger a test run to verify everything works end-to-end.

---

**Questions? See the guide files listed above or check GitHub Issues on the repository.**
