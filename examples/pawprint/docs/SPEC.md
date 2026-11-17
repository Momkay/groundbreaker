# Pawprint - Spec
## Objective
Pet owners in one city book vetted sitters without chat-group chaos. Success: 50 bookings in month one, under 5% sitter cancellations.

## Users
Owners (book), sitters (publish availability, accept bookings).

## Scope
MVP: F1-F3. Later: reviews, multi-city. Non-goals: in-app chat, insurance, native apps.

## Features
### F1 Request a booking
As an owner I see a sitter's open days and request a booking.
Acceptance:
- Only open days are selectable; a taken day cannot be requested
- Request creates a pending booking visible to both parties

### F2 Accept or decline
As a sitter I accept or decline a request within 24h.
Acceptance:
- Accepting marks the day taken and emails the owner
- No response in 24h auto-declines and frees the day

### F3 Pay a deposit
As an owner I pay a 20% deposit via Stripe Checkout when the sitter accepts.
Acceptance:
- Booking confirms only after a verified Stripe webhook
- Replayed webhooks do not double-confirm

## Threat model
Assets: booking data, owner addresses, payments. Top threats: IDOR on bookings, forged webhooks, address leakage before acceptance. Mitigations are the acceptance criteria above plus authz tests per action.

## Assumptions
ASSUMPTION: one city, one currency, English only.
ASSUMPTION: sitter vetting is manual and out of scope.

## Open questions
Who refunds a deposit when the sitter cancels?
