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
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=60)
        response.raise_for_status()
        return response.json()

    def fetch_problems(self, start: datetime, end: datetime, selector: str = "") -> list[DynatraceProblem]:
        params: dict[str, Any] = {
            "from": start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "to": end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "pageSize": 200,
        }
        if selector:
            params["problemSelector"] = selector
        data = self._get("/api/v2/problems", params=params)
        return [self._parse_problem(item) for item in data.get("problems", [])]

    def fetch_application_availability(self, metric_selector: str, start: datetime, end: datetime) -> dict[str, float]:
        params = {
            "metricSelector": metric_selector,
            "from": start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "to": end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        data = self._get("/api/v2/metrics/query", params=params)
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


