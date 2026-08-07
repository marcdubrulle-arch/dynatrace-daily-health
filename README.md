# dynatrace-daily-health

Daily Dynatrace health report:
- problems from the last 24h
- problems still open
- comparison with J-7
- application availability
- synthetic test results

## Configuration

### Required
- `DYNATRACE_BASE_URL` - Your Dynatrace environment URL (e.g., https://uxw82338.live.dynatrace.com)
- `DYNATRACE_API_TOKEN` - API token with read access to problems and metrics

### Optional
- `DYNATRACE_PROBLEM_SELECTOR` - Problem filter (default: all problems)
- `DYNATRACE_AVAILABILITY_METRIC_SELECTOR` - Availability metric (default: service availability)
- `OUTPUT_DIR` - Report output directory (default: `reports`)

### Email Configuration (Optional)
- `SMTP_SERVER` - SMTP server (e.g., smtp.gmail.com)
- `SMTP_PORT` - SMTP port (default: 587)
- `SMTP_USER` - SMTP username
- `SMTP_PASSWORD` - SMTP password
- `EMAIL_FROM` - Sender email address (defaults to `SMTP_USER` if omitted)
- `EMAIL_TO` - Recipient email addresses (comma-separated)

If `EMAIL_TO` is set, SMTP settings (`SMTP_SERVER`, `SMTP_USER`, `SMTP_PASSWORD`) must also be set.

## Run

```bash
python run_daily.py
```

## Output

- `reports/report_YYYY-MM-DD.md` - Markdown report
- `reports/report_YYYY-MM-DD.json` - JSON report
- Email sent to configured recipients (if email config provided)

## Creating a Dynatrace API Token

1. Go to **Settings → Identity → API tokens**
2. Click **Create new token**
3. Name: "Daily Health Check"
4. Add scopes:
   - `entities.read` - Read entities
   - `metrics.read` - Read metrics
   - `settings.read` - Read settings (optional)
5. Copy the token and set `DYNATRACE_API_TOKEN` environment variable
