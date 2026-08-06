from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.analyzer import analyze
from src.config import Config
from src.dynatrace_client import DynatraceClient
from src.email_sender import EmailSender, build_email_html
from src.report import write_outputs


def main() -> None:
    try:
        config = Config()
        
        # Debug logging
        print(f"DEBUG: DYNATRACE_BASE_URL = '{config.base_url}'")
        if getattr(config, "base_url_was_normalized", False):
            print("DEBUG: DYNATRACE_BASE_URL was normalized to API endpoint format")
        print(f"DEBUG: DYNATRACE_API_TOKEN length = {len(config.api_token) if config.api_token else 0}")
        print(f"DEBUG: DYNATRACE_API_TOKEN prefix = '{config.api_token[:20] if config.api_token else 'EMPTY'}'")
        print(f"DEBUG: EMAIL_TO = '{config.email_to}'")
        
        config.validate()
        print("DEBUG: Config validation passed")
    except ValueError as e:
        print(f"CONFIG ERROR: {e}")
        raise
    except Exception as e:
        print(f"UNEXPECTED ERROR during config: {e}")
        raise

    client = DynatraceClient(config.base_url, config.api_token)
    now = datetime.now(timezone.utc)
    last_24h_start = now - timedelta(days=1)
    last_7d_start = now - timedelta(days=7)

    problems_24h = client.fetch_problems(last_24h_start, now, config.problem_selector)
    problems_7d = client.fetch_problems(last_7d_start, now, config.problem_selector)
    availability = client.fetch_application_availability(
        config.availability_metric_selector,
        last_24h_start,
        now,
    )
    synthetic_tests = client.fetch_synthetic_tests(last_24h_start, now)

    result = analyze(problems_24h, problems_7d, availability, synthetic_tests)
    md_path, json_path = write_outputs(result, config.output_dir, now)
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")

    # Send email report if configured
    if config.email_to and config.smtp_server:
        email_sender = EmailSender(
            config.smtp_server,
            config.smtp_port,
            config.smtp_user,
            config.smtp_password,
        )
        email_html = build_email_html(
            result.summary,
            result.open_problems,
            result.recurring_problems,
            result.availability,
            result.synthetic_tests,
        )
        email_sender.send_report(
            config.email_from,
            config.email_to,
            "[Dynatrace] Daily Health Report",
            email_html,
            md_path,
        )


if __name__ == "__main__":
    main()
