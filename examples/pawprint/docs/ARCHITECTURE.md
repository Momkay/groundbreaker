# Architecture
Single Next.js app; feature folders hold domain logic; Postgres via Drizzle; Stripe webhook route verifies signatures and is idempotent on event id.

## Key decisions
- Monolith over services: one team, one city, no scaling need yet. Rejected: separate API service.
- Auth.js over hand-rolled auth: sessions and CSRF handled. Rejected: custom JWT.
