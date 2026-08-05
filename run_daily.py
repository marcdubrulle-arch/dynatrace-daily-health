from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.analyzer import analyze
from src.config import Config
from src.dynatrace_client import DynatraceClient
from src.report import write_outputs


def main() -> None:
    config = Config()
    config.validate()

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
    result = analyze(problems_24h, problems_7d, availability)
    md_path, json_path = write_outputs(result, config.output_dir, now)
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()

