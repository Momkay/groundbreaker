# Pawprint
Booking web app where pet owners find and book vetted local pet sitters.

## Commands
- `pnpm install` - install
- `pnpm dev` - dev server on :3000
- `pnpm test` - unit + integration (Vitest, real Postgres via docker compose)
- `pnpm test:e2e` - Playwright happy paths
- `pnpm lint` / `pnpm typecheck` - must be clean before any commit

## Structure
- `src/app/` routes (thin); `src/features/<name>/` domain logic, queries, components per feature
- `src/db/` schema + migrations (Drizzle); all SQL lives here
- `e2e/` Playwright specs

## Conventions
- Server Actions validate input with Zod at the boundary; domain functions take typed, already-valid data
- Money as integer cents; times stored UTC, shown in the sitter's timezone
- Errors: throw typed `AppError`, map to user messages in one place (`src/lib/errors.ts`)

## Hard rules
- Authorize every action by booking/sitter ownership on the server - never trust client ids
- Never weaken `CONSTRAINTS.md`: no skipped tests, no `eslint-disable` without a written reason
- No secrets in the repo; add new vars to `.env.example`

## Skill routing
| When | Use |
|---|---|
| Implementing logic or fixing a bug | `agent-skills:test-driven-development` |
| Building or restyling UI | `taste-skill:design-taste-frontend` |
| Touching auth, payments, input, deps | `agent-skills:security-and-hardening` |
| Before merge | `agent-skills:code-review-and-quality` |

## Definition of done
Acceptance criteria in `docs/SPEC.md` met, tests green, lint + types clean, docs updated.

## Docs
`docs/SPEC.md` · `docs/ARCHITECTURE.md` · `docs/DESIGN.md` · `CONSTRAINTS.md` · `docs/PLAN.md` · `KICKOFF.md`
