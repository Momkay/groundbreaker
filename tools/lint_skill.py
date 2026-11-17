#!/usr/bin/env python3
"""Lint every skill under skills/ and self-test the scripts. Stdlib only.

Usage: python tools/lint_skill.py        (run from repo root; used by CI)
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []


def err(msg):
    errors.append(msg)
    print("ERROR", msg)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z][\w-]*:", line):
            k, _, v = line.partition(":")
            fm[k] = v.strip()
    return fm


def lint_skill(d):
    name = os.path.basename(d)
    path = os.path.join(d, "SKILL.md")
    if not os.path.exists(path):
        return err(f"{name}: SKILL.md missing")
    text = open(path, encoding="utf-8").read()
    fm = frontmatter(text)
    if fm is None:
        return err(f"{name}: no YAML frontmatter")
    if fm.get("name") != name:
        err(f"{name}: frontmatter name '{fm.get('name')}' must equal folder name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm.get("name", "")) or len(fm.get("name", "")) > 64:
        err(f"{name}: name must be lowercase-hyphen, <= 64 chars")
    desc = fm.get("description", "")
    if not desc or len(desc) > 1024:
        err(f"{name}: description missing or > 1024 chars ({len(desc)})")
    if re.search(r"\b(I|you|your)\b", desc.split("Use when")[0]):
        err(f"{name}: description should be third person")
    if "Use when" not in desc:
        err(f"{name}: description should say when to use the skill")
    lines = text.count("\n")
    if lines > 500:
        err(f"{name}: SKILL.md is {lines} lines (max 500); move detail to references/")
    for ref in set(re.findall(r"`((?:references|scripts|evals)/[\w./-]+)`", text)):
        if not os.path.exists(os.path.join(d, ref)):
            err(f"{name}: SKILL.md references missing file {ref}")
    for f in os.listdir(os.path.join(d, "references")) if os.path.isdir(os.path.join(d, "references")) else []:
        body = open(os.path.join(d, "references", f), encoding="utf-8").read()
        if body.count("\n") > 100 and "Contents" not in body[:400]:
            err(f"{name}: references/{f} > 100 lines needs a Contents line at the top")
        if f"references/{f}" not in text:
            err(f"{name}: references/{f} is not linked from SKILL.md (orphan)")
    if "\\" in "".join(re.findall(r"`(?:references|scripts)/[^`]*`", text)):
        err(f"{name}: use forward slashes in paths")
    ev = os.path.join(d, "evals")
    for f in os.listdir(ev) if os.path.isdir(ev) else []:
        try:
            json.load(open(os.path.join(ev, f), encoding="utf-8"))
        except ValueError as e:
            err(f"{name}: evals/{f} invalid JSON: {e}")


def selftest(d):
    v = os.path.join(d, "scripts", "validate.py")
    good = subprocess.run([sys.executable, v, os.path.join(ROOT, "examples", "pawprint")], capture_output=True, text=True)
    if good.returncode != 0:
        err("validate.py rejects examples/pawprint:\n" + good.stdout)
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "docs"))
        open(os.path.join(t, "CLAUDE.md"), "w").write("# <Project>\nTODO\nSee docs/NOPE.md\n")
        open(os.path.join(t, "docs", "SPEC.md"), "w").write("# Spec\nno criteria here\n")
        bad = subprocess.run([sys.executable, v, t], capture_output=True, text=True)
        for needle in ("placeholder", "missing file", "acceptance"):
            if needle not in bad.stdout:
                err(f"validate.py failed to flag '{needle}' in a broken project")
    det = subprocess.run([sys.executable, os.path.join(d, "scripts", "detect.py"), os.path.join(ROOT, "examples", "pawprint")], capture_output=True, text=True)
    try:
        assert json.loads(det.stdout)["manifests"] == ["package.json"]
    except Exception as e:
        err(f"detect.py output wrong: {e} {det.stderr[:200]}")


skills = os.path.join(ROOT, "skills")
for s in sorted(os.listdir(skills)):
    lint_skill(os.path.join(skills, s))
selftest(os.path.join(skills, "groundbreaker"))
print(f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
