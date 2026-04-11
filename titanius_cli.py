from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflows import registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="titanius")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List available workflows")
    list_parser.set_defaults(command="list")

    run_parser = subparsers.add_parser("run", help="Run a workflow")
    run_parser.add_argument("workflow", help="Workflow name")
    run_parser.add_argument("--input", required=True, help="Path to JSON or CSV input")
    run_parser.add_argument("--mode", choices=["dry", "report", "apply"], default="report")
    run_parser.add_argument("--output-json", help="Optional path for JSON output")
    run_parser.add_argument("--output-md", help="Optional path for markdown report output")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        print(json.dumps({"workflows": registry.list_names()}, indent=2))
        return 0

    runner = registry.get(args.workflow)
    result = runner(input_path=args.input, mode=args.mode)

    if args.output_json:
        Path(args.output_json).write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.output_md:
        Path(args.output_md).write_text(result.get("markdown_report", ""), encoding="utf-8")

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
