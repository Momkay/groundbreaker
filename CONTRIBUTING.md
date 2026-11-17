# Contributing

1. Run `python tools/lint_skill.py` before every PR; CI runs the same check.
2. Keep `SKILL.md` under 500 lines. Detail goes in `references/`, linked directly from `SKILL.md` (one level deep). Reference files over 100 lines start with a `Contents` line.
3. Be concise: Claude is already smart. Every line must earn its tokens; generic advice gets cut.
4. Description is third person and says what the skill does and when to use it.
5. Behavior change = update `evals/evals.json` (and `triggers.json` if triggering changes) and `CHANGELOG.md`.
6. Scripts stay stdlib-only, read-only, no network, with a documented manual fallback in the skill.
7. Profile defaults name ecosystems, never pinned versions.

Good first contributions: new profiles (game, browser extension, data pipeline), better interview options, additional validator checks, translations of the README.
