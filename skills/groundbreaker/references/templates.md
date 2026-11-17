# groundbreaker templates

Contents: SPEC · KICKOFF · ARCHITECTURE · DESIGN · CONSTRAINTS · CLAUDE.md · PLAN · Manual validation

Fill with real content from the interview. Omit any section that would be empty or generic. No `<angle-bracket>` placeholder, `TODO` or `TBD` may survive into a generated file (`scripts/validate.py` fails on them).

## docs/SPEC.md
```
# <Project> - Spec
## Objective      one paragraph: problem, who has it, what success looks like (measurable)
## Users          primary / secondary, one line each
## Scope          MVP features | Later | Non-goals (explicit)
## Features       per feature: user story + acceptance criteria (Given/When/Then or checklist)
## Data & integrations   entities, external services, auth model
## Threat model   assets, entry points, top threats -> mitigations (as acceptance criteria)
## Assumptions    ASSUMPTION: ... (each confirmable)
## Open questions  ranked by risk
```

## KICKOFF.md (the master prompt)
```
You are building <Project>: <one-line>. Read, in order: CLAUDE.md, docs/SPEC.md, docs/ARCHITECTURE.md, docs/DESIGN.md, CONSTRAINTS.md, docs/PLAN.md.

Context: <who it is for, why it exists>
Stack (decided): <list>. Do not substitute without asking.
Quality bar: <3-5 bullet highlights from CONSTRAINTS.md>
Skills to use: <routing table summary>
Working method: one vertical slice at a time from docs/PLAN.md; write the failing test first; run <test/lint/typecheck commands> before declaring done; verify UI in a real browser when applicable.
Stop and ask when: <irreversible actions, new dependency, spec ambiguity, constraint would be weakened>
Start now with slice 1: <name> - done means: <acceptance criteria>.
```

## docs/ARCHITECTURE.md
```
# Architecture
## Overview      diagram (mermaid) + 5-line description
## Components    name - responsibility - depends on
## Data model    entities + key relations
## Key decisions ADR-style: Decision / Context / Choice / Alternatives rejected / Consequences
## Layout        directory tree with one-line purposes
## Cross-cutting error handling, logging, config/secrets, auth, observability
```

## docs/DESIGN.md (UI projects)
```
# Design
## Direction     vibe in 2 sentences + 2-3 references and what to take from each
## Tokens        color (semantic, light+dark, contrast-checked), type scale + families, spacing, radius, shadow, motion
## Layout        grid, breakpoints, density
## Components    list + states (default/hover/focus/disabled/loading/empty/error)
## Accessibility target level, focus order, keyboard, contrast, reduced motion
## Anti-patterns what this project must NOT look like (generic templated UI, etc.)
```
Delegate to `taste-skill:design-taste-frontend` (marketing/public pages) or `agent-skills:frontend-ui-engineering` (app UIs) when installed.

## CONSTRAINTS.md - default thresholds (user may override; ask only if they care)
| Dimension | Default | Enforced by |
|---|---|---|
| Types/lint | strict, zero warnings | typecheck + lint in CI |
| Tests | pyramid; new logic needs a test; coverage >= 80% lines on core logic | test command in CI |
| Security | no secrets in repo, input validated at boundaries, authz on every endpoint, deps audited, no high/critical vulns | secret scan + audit in CI |
| Performance (web) | LCP < 2.5s, CLS < 0.1, INP < 200ms, JS budget stated | Lighthouse CI / `agent-skills:webperf` |
| Accessibility | WCAG 2.2 AA | axe in tests + manual keyboard pass |
| Process | no skipped/deleted tests, no new suppressions (`@ts-ignore`, `eslint-disable`) without a written reason | review + `agent-skills:constraint-driven-development` |

## CLAUDE.md (<100 lines)
```
# <Project>
<one-line description>
## Commands     install / dev / build / test / lint / typecheck. Brownfield: run them to verify. Greenfield: they don't exist yet, so say "created in slice 1" and make slice 1 create them
## Structure    top-level dirs, one line each
## Conventions  naming, error handling, imports, commit style (only non-obvious ones)
## Hard rules   never do X (secrets, destructive ops, weakening constraints)
## Skill routing
| When | Use |
|---|---|
## Definition of done   tests pass, lint/types clean, acceptance criteria met, docs updated
## Docs         pointers to SPEC, ARCHITECTURE, DESIGN, CONSTRAINTS, PLAN
```

## docs/PLAN.md
```
# Plan
Slice N: <name> | depends on: <slices> | size: S/M/L
  Delivers: <user-visible outcome>
  Tasks: [ ] ...
  Acceptance: <testable>
  Risks: <what could derail it>
```
Rules: slice 1 is the thinnest end-to-end path (UI -> logic -> storage -> deploy if feasible); no slice larger than ~1 day; riskiest unknown goes early.

## Manual validation (when Python is unavailable)
- CLAUDE.md exists and is under ~100 lines.
- Grep generated files for `TODO`, `TBD`, `{{`, and `<Word>` placeholders: none left.
- Every `docs/*.md` path mentioned in CLAUDE.md/KICKOFF.md exists.
- Every `npm|pnpm|yarn run X` in CLAUDE.md exists in `package.json` scripts (same idea for other ecosystems).
- SPEC has acceptance criteria and an assumptions/open-questions section.
- CONSTRAINTS has no empty "Enforced by" cell.
