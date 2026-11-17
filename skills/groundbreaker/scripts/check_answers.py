#!/usr/bin/env python3
"""Validate a `--from` answers file. Read-only, stdlib only.

Usage: python check_answers.py answers.json
Exit 0 = valid, 1 = errors (nothing should be written).
"""
import json
import re
import sys

ENUMS = {
    "type": ["web-app", "marketing-site", "api-backend", "cli", "library", "mobile", "ai-llm-app", "other"],
    "team": ["solo", "team"],
    "ambition": ["prototype", "mvp", "production"],
    "sensitivity": ["none", "pii", "payments", "health-legal"],
    "auth": ["none", "simple", "roles", "sso"],
    "testing": ["smoke", "pyramid", "tdd"],
    "a11y": ["basic", "aa"],
}
SECRET = re.compile(r"sk-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY")


def check(data):
    errs = []
    if not isinstance(data, dict):
        return ["top level must be a JSON object"]
    for req in ("idea", "type"):
        if not data.get(req):
            errs.append(f"missing required key: {req}")
    for key, allowed in ENUMS.items():
        if key in data and data[key] is not None and data[key] not in allowed:
            errs.append(f"{key}: '{data[key]}' not allowed; use one of {', '.join(allowed)}")
    if "constraints" in data and not isinstance(data["constraints"], list):
        errs.append("constraints must be a list")
    if "other_agents" in data and not isinstance(data["other_agents"], bool):
        errs.append("other_agents must be true or false")
    ui = data.get("ui")
    if ui is not None:
        if not isinstance(ui, dict):
            errs.append("ui must be an object")
        elif ui.get("theme") not in (None, "light", "dark", "both"):
            errs.append(f"ui.theme: '{ui['theme']}' not allowed; use one of light, dark, both")
    if SECRET.search(json.dumps(data)):
        errs.append("looks like a secret/credential is in the answers; remove it (use .env.example instead)")
    return errs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check_answers.py answers.json")
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            problems = check(json.load(f))
    except (OSError, ValueError) as e:
        problems = [f"cannot read answers file: {e}"]
    for p in problems:
        print("ERROR", p)
    print(f"{len(problems)} error(s)")
    sys.exit(1 if problems else 0)
