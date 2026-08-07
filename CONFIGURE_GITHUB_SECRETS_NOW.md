# ⚠️ URGENT: Configure GitHub Secrets Now!

## Problem Found
The workflow is failing because **GitHub Secrets are not configured**.

The workflow needs these secrets to run:
- `DYNATRACE_BASE_URL`
- `DYNATRACE_API_TOKEN`

Without them, the Python script exits with "CONFIG ERROR: DYNATRACE_BASE_URL is required" (exit code 1).

## Solution: Add Secrets to GitHub

### Step 1: Go to GitHub Secrets Settings
1. Open: https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions
2. Or: Repository → Settings → Secrets and variables → Actions

### Step 2: Create DYNATRACE_BASE_URL Secret
1. Click "New repository secret"
2. **Name**: `DYNATRACE_BASE_URL`
3. **Value**: `https://uxw82338.live.dynatrace.com`
4. Click "Add secret"

### Step 3: Create DYNATRACE_API_TOKEN Secret
1. Click "New repository secret"  
2. **Name**: `DYNATRACE_API_TOKEN`
3. **Value**: Copy the token from your `.env.local` file (do not share publicly)
4. Click "Add secret"

### Step 4 (Optional): Add Email Secrets
If you want to send email reports, also add:

- **Name**: `EMAIL_TO`
  - **Value**: `marc.dubrulle@orange.com`

- **Name**: `SMTP_SERVER`
  - **Value**: `smtp.orange.com`

- **Name**: `SMTP_PORT`
  - **Value**: `587`

## Step 5: Trigger Workflow
Once secrets are configured, the workflow will automatically run on the next push. Or manually trigger:

1. Go to: https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions
2. Click "Daily Dynatrace Health"
3. Click "Run workflow" button
4. Select branch: `main`
5. Click "Run workflow"

## Expected Result
After secrets are configured, the workflow should:
- ✅ Checkout code
- ✅ Setup Python
- ✅ Install dependencies  
- ✅ Generate report (SUCCESS)
- ✅ Upload artifacts

## Verification
To verify secrets were added correctly:
1. Go to Settings → Secrets and variables → Actions
2. You should see:
   - `DYNATRACE_BASE_URL` ✓
   - `DYNATRACE_API_TOKEN` ✓
   - `EMAIL_TO` (if added) ✓
   - `SMTP_SERVER` (if added) ✓
   - `SMTP_PORT` (if added) ✓

## Why This Happened
- The Python code checks for these secrets during startup
- If they're empty, it raises: `ValueError("DYNATRACE_BASE_URL is required")`
- This causes exit code 1 (failure)

## Next Steps
1. ✅ Configure the secrets in GitHub (you do this)
2. ✅ Trigger a test workflow run
3. ✅ Check logs for success

---

**Status**: Once you complete the above steps, the workflow will work! 🚀
