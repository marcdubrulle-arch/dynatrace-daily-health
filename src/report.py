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
    
    lines.extend(["", "## Synthetic Tests"])
    if result.synthetic_tests:
        for test in result.synthetic_tests:
            lines.append(f"- {test['name']} | {test['status']} | Availability: {test['availability']:.2f}%")
    else:
        lines.append("- none")
    
    lines.append("")
    return "\n".join(lines)


def build_html(result: AnalysisResult, generated_at: datetime) -> str:
    generated = generated_at.astimezone(timezone.utc).isoformat()
    summary_rows = "".join(
        f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in result.summary.items()
    )

    if result.open_problems:
        open_rows = "".join(
            f"<tr><td>{item['display_id']}</td><td>{item['severity']}</td><td>{item['title']}</td></tr>"
            for item in result.open_problems
        )
    else:
        open_rows = '<tr><td colspan="3">none</td></tr>'

    if result.recurring_problems:
        recurring_rows = "".join(
            f"<tr><td>{item['signature']}</td><td>{item['count']}</td></tr>"
            for item in result.recurring_problems
        )
    else:
        recurring_rows = '<tr><td colspan="2">none</td></tr>'

    if result.availability:
        availability_rows = "".join(
            f"<tr><td>{app}</td><td>{value:.2f}%</td></tr>"
            for app, value in sorted(result.availability.items())
        )
    else:
        availability_rows = '<tr><td colspan="2">none</td></tr>'

    if result.synthetic_tests:
        synthetic_rows = "".join(
            f"<tr><td>{test['name']}</td><td>{test['status']}</td><td>{test['availability']:.2f}%</td></tr>"
            for test in result.synthetic_tests
        )
    else:
        synthetic_rows = '<tr><td colspan="3">none</td></tr>'

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dynatrace Daily Health</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #111827; }}
    h1 {{ margin-bottom: 0; }}
    .muted {{ color: #6b7280; margin-top: 6px; }}
    table {{ border-collapse: collapse; width: 100%; margin: 12px 0 24px; }}
    th, td {{ border: 1px solid #e5e7eb; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #f3f4f6; }}
  </style>
</head>
<body>
  <h1>Dynatrace Daily Health</h1>
  <p class="muted">Generated at {generated}</p>

  <h2>Summary</h2>
  <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{summary_rows}</tbody></table>

  <h2>Open problems</h2>
  <table><thead><tr><th>ID</th><th>Severity</th><th>Title</th></tr></thead><tbody>{open_rows}</tbody></table>

  <h2>Recurring problems</h2>
  <table><thead><tr><th>Signature</th><th>Occurrences</th></tr></thead><tbody>{recurring_rows}</tbody></table>

  <h2>Availability</h2>
  <table><thead><tr><th>Application / Monitor</th><th>Availability</th></tr></thead><tbody>{availability_rows}</tbody></table>

  <h2>Synthetic tests</h2>
  <table><thead><tr><th>Name</th><th>Status</th><th>Availability</th></tr></thead><tbody>{synthetic_rows}</tbody></table>
</body>
</html>
"""


def write_outputs(result: AnalysisResult, output_dir: str, generated_at: datetime) -> tuple[Path, Path, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    day = generated_at.date().isoformat()
    md_path = out / f"report_{day}.md"
    json_path = out / f"report_{day}.json"
    html_path = out / f"report_{day}.html"
    md_path.write_text(build_markdown(result, generated_at), encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "generated_at": generated_at.astimezone(timezone.utc).isoformat(),
                "summary": result.summary,
                "open_problems": result.open_problems,
                "recurring_problems": result.recurring_problems,
                "availability": result.availability,
                "synthetic_tests": result.synthetic_tests,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    html_path.write_text(build_html(result, generated_at), encoding="utf-8")
    return md_path, json_path, html_path
