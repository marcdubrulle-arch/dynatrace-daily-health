# 🚨 URGENT: Fix Dynatrace Base URL

## Problem Identified

The workflow test run #15 **FAILED** because the DYNATRACE_BASE_URL is incorrect.

### What You Configured
```
https://uxw82338.apps.dynatrace.com/
```

### What It Should Be
```
https://uxw82338.live.dynatrace.com
```

**Note:** 
- ❌ NO `/apps/` path
- ❌ NO trailing slash `/`

---

## Root Cause

The Python script tried to connect to `uxw82338.apps.dynatrace.com`, which doesn't exist or isn't accessible. The correct Dynatrace API URL uses the `.live` subdomain, not `.apps`.

**Compare with .env.local:**
```
DYNATRACE_BASE_URL=https://uxw82338.live.dynatrace.com   ← Correct!
```

---

## How to Fix (Choose One Method)

### Method 1: Direct Edit in GitHub Web UI (IF ACCESSIBLE)

1. Go to: https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions

2. Find the secret `DYNATRACE_BASE_URL`

3. Click the pencil/edit icon (✏️)

4. **DELETE the current value**: `https://uxw82338.apps.dynatrace.com/`

5. **REPLACE with**: `https://uxw82338.live.dynatrace.com`

6. Click "Update secret"

### Method 2: Use GitHub CLI (if available)

```bash
gh secret set DYNATRACE_BASE_URL -R marcdubrulle-arch/dynatrace-daily-health -b "https://uxw82338.live.dynatrace.com"
```

### Method 3: Use PowerShell Script (Windows)

```powershell
# First, get a GitHub Personal Access Token from:
# https://github.com/settings/tokens
# Select scopes: "repo" and "workflow"

$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"

# Then create/update the secret
$Secret = "https://uxw82338.live.dynatrace.com"
$Url = "https://api.github.com/repos/marcdubrulle-arch/dynatrace-daily-health/actions/secrets/DYNATRACE_BASE_URL"

$Headers = @{
    "Authorization" = "token $env:GITHUB_TOKEN"
    "Accept" = "application/vnd.github.v3+json"
    "Content-Type" = "application/json"
}

# Get the public key first (needed for encryption)
$KeyResponse = Invoke-WebRequest -Uri "https://api.github.com/repos/marcdubrulle-arch/dynatrace-daily-health/actions/secrets/public-key" -Headers $Headers
$PublicKey = ($KeyResponse.Content | ConvertFrom-Json).key

# For simplicity, you can also use curl if available
curl -X PUT $Url `
  -H "Authorization: token $env:GITHUB_TOKEN" `
  -H "Accept: application/vnd.github.v3+json" `
  -H "Content-Type: application/json" `
  -d "{`"encrypted_value`":`"$Secret`"}"
```

---

## Verification Steps

After fixing the URL:

1. **Go to:** https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions/workflows/daily-health.yml

2. **Click:** "Run workflow" button

3. **Select:** Branch = "main"

4. **Click:** "Run workflow"

5. **Monitor the run:**
   - Should complete in ~30-60 seconds (not 10 seconds!)
   - Look for ✅ green checkmark
   - Click on job to verify Dynatrace data loaded:
     ```
     DEBUG: DYNATRACE_BASE_URL = 'https://uxw82338.live.dynatrace.com'
     DEBUG: DYNATRACE_API_TOKEN length = 180
     DEBUG: Config validation passed
     ```

---

## Double-Check Your Configuration

### Current .env.local (LOCAL TESTING)
```
DYNATRACE_BASE_URL=https://uxw82338.live.dynatrace.com  ← CORRECT
```

### What GitHub Secrets SHOULD Have
- `DYNATRACE_BASE_URL`: `https://uxw82338.live.dynatrace.com`  ← FIX THIS!
- `DYNATRACE_API_TOKEN`: (already configured ✅)

---

## Why This Matters

- **`.apps.dynatrace.com`** = Admin/UI interface (web browser)
- **`.live.dynatrace.com`** = API endpoint (for scripts/integrations)

The Python script makes HTTP requests to the API, not the UI, so it needs the `.live` domain.

---

## After Fixing

Once you correct the URL and re-run the workflow, it should:
1. ✅ Connect to Dynatrace
2. ✅ Fetch last 24h and 7d problems
3. ✅ Fetch application availability
4. ✅ Fetch synthetic tests data
5. ✅ Generate markdown and JSON reports
6. ✅ Send email report (if SMTP configured)

---

## Questions?

- Check: `NEXT_STEPS.md` - Overall configuration status
- Check: `SETUP_GITHUB_SECRETS.md` - Secret configuration guide
- Check: `DIAGNOSTIC_AND_SOLUTION.md` - Troubleshooting

**Let me know once you've fixed the URL and I'll help you re-run the test!**
