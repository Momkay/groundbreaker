# Constraints
| Dimension | Threshold | Enforced by |
|---|---|---|
| Types and lint | strict TS, zero warnings | `pnpm typecheck && pnpm lint` in CI |
| Tests | 80% line coverage on `src/features/**`; every bug fix has a regression test | `pnpm test --coverage` in CI |
| Security | authz check on every server action; no secrets in repo; no high/critical audit findings | secret scan + `pnpm audit` in CI |
| Performance | LCP under 2.5s, CLS under 0.1, INP under 200ms on search and booking pages | Lighthouse CI |
| Accessibility | WCAG 2.2 AA on booking flow | axe in Playwright + manual keyboard pass |
| Process | no skipped or deleted tests, no new suppressions without a written reason | review checklist |
