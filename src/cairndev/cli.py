from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .checks import run_checks
from .init_project import init_project
from .reporting import report_to_json, report_to_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cairndev", description="CairnDev quality checks")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Run design-quality checks")
    check.add_argument("path", nargs="?", default=".")
    check.add_argument("--json", action="store_true", dest="as_json")

    summarize = sub.add_parser("summarize", help="Summarize project quality state")
    summarize.add_argument("path", nargs="?", default=".")

    init = sub.add_parser("init", help="Initialize CairnDev files in a repo")
    init.add_argument("--target", default=".")
    init.add_argument("--force", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "check":
        report = run_checks(Path(args.path))
        print(report_to_json(report) if args.as_json else report_to_text(report))
        return 1 if report.error_count else 0
    if args.command == "summarize":
        report = run_checks(Path(args.path))
        print(report_to_text(report))
        return 0
    if args.command == "init":
        created = init_project(Path(args.target), force=args.force)
        if created:
            print("Created:")
            for path in created:
                print(f"- {path}")
        else:
            print("No files created; existing files preserved. Use --force to overwrite.")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
