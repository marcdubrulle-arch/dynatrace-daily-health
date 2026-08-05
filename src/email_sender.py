from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str) -> None:
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_report(self, email_from: str, email_to: list[str], subject: str, html_content: str, md_path: Path | None = None) -> bool:
        """Send email report with HTML content and optional attachment."""
        if not email_to or not email_from or not self.smtp_server:
            print("Warning: Email configuration incomplete, skipping email send")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = email_from
            msg["To"] = ", ".join(email_to)

            # Attach HTML content
            html_part = MIMEText(html_content, "html", "utf-8")
            msg.attach(html_part)

            # Attach markdown report if provided
            if md_path and md_path.exists():
                with open(md_path, "r", encoding="utf-8") as f:
                    md_content = f.read()
                md_part = MIMEText(md_content, "plain", "utf-8")
                md_part.add_header("Content-Disposition", "attachment", filename=md_path.name)
                msg.attach(md_part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(email_from, email_to, msg.as_string())

            print(f"Email sent successfully to {', '.join(email_to)}")
            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False


def build_email_html(summary: dict, open_problems: list, recurring_problems: list, availability: dict, synthetic_tests: list) -> str:
    """Build HTML email content from analysis results."""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #1e40af; border-bottom: 3px solid #1e40af; padding-bottom: 10px; }}
            h2 {{ color: #3b82f6; margin-top: 20px; }}
            .summary {{ background-color: #eff6ff; padding: 15px; border-radius: 5px; margin: 10px 0; }}
            .summary-item {{ display: inline-block; margin-right: 20px; }}
            .summary-value {{ font-weight: bold; font-size: 18px; color: #1e40af; }}
            .problems {{ margin: 15px 0; }}
            .problem-item {{ padding: 10px; background-color: #fef3c7; border-left: 4px solid #f59e0b; margin: 5px 0; border-radius: 3px; }}
            .problem-severity-critical {{ border-left-color: #dc2626; background-color: #fee2e2; }}
            .problem-severity-high {{ border-left-color: #f59e0b; background-color: #fef3c7; }}
            .availability {{ margin: 15px 0; }}
            .availability-item {{ padding: 8px; background-color: #f0fdf4; border-left: 4px solid #22c55e; margin: 5px 0; border-radius: 3px; }}
            .availability-item.poor {{ background-color: #fef2f2; border-left-color: #dc2626; }}
            .synthetic {{ margin: 15px 0; }}
            .synthetic-item {{ padding: 8px; background-color: #f3f4f6; border-left: 4px solid #6b7280; margin: 5px 0; border-radius: 3px; }}
            .synthetic-item.failed {{ background-color: #fee2e2; border-left-color: #dc2626; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; border-top: 1px solid #e5e7eb; padding-top: 10px; }}
            .no-issues {{ color: #059669; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #e5e7eb; }}
            th {{ background-color: #f3f4f6; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Dynatrace Daily Health Report</h1>
            
            <div class="summary">
                <div class="summary-item">Problems (24h): <span class="summary-value">{summary.get('problems_last_24h', 0)}</span></div>
                <div class="summary-item">Open Problems: <span class="summary-value">{summary.get('open_problems', 0)}</span></div>
                <div class="summary-item">Applications: <span class="summary-value">{summary.get('applications', 0)}</span></div>
                <div class="summary-item">Recurring Issues: <span class="summary-value">{summary.get('recurring_signatures', 0)}</span></div>
            </div>
            
            <h2>🔴 Open Problems</h2>
            <div class="problems">
    """

    if open_problems:
        for problem in open_problems:
            severity_class = ""
            if problem.get("severity", "").upper() == "CRITICAL":
                severity_class = " problem-severity-critical"
            elif problem.get("severity", "").upper() == "HIGH":
                severity_class = " problem-severity-high"
            
            html += f"""
            <div class="problem-item{severity_class}">
                <strong>{problem.get('display_id', 'N/A')}</strong> | {problem.get('severity', 'N/A')} | {problem.get('title', 'N/A')}
                <br><small>Affected entities: {problem.get('affected_entity_count', 0)}</small>
            </div>
            """
    else:
        html += '<div class="no-issues">✓ No open problems</div>'

    html += """
            </div>
            
            <h2>🔄 Recurring Problems (Last 7 days)</h2>
            <div class="problems">
    """

    if recurring_problems:
        for problem in recurring_problems:
            html += f"""
            <div class="problem-item">
                {problem.get('signature', 'N/A')} <strong>({problem.get('count', 0)} occurrences)</strong>
            </div>
            """
    else:
        html += '<div class="no-issues">✓ No recurring problems</div>'

    html += """
            </div>
            
            <h2>📈 Application Availability (Last 24h)</h2>
            <div class="availability">
    """

    if availability:
        for app, value in sorted(availability.items()):
            css_class = "poor" if value < 95 else ""
            html += f'<div class="availability-item {css_class}">{app}: <strong>{value:.2f}%</strong></div>'
    else:
        html += '<div class="no-issues">✓ All applications available</div>'

    html += """
            </div>
            
            <h2>🧪 Synthetic Tests</h2>
            <div class="synthetic">
    """

    if synthetic_tests:
        for test in synthetic_tests:
            css_class = "failed" if test.get("status") != "enabled" or test.get("availability", 0) < 95 else ""
            html += f"""
            <div class="synthetic-item {css_class}">
                {test.get('name', 'N/A')} - Status: {test.get('status', 'N/A')} | Availability: <strong>{test.get('availability', 0):.2f}%</strong>
            </div>
            """
    else:
        html += '<div class="no-issues">✓ No synthetic tests configured</div>'

    html += """
            </div>
            
            <div class="footer">
                <p>Generated by Dynatrace Daily Health Check</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html
