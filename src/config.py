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
        
        # Email configuration
        self.smtp_server = os.environ.get("SMTP_SERVER", "").strip()
        smtp_port_str = os.environ.get("SMTP_PORT", "").strip()
        self.smtp_port = int(smtp_port_str) if smtp_port_str else 587
        self.smtp_user = os.environ.get("SMTP_USER", "").strip()
        self.smtp_password = os.environ.get("SMTP_PASSWORD", "")
        self.email_from = os.environ.get("EMAIL_FROM", "").strip()
        email_to_str = os.environ.get("EMAIL_TO", "").strip()
        self.email_to = [e.strip() for e in email_to_str.split(",") if e.strip()]

    def validate(self) -> None:
        if not self.base_url:
            raise ValueError("DYNATRACE_BASE_URL is required")
        if not self.api_token:
            raise ValueError("DYNATRACE_API_TOKEN is required")


