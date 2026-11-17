#!/usr/bin/env python3
"""Detect a project's stack and state. Read-only, stdlib only, prints JSON.

Usage: python detect.py [project_dir]
"""
import json
import os
import re
import sys

SKIP = {".git", "node_modules", ".venv", "venv", "dist", "build", "target", "__pycache__", ".next", ".cache", "vendor"}
SRC_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".kt", ".cs", ".rb", ".php", ".swift", ".c", ".cpp", ".svelte", ".vue", ".dart"}
LOCKS = {"package-lock.json": "npm", "pnpm-lock.yaml": "pnpm", "yarn.lock": "yarn", "bun.lockb": "bun", "bun.lock": "bun",
         "poetry.lock": "poetry", "uv.lock": "uv", "Pipfile.lock": "pipenv", "Cargo.lock": "cargo", "go.sum": "go", "Gemfile.lock": "bundler", "composer.lock": "composer"}
MANIFESTS = ["package.json", "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts", "Gemfile", "composer.json", "pubspec.yaml", "Package.swift"]
HINTS = {  # dependency name -> label
    "next": "nextjs", "react": "react", "vue": "vue", "svelte": "svelte", "@sveltejs/kit": "sveltekit", "astro": "astro", "@remix-run/react": "remix",
    "express": "express", "fastify": "fastify", "@nestjs/core": "nestjs", "hono": "hono", "tailwindcss": "tailwind", "typescript": "typescript",
    "vite": "vite", "vitest": "vitest", "jest": "jest", "@playwright/test": "playwright", "cypress": "cypress", "eslint": "eslint", "prettier": "prettier",
    "biome": "biome", "@biomejs/biome": "biome", "prisma": "prisma", "drizzle-orm": "drizzle", "expo": "expo", "react-native": "react-native",
    "django": "django", "fastapi": "fastapi", "flask": "flask", "pytest": "pytest", "ruff": "ruff", "mypy": "mypy", "sqlalchemy": "sqlalchemy",
    "anthropic": "anthropic-sdk", "@anthropic-ai/sdk": "anthropic-sdk", "openai": "openai-sdk",
}
DOCS = ["README.md", "CLAUDE.md", "AGENTS.md", "CONSTRAINTS.md", "KICKOFF.md", "docs/SPEC.md", "docs/ARCHITECTURE.md", "docs/DESIGN.md", "docs/PLAN.md",
        ".groundbreaker/state.json", ".groundbreaker/team.md", ".env.example"]


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def main(root):
    out = {"root": os.path.abspath(root)}
    names = set(os.listdir(root)) if os.path.isdir(root) else set()
    src = 0
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP and not d.startswith(".venv")]
        if dp[len(root):].count(os.sep) > 6:
            dns[:] = []
        src += sum(os.path.splitext(f)[1] in SRC_EXT for f in fns)
        if src > 500:
            break
    out["source_files"] = src
    out["mode"] = "greenfield" if src <= 5 else "brownfield"
    out["manifests"] = [m for m in MANIFESTS if m in names] + [n for n in names if n.endswith((".csproj", ".sln"))]
    out["package_manager"] = next((v for k, v in LOCKS.items() if k in names), None)
    hints, scripts = set(), {}
    pkg = read(os.path.join(root, "package.json"))
    if pkg:
        try:
            data = json.loads(pkg)
            scripts = data.get("scripts", {})
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            hints |= {HINTS[d] for d in deps if d in HINTS}
            if data.get("workspaces"):
                out.setdefault("monorepo", []).append("npm-workspaces")
        except ValueError:
            out["warnings"] = ["package.json is not valid JSON"]
    for f in ("pyproject.toml", "requirements.txt", "Pipfile"):
        txt = read(os.path.join(root, f)).lower()
        hints |= {label for dep, label in HINTS.items() if re.search(r"(?m)(^|[\s\"'\[,])" + re.escape(dep) + r"([\s\"'=<>~!\],;]|$)", txt) and dep.isalpha()}
    out["stack_hints"] = sorted(hints)
    out["scripts"] = scripts
    for m in ("pnpm-workspace.yaml", "turbo.json", "nx.json", "lerna.json"):
        if m in names:
            out.setdefault("monorepo", []).append(m)
    out["ci"] = [p for p in (".github/workflows", ".gitlab-ci.yml", ".circleci", "azure-pipelines.yml", "Jenkinsfile") if os.path.exists(os.path.join(root, p))]
    out["tests_present"] = any(n in names for n in ("tests", "test", "__tests__", "spec", "e2e", "cypress", "playwright.config.ts"))
    out["docs"] = {d: os.path.exists(os.path.join(root, d)) for d in DOCS}
    out["git"] = os.path.isdir(os.path.join(root, ".git"))
    out["graphify"] = os.path.isdir(os.path.join(root, "graphify-out"))
    out["has_ui_hint"] = bool(hints & {"nextjs", "react", "vue", "svelte", "sveltekit", "astro", "remix", "expo", "react-native"}) or "index.html" in names
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
