# Interview guide

Contents: principles · rounds · sharpening · answers file schema · plain-text fallback

## Principles
- Skip any question the repo, `prefs.json`, `team.md` or an earlier answer already settles.
- Option 1 = recommended default, labeled "(Recommended)" with a one-line reason.
- 4 questions max per call, 2-4 rounds total. Free text always available via "Other".
- Concrete options beat open questions ("calm & dense like Linear" vs "what style?").
- Do not ask technical questions the user can't judge (e.g. ORM choice) - decide, justify in the decision table.

## Rounds

**R1 What & who (always)**
- Idea in one sentence (free text).
- Type: web app / marketing site / API-backend / CLI / library / mobile / AI-LLM app / other.
- Primary user (end customers, internal team, developers, just me).
- Solo or team (affects CI, review, docs depth).

**R2 Shape & constraints** (brownfield: only unknowns)
- Stack: recommend one per profile with reason; offer 2 alternatives.
- Deploy target: managed platform / own server+containers / serverless / not decided (decide for me).
- Ambition: prototype / MVP / production-grade.
- Hard constraints (multi-select): budget cap, offline, compliance (GDPR, HIPAA, PCI), existing systems to integrate, other AI agents used (-> AGENTS.md).

**R3 Quality bar**
- Data sensitivity: none / accounts + PII / payments / health or legal.
- Auth: none / simple login / roles + orgs / SSO.
- Testing depth: smoke only / pragmatic pyramid / strict TDD.
- Performance/scale expectation and accessibility level (basic / WCAG AA).

**R4 UI & design** (only if the project has a UI)
- Direction: 3-4 concrete vibes + Other (e.g. calm-dense tool, bold editorial, playful, enterprise-neutral).
- Reference sites/apps (free text, optional).
- Brand assets/colors if they exist; light / dark / both; density.

## Sharpening (max 2)
Only if who / why / "done means" is still vague. Ask the single riskiest unknown first ("What is the first thing a user must be able to do for this to be worth shipping?"). Then stop interviewing - remaining gaps become `ASSUMPTION:` lines.

## `--quick`
Ask: R1 idea + type, then one combined question (ambition, stack, data sensitivity). Everything else defaulted and listed as assumptions.

## Answers file (`--from answers.json`)
```json
{
  "idea": "string", "type": "web-app", "users": "string", "team": "solo",
  "stack": "string|null", "deploy": "string|null", "ambition": "mvp",
  "constraints": ["gdpr"], "other_agents": false,
  "sensitivity": "pii", "auth": "roles", "testing": "pyramid", "a11y": "aa",
  "ui": {"direction": "string", "references": ["url"], "theme": "both"}
}
```
Unknown/missing keys fall back to defaults and are logged as assumptions. Validate enum values; reject unknown types with the allowed list.

## Plain-text fallback
No `AskUserQuestion`: send one numbered message per round, defaults marked `[default]`, accept answers like `1a 2b 3 default`.
