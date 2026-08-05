from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .analyzer import AnalysisResult


def build_markdown(result: AnalysisResult, generated_at: datetime) -> str:
    lines = [
        "# Dynatrace Daily Health",
        "",
        f"_Generated at {generated_at.astimezone(timezone.utc).isoformat()}_",
        "",
        "## Summary",
    ]
    for key, value in result.summary.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Open problems"])
    if result.open_problems:
        for item in result.open_problems:
            lines.append(f"- {item['display_id']} | {item['severity']} | {item['title']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Recurring problems"])
    if result.recurring_problems:
        for item in result.recurring_problems:
            lines.append(f"- {item['signature']} ({item['count']} occurrences)")
    else:
        lines.append("- none")
    lines.extend(["", "## Availability"])
    if result.availability:
        for app, value in sorted(result.availability.items()):
            lines.append(f"- {app}: {value:.2f}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def write_outputs(result: AnalysisResult, output_dir: str, generated_at: datetime) -> tuple[Path, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    day = generated_at.date().isoformat()
    md_path = out / f"report_{day}.md"
    json_path = out / f"report_{day}.json"
    md_path.write_text(build_markdown(result, generated_at), encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "generated_at": generated_at.astimezone(timezone.utc).isoformat(),
                "summary": result.summary,
                "open_problems": result.open_problems,
                "recurring_problems": result.recurring_problems,
                "availability": result.availability,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return md_path, json_path


