# dynatrace-daily-health

Daily Dynatrace health report:
- problems from the last 24h
- problems still open
- comparison with J-7
- application availability

## Configuration

Set:
- `DYNATRACE_BASE_URL`
- `DYNATRACE_API_TOKEN`
- `DYNATRACE_PROBLEM_SELECTOR` (optional)
- `DYNATRACE_AVAILABILITY_METRIC_SELECTOR` (optional)

## Run

```bash
python run_daily.py
```

## Output

- `reports/report_YYYY-MM-DD.md`
- `reports/report_YYYY-MM-DD.json`

