from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import requests


@dataclass
class DynatraceProblem:
    id: str
    display_id: str
    title: str
    status: str
    severity: str
    impact_level: str | None
    affected_entity_count: int
    start_time: str | None
    end_time: str | None


@dataclass
class SyntheticTest:
    id: str
    name: str
    status: str
    availability: float
    last_run: str | None


class DynatraceClient:
    def __init__(self, base_url: str, api_token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Api-Token {api_token}",
                "Accept": "application/json",
            }
        )

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}{path}", params=params, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else "unknown"
            print(f"HTTP ERROR: {status_code} on {path}")
            if e.response is not None and e.response.request is not None:
                print(f"Request URL: {e.response.request.url}")
                print(f"Response text: {e.response.text[:500]}")
            raise
        except Exception as e:
            print(f"API ERROR: {e}")
            raise

    def fetch_problems(self, start: datetime, end: datetime, selector: str = "") -> list[DynatraceProblem]:
        params: dict[str, Any] = {
            "from": _to_dt_api_time(start),
            "to": _to_dt_api_time(end),
            "pageSize": 200,
        }
        if selector:
            params["problemSelector"] = selector
        try:
            data = self._get("/api/v2/problems", params=params)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 400:
                fallback_params: dict[str, Any] = {
                    "from": int(start.timestamp() * 1000),
                    "to": int(end.timestamp() * 1000),
                    "pageSize": 200,
                }
                if selector:
                    fallback_params["problemSelector"] = selector
                print("Retrying /api/v2/problems with epoch millisecond timestamps")
                data = self._get("/api/v2/problems", params=fallback_params)
            else:
                raise
        return [self._parse_problem(item) for item in data.get("problems", [])]

    def fetch_application_availability(self, metric_selector: str, start: datetime, end: datetime) -> dict[str, float]:
        params = {
            "metricSelector": metric_selector,
            "from": _to_dt_api_time(start),
            "to": _to_dt_api_time(end),
        }
        try:
            data = self._get("/api/v2/metrics/query", params=params)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code in (400, 404):
                print(
                    "Warning: availability metrics query failed; continuing without availability data"
                )
                return {}
            raise
        availability: dict[str, float] = {}
        for result in data.get("result", []):
            for series in result.get("data", []):
                dims = series.get("dimensions", [])
                key = dims[0] if dims else "unknown"
                values = series.get("values", [])
                value = next((v for v in reversed(values) if v is not None), None)
                if value is not None:
                    availability[key] = float(value)
        return availability

    def fetch_synthetic_tests(self, start: datetime, end: datetime) -> list[SyntheticTest]:
        """Fetch synthetic test results for the given time range."""
        params = {
            "from": _to_dt_api_time(start),
            "to": _to_dt_api_time(end),
            "pageSize": 200,
        }
        try:
            data = self._get("/api/v2/synthetics/monitors", params=params)
            tests = []
            for item in data.get("monitors", []):
                test = self._parse_synthetic_test(item, start, end)
                if test:
                    tests.append(test)
            return tests
        except Exception as e:
            print(f"Warning: Failed to fetch synthetic tests: {e}")
            return []

    @staticmethod
    def _parse_problem(item: dict[str, Any]) -> DynatraceProblem:
        return DynatraceProblem(
            id=str(item.get("problemId", "")),
            display_id=str(item.get("displayId", "")),
            title=str(item.get("title", "")),
            status=str(item.get("status", "")),
            severity=str(item.get("severityLevel", "")),
            impact_level=item.get("impactLevel"),
            affected_entity_count=int(item.get("affectedEntityCount", 0) or 0),
            start_time=item.get("startTime"),
            end_time=item.get("endTime"),
        )

    @staticmethod
    def _parse_synthetic_test(item: dict[str, Any], start: datetime, end: datetime) -> SyntheticTest | None:
        monitor_id = item.get("entityId")
        if not monitor_id:
            return None
        
        return SyntheticTest(
            id=monitor_id,
            name=str(item.get("displayName", "")),
            status=str(item.get("enabled", True)) == "True" and "enabled" or "disabled",
            availability=float(item.get("availability", 0) or 0),
            last_run=item.get("lastRun"),
        )


def _to_dt_api_time(dt: datetime) -> str:
    # Dynatrace API accepts RFC3339; using second precision avoids tenant-specific
    # parsing issues with microseconds.
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
