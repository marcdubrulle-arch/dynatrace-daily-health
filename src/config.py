from __future__ import annotations

import os


class Config:
    def __init__(self) -> None:
        self.base_url = os.environ.get("DYNATRACE_BASE_URL", "").rstrip("/")
        self.api_token = os.environ.get("DYNATRACE_API_TOKEN", "")
        self.problem_selector = os.environ.get("DYNATRACE_PROBLEM_SELECTOR", "")
        self.availability_metric_selector = os.environ.get(
            "DYNATRACE_AVAILABILITY_METRIC_SELECTOR",
            'builtin:service.availability:splitBy():sort(value(avg,descending))',
        )
        self.output_dir = os.environ.get("OUTPUT_DIR", "reports")

    def validate(self) -> None:
        if not self.base_url:
            raise ValueError("DYNATRACE_BASE_URL is required")
        if not self.api_token:
            raise ValueError("DYNATRACE_API_TOKEN is required")


