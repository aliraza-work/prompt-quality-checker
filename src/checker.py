#!/usr/bin/env python3
"""Check prompt files for quality issues before LLM training review."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

REQUIRED_MARKERS = ("task:", "constraints:", "output format:")

def check_prompt(text: str) -> list[str]:
    issues = []
    lowered = text.lower()
    for marker in REQUIRED_MARKERS:
        if marker not in lowered:
            issues.append(f"missing_section:{marker.rstrip(':')}")
    if len(text.strip()) < 40:
        issues.append("too_short")
    if "ignore previous" in lowered and "follow instructions" in lowered:
        issues.append("conflicting_instructions")
    if re.search(r"\bTODO\b|\bTBD\b", text):
        issues.append("placeholder_text")
    return issues

def check_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for item in data:
        issues = check_prompt(item.get("prompt", ""))
        rows.append({"id": item.get("id"), "ok": not issues, "issues": issues})
    return {
        "total": len(rows),
        "passed": sum(1 for r in rows if r["ok"]),
        "failed": sum(1 for r in rows if not r["ok"]),
        "rows": rows,
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="samples/prompt_report.json")
    args = parser.parse_args()
    result = check_file(Path(args.input))
    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"passed={result['passed']} failed={result['failed']}")

if __name__ == "__main__":
    main()
