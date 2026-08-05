from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import re
from typing import Iterable

from .dynatrace_client import DynatraceProblem, SyntheticTest


@dataclass
class AnalysisResult:
    open_problems: list[dict]
    recurring_problems: list[dict]
    availability: dict[str, float]
    synthetic_tests: list[dict]
    summary: dict[str, int]


def problem_signature(problem: DynatraceProblem) -> str:
    title = problem.title.lower()
    title = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "<date>", title)
    title = re.sub(r"\b\d+\b", "<n>", title)
    return title


def analyze(
    problems_24h: Iterable[DynatraceProblem],
    problems_7d: Iterable[DynatraceProblem],
    availability: dict[str, float],
    synthetic_tests: list[SyntheticTest] | None = None,
) -> AnalysisResult:
    p24 = list(problems_24h)
    p7 = list(problems_7d)
    synthetic_tests = synthetic_tests or []

    open_problems = [asdict_problem(p) for p in p24 if p.status.upper() == "OPEN"]
    signatures = Counter(problem_signature(p) for p in p7)

    recurring = []
    for signature, count in signatures.items():
        if count >= 2:
            recurring.append({"signature": signature, "count": count})
    recurring.sort(key=lambda item: item["count"], reverse=True)

    synthetic_dicts = [asdict_synthetic(s) for s in synthetic_tests]

    summary = {
        "problems_last_24h": len(p24),
        "open_problems": len(open_problems),
        "recurring_signatures": len(recurring),
        "applications": len(availability),
        "synthetic_tests": len(synthetic_dicts),
    }
    return AnalysisResult(
        open_problems=open_problems,
        recurring_problems=recurring[:10],
        availability=availability,
        synthetic_tests=synthetic_dicts,
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


def asdict_synthetic(test: SyntheticTest) -> dict:
    return {
        "id": test.id,
        "name": test.name,
        "status": test.status,
        "availability": test.availability,
        "last_run": test.last_run,
    }

