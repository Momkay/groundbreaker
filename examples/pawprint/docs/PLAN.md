# Plan
Slice 1: Request a booking | depends on: none | size: M
  Delivers: owner can pick an open day and request a booking
  Tasks: schema + seed data, availability query, request action with authz, booking page, e2e test
  Acceptance: F1 criteria pass in Playwright
  Risks: availability race conditions - use a unique constraint on sitter + day

Slice 2: Accept or decline | depends on: 1 | size: M
  Delivers: sitter inbox with accept/decline and 24h auto-decline job
  Tasks: inbox page, accept/decline actions, scheduled expiry, email
  Acceptance: F2 criteria pass

Slice 3: Deposit payment | depends on: 2 | size: L
  Delivers: Stripe Checkout deposit and webhook confirmation
  Tasks: checkout session, webhook route with signature check, idempotency table
  Acceptance: F3 criteria pass, replay test green
  Risks: webhook ordering; test with Stripe CLI fixtures
