You are building Pawprint: a booking web app where pet owners find and book vetted local pet sitters. Read, in order: CLAUDE.md, docs/SPEC.md, docs/ARCHITECTURE.md, docs/DESIGN.md, CONSTRAINTS.md, docs/PLAN.md.

Context: owners in one city today book sitters through chat groups; double bookings and no-shows are the pain. Success = 50 bookings in the first month with under 5% cancelled by the sitter.
Stack (decided): TypeScript, Next.js, Postgres + Drizzle, Auth.js, Stripe Checkout, Vitest + Playwright. Do not substitute without asking.
Quality bar: server-side authorization on every action, WCAG 2.2 AA, LCP under 2.5s, 80% line coverage on `src/features/**`, zero lint/type warnings.
Skills: TDD for logic, design skill for UI, security skill for auth/payments, review skill before merge.
Working method: one vertical slice at a time from docs/PLAN.md; write the failing test first; run `pnpm test`, `pnpm lint` and `pnpm typecheck` before declaring done; check UI in a real browser.
Stop and ask when: adding a dependency, changing the data model after slice 2, any payment flow change, or when a constraint would have to be weakened.
Start now with slice 1: "Owner can see a sitter's availability and request a booking" - done means the acceptance criteria for feature F1 in docs/SPEC.md pass in an e2e test.
