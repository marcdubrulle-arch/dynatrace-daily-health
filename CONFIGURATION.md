# Configuration Example - dynatrace-daily-health

## .env Example (for local testing)

```env
# Dynatrace Configuration
DYNATRACE_BASE_URL=https://uxw82338.live.dynatrace.com
DYNATRACE_API_TOKEN=dt0c01.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional: Problem selector filter
# DYNATRACE_PROBLEM_SELECTOR=

# Optional: Custom availability metric
# DYNATRACE_AVAILABILITY_METRIC_SELECTOR=builtin:service.availability:splitBy():sort(value(avg,descending))

# Output directory
# OUTPUT_DIR=reports

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your.email@gmail.com
EMAIL_TO=marc.dubrulle@orange.com
```

## Testing Locally

```bash
# Load environment from .env file
export $(cat .env | grep -v '#' | xargs)

# Run the daily health check
python run_daily.py
```

## GitHub Actions Secrets

The workflow reads from GitHub Secrets. Configure them at:
`https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions`

Required secrets:
- `DYNATRACE_BASE_URL`
- `DYNATRACE_API_TOKEN`

Optional secrets (for email):
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `EMAIL_FROM`
- `EMAIL_TO`

## Email Provider Examples

### Gmail
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=<app-specific-password>
```
⚠️ Use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.

### Orange Mail (Wanadoo)
```
SMTP_SERVER=smtp.wanadoo.fr
SMTP_PORT=587
SMTP_USER=your.email@wanadoo.fr
SMTP_PASSWORD=<your-password>
```

### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your.email@outlook.com
SMTP_PASSWORD=<your-password>
```

### Corporate Email (with STARTTLS)
```
SMTP_SERVER=mail.company.com
SMTP_PORT=587
SMTP_USER=user@company.com
SMTP_PASSWORD=<your-password>
```

## Schedule

The workflow runs daily at **18:00 UTC** (20:00 CEST in summer, 19:00 CET in winter).

To run immediately, trigger via:
- GitHub UI: Actions → Daily Dynatrace Health → Run workflow
- GitHub CLI: `gh workflow run daily-health.yml --repo marcdubrulle-arch/dynatrace-daily-health`

## Output

Each run generates:
- `reports/report_YYYY-MM-DD.md` - Markdown report
- `reports/report_YYYY-MM-DD.json` - JSON report
- Email notification (if configured)

Access reports via GitHub Actions artifacts.
