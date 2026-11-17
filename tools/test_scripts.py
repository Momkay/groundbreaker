#!/usr/bin/env python3
"""Behavior tests for the skill's helper scripts. Stdlib only.

Usage: python tools/test_scripts.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "skills", "groundbreaker")
sys.path.insert(0, os.path.join(SK, "scripts"))
import check_answers  # noqa: E402


def run(script, *args):
    p = subprocess.run([sys.executable, os.path.join(SK, "scripts", script), *args], capture_output=True, text=True)
    return p.returncode, p.stdout


def make(tree):
    d = tempfile.mkdtemp()
    for path, body in tree.items():
        full = os.path.join(d, *path.split("/"))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(body if isinstance(body, str) else json.dumps(body))
    return d


class Detect(unittest.TestCase):
    def detect(self, tree):
        code, out = run("detect.py", make(tree))
        self.assertEqual(code, 0)
        return json.loads(out)

    def test_empty_is_greenfield(self):
        self.assertEqual(self.detect({"README.md": "x"})["mode"], "greenfield")

    def test_node_project(self):
        r = self.detect({
            "package.json": {"scripts": {"test": "vitest"}, "dependencies": {"next": "1", "react": "1"}, "devDependencies": {"vitest": "1", "typescript": "1"}},
            "pnpm-lock.yaml": "", ".github/workflows/ci.yml": "", "tests/a.test.ts": "",
            **{f"src/f{i}.ts": "" for i in range(8)}})
        self.assertEqual(r["mode"], "brownfield")
        self.assertEqual(r["package_manager"], "pnpm")
        self.assertTrue({"nextjs", "react", "vitest", "typescript"} <= set(r["stack_hints"]))
        self.assertTrue(r["ci"] and r["tests_present"] and r["has_ui_hint"])

    def test_python_project(self):
        r = self.detect({"pyproject.toml": 'dependencies = ["fastapi>=0.1", "pytest"]', "uv.lock": "", **{f"a{i}.py": "" for i in range(8)}})
        self.assertIn("fastapi", r["stack_hints"])
        self.assertEqual(r["package_manager"], "uv")

    def test_monorepo_and_skip_dirs(self):
        r = self.detect({"pnpm-workspace.yaml": "", "package.json": {}, **{f"node_modules/x/{i}.js": "" for i in range(20)}})
        self.assertIn("pnpm-workspace.yaml", r["monorepo"])
        self.assertEqual(r["source_files"], 0)  # node_modules ignored

    def test_bad_package_json_does_not_crash(self):
        r = self.detect({"package.json": "{not json"})
        self.assertTrue(r["warnings"])

    def test_existing_docs_seen(self):
        r = self.detect({"CLAUDE.md": "x", ".groundbreaker/state.json": "{}"})
        self.assertTrue(r["docs"]["CLAUDE.md"] and r["docs"][".groundbreaker/state.json"])


class Validate(unittest.TestCase):
    GOOD_SPEC = "# S\n## Features\nAcceptance:\n- x\n## Assumptions\nASSUMPTION: y\n"

    def v(self, tree):
        return run("validate.py", make(tree))

    def test_clean(self):
        code, out = self.v({"CLAUDE.md": "# P\n`docs/SPEC.md`\n", "docs/SPEC.md": self.GOOD_SPEC})
        self.assertEqual(code, 0, out)

    def test_missing_claude_md(self):
        self.assertEqual(self.v({"docs/SPEC.md": self.GOOD_SPEC})[0], 1)

    def test_placeholders_flagged_but_not_in_code_or_generics(self):
        code, out = self.v({"CLAUDE.md": "# <Project>\nTODO later\n"})
        self.assertEqual(code, 1)
        self.assertIn("placeholder", out)
        code, out = self.v({"CLAUDE.md": "# P\nUse `src/<name>/` and Array<Foo> freely.\n"})
        self.assertEqual(code, 0, out)

    def test_missing_referenced_doc(self):
        code, out = self.v({"CLAUDE.md": "# P\nsee docs/PLAN.md\n"})
        self.assertIn("missing file", out)

    def test_npm_script_must_exist(self):
        tree = {"CLAUDE.md": "# P\n- `pnpm test`\n- `pnpm run e2e`\n", "package.json": {"scripts": {"test": "x"}}}
        code, out = self.v(tree)
        self.assertEqual(code, 1)
        self.assertIn("`e2e`", out)
        self.assertNotIn("`test`", out)

    def test_spec_needs_acceptance(self):
        code, out = self.v({"CLAUDE.md": "# P\n", "docs/SPEC.md": "# S\njust prose\n"})
        self.assertIn("acceptance", out)

    def test_constraints_empty_cell(self):
        code, out = self.v({"CLAUDE.md": "# P\n", "CONSTRAINTS.md": "| a | b |\n|---|---|\n| x |  |\n"})
        self.assertEqual(code, 1)
        self.assertIn("empty table cell", out)

    def test_long_claude_md_warns(self):
        code, out = self.v({"CLAUDE.md": "# P\n" + "line\n" * 130})
        self.assertEqual(code, 0)
        self.assertIn("WARN", out)


class Answers(unittest.TestCase):
    OK = {"idea": "x", "type": "web-app", "auth": "simple", "ui": {"theme": "both"}}

    def test_valid(self):
        self.assertEqual(check_answers.check(self.OK), [])

    def test_bad_enum_lists_allowed(self):
        e = check_answers.check({**self.OK, "type": "spaceship"})
        self.assertTrue(e and "web-app" in e[0])

    def test_missing_required_and_wrong_types(self):
        e = check_answers.check({"constraints": "gdpr", "other_agents": "yes", "ui": []})
        self.assertGreaterEqual(len(e), 4)

    def test_secret_rejected(self):
        e = check_answers.check({**self.OK, "idea": "use key sk-abcdefghijklmnop1234"})
        self.assertTrue(any("secret" in x for x in e))

    def test_cli_exit_codes_and_garbage_file(self):
        good = make({"a.json": self.OK})
        self.assertEqual(run("check_answers.py", os.path.join(good, "a.json"))[0], 0)
        bad = make({"a.json": "{oops"})
        self.assertEqual(run("check_answers.py", os.path.join(bad, "a.json"))[0], 1)
        self.assertEqual(run("check_answers.py", os.path.join(bad, "nope.json"))[0], 1)

    def test_docs_list_every_enum_value(self):
        with open(os.path.join(SK, "references", "interview.md"), encoding="utf-8") as f:
            doc = f.read()
        for key, vals in check_answers.ENUMS.items():
            for v in vals:
                self.assertIn(v, doc, f"{key}={v} missing from interview.md allowed values")


if __name__ == "__main__":
    unittest.main(verbosity=1)
