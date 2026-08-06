# GitHub Secrets Configuration Checklist

## Required Secrets (MUST CONFIGURE)

### 1. ✅ DYNATRACE_API_TOKEN
- **Status:** ✅ CONFIGURED (vous l'avez mis à jour)
- **Value Format:** `dt0c01.xxxxxxxx...` (150+ characters)
- **Where to get:**
  - https://uxw82338.live.dynatrace.com/ui/settings/integration/apiTokens
- **Required Scopes:**
  - `entities.read`
  - `problems.read`
  - `metrics.read`
  - `settings.read`

### 2. ⚠️ DYNATRACE_BASE_URL
- **Status:** NEEDS VERIFICATION
- **Value:** `https://uxw82338.live.dynatrace.com`
- **Where to configure:**
  - https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions
  - Click "New repository secret"
  - Name: `DYNATRACE_BASE_URL`
  - Value: `https://uxw82338.live.dynatrace.com`

---

## Optional Secrets (For Email Reports)

### 3. SMTP_SERVER
- **Status:** NEEDS CONFIGURATION (for email)
- **Value:** `smtp.orange.com`
- **Default if not set:** Email won't be sent, but script will still work
- **Steps:**
  - Go to: https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions
  - Click "New repository secret"
  - Name: `SMTP_SERVER`
  - Value: `smtp.orange.com`

### 4. SMTP_PORT
- **Status:** NEEDS CONFIGURATION (for email)
- **Value:** `587`
- **Default if not set:** `587`
- **Steps:**
  - Name: `SMTP_PORT`
  - Value: `587`

### 5. SMTP_USER
- **Status:** NEEDS CONFIGURATION (optional, for SMTP auth)
- **Value:** Your Orange email username
- **Example:** `your.email@orange.com` or just the username part
- **Steps:**
  - Name: `SMTP_USER`
  - Value: Your Orange email credentials

### 6. SMTP_PASSWORD
- **Status:** NEEDS CONFIGURATION (optional, for SMTP auth)
- **Value:** Your Orange email password or app password
- **Important:** Never commit this! GitHub Secrets encrypts it.
- **Steps:**
  - Name: `SMTP_PASSWORD`
  - Value: Your password

### 7. EMAIL_FROM
- **Status:** NEEDS CONFIGURATION (optional, for email)
- **Value:** `noreply@dynatrace-health.local` or your Orange email
- **Example:** `marc.dubrulle@orange.com`
- **Steps:**
  - Name: `EMAIL_FROM`
  - Value: The sender email address

### 8. EMAIL_TO
- **Status:** NEEDS CONFIGURATION (optional, for email)
- **Value:** `marc.dubrulle@orange.com` (or multiple: `email1@example.com,email2@example.com`)
- **Steps:**
  - Name: `EMAIL_TO`
  - Value: `marc.dubrulle@orange.com`

---

## How to Add Secrets (Step-by-Step)

### Via Web UI:

1. **Go to Repository Settings:**
   - URL: https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions

2. **For each secret, click "New repository secret"**

3. **Fill in the form:**
   - **Name:** (exactly as listed above, case-sensitive)
   - **Value:** (the actual value)
   - Click **"Add secret"**

4. **Repeat for each secret**

### Via GitHub CLI (if installed):

```bash
# Substitute with actual values
gh secret set DYNATRACE_API_TOKEN -R marcdubrulle-arch/dynatrace-daily-health -b "dt0c01.xxxx..."
gh secret set DYNATRACE_BASE_URL -R marcdubrulle-arch/dynatrace-daily-health -b "https://uxw82338.live.dynatrace.com"
gh secret set SMTP_SERVER -R marcdubrulle-arch/dynatrace-daily-health -b "smtp.orange.com"
gh secret set SMTP_PORT -R marcdubrulle-arch/dynatrace-daily-health -b "587"
gh secret set EMAIL_FROM -R marcdubrulle-arch/dynatrace-daily-health -b "marc.dubrulle@orange.com"
gh secret set EMAIL_TO -R marcdubrulle-arch/dynatrace-daily-health -b "marc.dubrulle@orange.com"

# Verify
gh secret list -R marcdubrulle-arch/dynatrace-daily-health
```

---

## Verification Checklist

After configuring all secrets:

- [ ] DYNATRACE_API_TOKEN is set
- [ ] DYNATRACE_BASE_URL is set
- [ ] SMTP_SERVER is set (optional but recommended)
- [ ] SMTP_PORT is set (optional)
- [ ] EMAIL_FROM is set (optional)
- [ ] EMAIL_TO is set (optional)

**Next:** Run the workflow with:
```bash
gh workflow run daily-health.yml -R marcdubrulle-arch/dynatrace-daily-health
# OR visit:
# https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions/workflows/daily-health.yml
```

---

## What Each Secret Does

| Secret | Purpose | Required | Example |
|--------|---------|----------|---------|
| `DYNATRACE_API_TOKEN` | Authenticate to Dynatrace API | ✅ YES | `dt0c01.xxxxx` |
| `DYNATRACE_BASE_URL` | Dynatrace instance URL | ✅ YES | `https://uxw82338.live.dynatrace.com` |
| `SMTP_SERVER` | Email server | ⚠️ For email | `smtp.orange.com` |
| `SMTP_PORT` | Email server port | ⚠️ For email | `587` |
| `SMTP_USER` | Email auth username | ⚠️ Optional | `your.email@orange.com` |
| `SMTP_PASSWORD` | Email auth password | ⚠️ Optional | `yourpassword` |
| `EMAIL_FROM` | Sender email | ⚠️ For email | `marc.dubrulle@orange.com` |
| `EMAIL_TO` | Recipient email | ⚠️ For email | `marc.dubrulle@orange.com` |

---

## If Something Goes Wrong

1. **Check the workflow run logs:**
   - https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions

2. **Look for error messages:**
   - Missing secrets → "ValueError: DYNATRACE_API_TOKEN is required"
   - Wrong values → "HTTP 403 Forbidden" or "Connection refused"
   - SMTP errors → "SMTP connection failed"

3. **Consult:**
   - `DIAGNOSTIC_AND_SOLUTION.md` for detailed troubleshooting
   - `CONFIGURATION.md` for all configuration options

---

## Security Notes

⚠️ **IMPORTANT:**

- ✅ GitHub Secrets are **encrypted** and only accessible to the workflow
- ✅ Secrets are **never displayed** in logs
- ⚠️ Never put secrets in code, config files, or documentation
- ⚠️ If a secret is exposed, **regenerate it immediately**
- ⚠️ Personal Access Tokens with too many permissions are a security risk
  - Scope your token to only `repo` and `workflow` permissions
  - Use a separate token just for this workflow

