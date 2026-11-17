#!/usr/bin/env python3
"""Validate groundbreaker output. Read-only, stdlib only.

Usage: python validate.py [project_dir]
Exit 0 = clean (warnings allowed), 1 = errors found.
"""
import json
import os
import re
import sys

FILES = ["CLAUDE.md", "AGENTS.md", "KICKOFF.md", "CONSTRAINTS.md", "docs/SPEC.md", "docs/ARCHITECTURE.md", "docs/DESIGN.md", "docs/PLAN.md"]
# (?<!\w) so generics like Array<Foo> are not mistaken for placeholders
PLACEHOLDER = re.compile(r"\bTODO\b|\bTBD\b|\{\{|(?<!\w)<(?:Project|project|name|your[- ][\w -]+|[A-Z][A-Za-z ]{2,30})>")
RUN = re.compile(r"\b(?:npm|pnpm|yarn|bun) (?:run )?([\w:.-]+)")
BUILTIN = {"install", "i", "ci", "test", "start", "init", "add", "audit", "exec", "dlx", "create", "update", "publish", "pack", "link", "outdated", "build"}


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def check(root):
    errs, warns = [], []
    text = {f: read(os.path.join(root, f)) for f in FILES}
    text = {f: t for f, t in text.items() if t is not None}

    if "CLAUDE.md" not in text and "AGENTS.md" not in text:
        errs.append("CLAUDE.md (or AGENTS.md) missing")
    for f, t in text.items():
        for n, line in enumerate(t.splitlines(), 1):
            # inline code like `src/features/<name>/` is a legitimate path pattern
            if PLACEHOLDER.search(re.sub(r"`[^`]*`", "", line)):
                errs.append(f"{f}:{n} unfilled placeholder: {line.strip()[:70]}")
    c = text.get("CLAUDE.md", "")
    if c.count("\n") > 120:
        warns.append(f"CLAUDE.md is {c.count(chr(10))} lines; keep it under ~100 (move detail into docs/)")

    # referenced docs exist
    for f in ("CLAUDE.md", "AGENTS.md", "KICKOFF.md"):
        for ref in set(re.findall(r"`?((?:docs/)?[\w./-]+\.md)`?", text.get(f, ""))):
            if ref.startswith("http") or "/" in ref and not ref.startswith("docs/"):
                continue
            if not os.path.exists(os.path.join(root, ref)):
                errs.append(f"{f} references missing file: {ref}")

    # npm-style commands exist in package.json
    pkg = read(os.path.join(root, "package.json"))
    if pkg:
        try:
            scripts = json.loads(pkg).get("scripts", {})
            for cmd in set(RUN.findall(c)):
                if cmd not in BUILTIN and cmd not in scripts:
                    errs.append(f"CLAUDE.md command `{cmd}` not in package.json scripts")
        except ValueError:
            warns.append("package.json is not valid JSON")

    spec = text.get("docs/SPEC.md")
    if spec is not None:
        if not re.search(r"acceptance", spec, re.I):
            errs.append("docs/SPEC.md has no acceptance criteria")
        if not re.search(r"assumption|open questions", spec, re.I):
            warns.append("docs/SPEC.md lists no assumptions/open questions (rarely true)")
    cons = text.get("CONSTRAINTS.md")
    if cons is not None:
        for line in cons.splitlines():
            if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", line):
                cells = [x.strip() for x in line.strip("|").split("|")]
                if any(x == "" for x in cells):
                    errs.append(f"CONSTRAINTS.md empty table cell: {line[:70]}")
    if "docs/PLAN.md" in text and not re.search(r"slice\s*1", text["docs/PLAN.md"], re.I):
        warns.append("docs/PLAN.md has no 'Slice 1'")
    return errs, warns, sorted(text)


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    errors, warnings, seen = check(root)
    print(f"checked: {', '.join(seen) or 'nothing found'}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)
