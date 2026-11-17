# Project profiles

Contents: how to use · web-app · marketing-site · api-backend · cli · library · mobile · ai-llm-app · universal baseline

## How to use
Pick the closest profile (blend two if needed). Everything here is a **starting default**, not a verdict: verify current versions and setup against official docs before writing them into any file, and prefer what the repo already uses. Defaults name ecosystems, not versions.

## Universal baseline (every profile)
- Secrets only via env/secret manager; commit `.env.example`, never `.env`.
- Validate all input at trust boundaries; authorize on the server for every endpoint/action.
- Pin dependencies via lockfile; audit in CI; no high/critical known vulns at merge.
- One command each for install, dev, test, lint, typecheck, build - documented in CLAUDE.md.
- CI runs the same commands as local; merges blocked on red.
- Definition of done = acceptance criteria met + tests green + lint/types clean + docs touched.

## web-app (SaaS, dashboard, internal tool)
- Defaults: TypeScript end to end; full-stack framework (Next.js / SvelteKit / Remix class) or SPA + API; Postgres; managed auth unless auth is the product.
- Shape: feature-folder modules, thin route handlers, domain logic in plain functions, data access in one layer.
- Tests: unit for domain logic, integration for API + DB (real DB in CI), 3-5 end-to-end happy paths, axe on key pages.
- Threats: broken access control (IDOR), XSS, CSRF, session fixation, mass assignment, tenant leakage, secrets in client bundle, SSRF via URL inputs.
- Targets: LCP < 2.5s, CLS < 0.1, INP < 200ms; JS budget stated; WCAG 2.2 AA.
- Pitfalls: building auth/billing by hand, no seed data, no loading/empty/error states, designing only the happy path.

## marketing-site (landing page, portfolio, docs)
- Defaults: static-first (Astro / Next static / plain HTML+CSS); CMS only if non-devs edit content.
- Tests: link check, Lighthouse CI, visual check at 3 breakpoints.
- Threats: third-party script supply chain, form spam, exposed keys. Strong CSP.
- Focus: design direction matters most - use `taste-skill:design-taste-frontend`; real photography/copy over placeholders; SEO + OG tags + sitemap.
- Pitfalls: generic template look, unoptimized images, layout shift from fonts.

## api-backend (service, integration, webhook receiver)
- Defaults: contract first (OpenAPI / typed schema); one framework idiomatic to the language; Postgres or the team's DB; background jobs for slow work.
- Shape: transport -> service -> repository; idempotency keys on mutations; pagination + rate limits from day one.
- Tests: contract tests against the schema, integration with real DB, property tests for parsers/money.
- Threats: injection, broken authN/authZ, excessive data exposure, unauthenticated webhooks (verify signatures), SSRF, DoS via unbounded input.
- Observability: structured logs with request IDs, health/readiness endpoints, basic metrics.
- Pitfalls: leaking internals in errors, no versioning plan, N+1 queries.

## cli (developer tool, automation)
- Defaults: single static binary language (Go / Rust) or the ecosystem the users already have (Node/Python) when distribution is via package manager.
- Shape: argument parsing -> command handlers -> pure core; stable exit codes; `--json` output for scripting; respects `NO_COLOR`.
- Tests: golden-file output tests, subprocess tests for exit codes, Windows/macOS/Linux matrix if you ship to all three.
- Threats: shell/command injection, path traversal, unsafe temp files, credentials in shell history/logs, auto-update integrity.
- Pitfalls: no `--help` examples, interactive-only flows (breaks CI), non-deterministic output.

## library (package, SDK)
- Defaults: smallest public surface; semver; typed API; zero or minimal runtime deps.
- Shape: public API file(s) separate from internals; examples compiled in CI.
- Tests: API-level tests mirroring README examples, compatibility matrix for supported runtimes, type tests.
- Threats: supply chain (publish with provenance, 2FA, trusted publishing), prototype pollution / unsafe deserialization, ReDoS.
- Docs: README quickstart in < 30 lines, CHANGELOG, migration notes for breaking changes.
- Pitfalls: leaking internal types, breaking changes in minors, no deprecation path.

## mobile (iOS/Android/cross-platform)
- Defaults: cross-platform framework only when team lacks native skills; otherwise native per platform; offline-first data layer if connectivity is unreliable.
- Shape: UI -> state -> repository -> remote/local sources.
- Tests: unit + component, a few device-level flows, accessibility labels/dynamic type checks.
- Threats: insecure local storage (use Keychain/Keystore), certificate pinning decisions, deep-link hijacking, over-broad permissions, API keys in the binary.
- Pitfalls: ignoring store review rules, no crash reporting, no migration plan for local DB.

## ai-llm-app (chat, agents, RAG, extraction)
- Defaults: provider SDK behind a thin interface; structured outputs; prompts versioned in files; streaming UI. Verify model IDs and parameters in provider docs (see `claude-api` skill for Anthropic).
- Shape: prompt/templates -> orchestration -> tools -> storage; retrieval separated from generation.
- Tests: eval set (inputs + expected properties) run in CI, deterministic unit tests around parsing/tool calls, cost/latency budget checks.
- Threats: prompt injection (treat retrieved/tool content as untrusted), data exfiltration through tools, over-privileged tools, PII in logs/traces, runaway cost (per-user limits, max tokens, loop caps).
- Pitfalls: no evals ("vibes" regression), unbounded agent loops, logging full prompts with PII, no fallback on provider errors.
