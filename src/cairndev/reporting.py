from __future__ import annotations

import json
from dataclasses import asdict

from .models import CheckReport


def report_to_dict(report: CheckReport) -> dict:
    return {
        "root": str(report.root),
        "passed": report.passed,
        "error_count": report.error_count,
        "warning_count": report.warning_count,
        "findings": [asdict(item) for item in report.findings],
    }


def report_to_json(report: CheckReport) -> str:
    return json.dumps(report_to_dict(report), indent=2, sort_keys=True)


def report_to_text(report: CheckReport) -> str:
    lines = [
        f"CairnDev report for {report.root}",
        f"Status: {'PASS' if report.passed else 'FAIL'}",
        f"Errors: {report.error_count}  Warnings: {report.warning_count}",
        "",
    ]
    if not report.findings:
        lines.append("No findings.")
        return "\n".join(lines)
    for finding in report.findings:
        location = finding.path or "<project>"
        if finding.line:
            location += f":{finding.line}"
        lines.append(f"[{finding.severity.upper()}] {finding.code} {location}")
        lines.append(f"  {finding.message}")
        if finding.suggestion:
            lines.append(f"  Suggestion: {finding.suggestion}")
    return "\n".join(lines)
