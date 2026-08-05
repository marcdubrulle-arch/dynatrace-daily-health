from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import re
from typing import Iterable

from .dynatrace_client import DynatraceProblem


@dataclass
class AnalysisResult:
    open_problems: list[dict]
    recurring_problems: list[dict]
    availability: dict[str, float]
    summary: dict[str, int]


def problem_signature(problem: DynatraceProblem) -> str:
    title = problem.title.lower()
    title = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "<date>", title)
    title = re.sub(r"\b\d+\b", "<n>", title)
    return title


def analyze(problems_24h: Iterable[DynatraceProblem], problems_7d: Iterable[DynatraceProblem], availability: dict[str, float]) -> AnalysisResult:
    p24 = list(problems_24h)
    p7 = list(problems_7d)

    open_problems = [asdict_problem(p) for p in p24 if p.status.upper() == "OPEN"]
    signatures = Counter(problem_signature(p) for p in p7)

    recurring = []
    for signature, count in signatures.items():
        if count >= 2:
            recurring.append({"signature": signature, "count": count})
    recurring.sort(key=lambda item: item["count"], reverse=True)

    summary = {
        "problems_last_24h": len(p24),
        "open_problems": len(open_problems),
        "recurring_signatures": len(recurring),
        "applications": len(availability),
    }
    return AnalysisResult(
        open_problems=open_problems,
        recurring_problems=recurring[:10],
        availability=availability,
        summary=summary,
    )


def asdict_problem(problem: DynatraceProblem) -> dict:
    return {
        "id": problem.id,
        "display_id": problem.display_id,
        "title": problem.title,
        "status": problem.status,
        "severity": problem.severity,
        "impact_level": problem.impact_level,
        "affected_entity_count": problem.affected_entity_count,
        "start_time": problem.start_time,
        "end_time": problem.end_time,
    }


