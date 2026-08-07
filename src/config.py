from __future__ import annotations

import os
from urllib.parse import urlsplit


class Config:
    def __init__(self) -> None:
        self.base_url, self.base_url_was_normalized = _normalize_base_url(
            os.environ.get("DYNATRACE_BASE_URL", "")
        )
        self.api_token = os.environ.get("DYNATRACE_API_TOKEN", "").strip()
        self.problem_selector = os.environ.get("DYNATRACE_PROBLEM_SELECTOR", "").strip()
        self.availability_metric_selector = _get_env_or_default(
            "DYNATRACE_AVAILABILITY_METRIC_SELECTOR",
            "(builtin:synthetic.browser.availability:splitBy(dt.entity.synthetic_test):avg:sort(value(avg,descending)):limit(20)):limit(100):names",
        )
        self.output_dir = os.environ.get("OUTPUT_DIR", "reports")
        
        # Email configuration
        self.smtp_server = os.environ.get("SMTP_SERVER", "").strip()
        smtp_port_str = os.environ.get("SMTP_PORT", "").strip()
        self.smtp_port = int(smtp_port_str) if smtp_port_str else 587
        self.smtp_user = os.environ.get("SMTP_USER", "").strip()
        self.smtp_password = os.environ.get("SMTP_PASSWORD", "")
        email_from_str = os.environ.get("EMAIL_FROM", "").strip()
        self.email_from = email_from_str or self.smtp_user
        email_to_str = os.environ.get("EMAIL_TO", "").strip()
        self.email_to = [e.strip() for e in email_to_str.split(",") if e.strip()]

    def validate(self) -> None:
        if not self.base_url:
            raise ValueError("DYNATRACE_BASE_URL is required")
        if not self.api_token:
            raise ValueError("DYNATRACE_API_TOKEN is required")


def _normalize_base_url(raw_value: str) -> tuple[str, bool]:
    raw = raw_value.strip()
    if not raw:
        return "", False

    candidate = raw if "://" in raw else f"https://{raw}"
    parsed = urlsplit(candidate)

    # urlsplit("host-only") places value into path, so handle both netloc and path.
    host = (parsed.netloc or parsed.path).strip().lower()
    if not host:
        return "", False

    if host.endswith(".apps.dynatrace.com"):
        host = host[: -len(".apps.dynatrace.com")] + ".live.dynatrace.com"

    normalized = f"{parsed.scheme or 'https'}://{host}".rstrip("/")
    return normalized, normalized != raw.rstrip("/")


def _get_env_or_default(name: str, default: str) -> str:
    value = os.environ.get(name)
    if value is None:
        return default
    stripped = value.strip()
    return stripped if stripped else default
