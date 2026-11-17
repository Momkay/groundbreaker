# groundbreaker

**Stop rewriting the same kickoff prompt. Run one command, answer a few questions, start building on solid ground.**

`/groundbreaker init` interviews you, decides the hard calls (stack, architecture, security, testing, UI), finds and vets the right skills, and writes the files your AI agent needs: a spec, a copy-paste kickoff prompt, architecture, design system, measurable quality constraints, `CLAUDE.md` and a vertical-slice plan. Then it validates its own output.

An Agent Skill for [Claude Code](https://claude.com/claude-code). The skill format follows the open Agent Skills standard, so it can also be used by other compatible agents.

## Why

Every new project starts the same loop: what prompt, what architecture, what about security and tests, which skills, what should the UI feel like? You answer it from scratch each time, and the answers drift between projects. groundbreaker turns the loop into one reviewed run with defaults that learn your taste.

| Without | With groundbreaker |
|---|---|
| A vague first prompt, rewritten when the agent goes sideways | One self-contained `KICKOFF.md` a cold session can start from |
| Security and tests bolted on late | Threat model and a measurable quality bar before line one |
| A pile of skills installed on a whim | Gaps found, each candidate vetted by reading its code, versions pinned |
| Docs that contradict each other | A validator checks placeholders, file references, commands, acceptance criteria |
| The same questions every project | Reusable answers saved once; per-repo and team standards respected |

## Install

Pick one.

```bash
# any agent that supports skills
npx skills add Momkay/groundbreaker --skill groundbreaker

# Claude Code plugin marketplace
/plugin marketplace add Momkay/groundbreaker
/plugin install groundbreaker@groundbreaker

# manual: copy the folder
cp -r skills/groundbreaker ~/.claude/skills/groundbreaker      # all projects
cp -r skills/groundbreaker .claude/skills/groundbreaker        # this repo only
```

Restart Claude Code. Python 3.8+ is optional: the two helper scripts speed things up, and every step has a manual fallback.

## Use

```
/groundbreaker init               full guided kickoff
/groundbreaker init --quick       3 questions, sensible defaults
/groundbreaker init --dry-run     preview everything, write nothing
/groundbreaker init --from a.json non-interactive, answers from a file
/groundbreaker skills             only discover, vet and wire skills
/groundbreaker refresh            detect drift between repo and docs
/groundbreaker validate           check the generated files
```

### What a run looks like

1. **Detect**: reads your repo (stack, scripts, CI, docs). Existing project? It only asks about what is missing.
2. **Interview**: 2-4 short rounds of multiple choice, recommended answer first.
3. **Decide**: a table of every decision with the reason, the rejected alternative and a confidence level, plus a threat model scaled to your data.
4. **Skills**: maps needs to skills, searches gaps, vets candidates, asks before installing.
5. **Preview**: you see every file and assumption. Nothing is written until you approve.
6. **Generate and verify**: writes the files, runs the validator, fixes what it flags.

### What you get

| File | Purpose |
|---|---|
| `KICKOFF.md` | The complete master prompt to start building |
| `docs/SPEC.md` | Objective, scope, features with acceptance criteria, assumptions, open questions |
| `docs/ARCHITECTURE.md` | Components, data model, short decision records |
| `docs/DESIGN.md` | Direction, tokens, states, accessibility (UI projects) |
| `CONSTRAINTS.md` | Measurable quality bar, each line enforced by a command |
| `CLAUDE.md` | Commands, conventions, hard rules, skill routing (under 100 lines) |
| `docs/PLAN.md` | Vertical slices, thinnest end-to-end path first |

See a complete sample in [`examples/pawprint`](examples/pawprint).

## Customize

- **Your defaults**: at the end of a run it offers to save reusable answers to `~/.claude/groundbreaker/prefs.json`. Nothing project-specific is stored.
- **Team standards**: put `.groundbreaker/team.md` in a repo or parent folder (required stack, security rules, review policy). It outranks personal defaults.
- **Profiles**: edit `skills/groundbreaker/references/profiles.md` to change defaults per project type (web app, marketing site, API, CLI, library, mobile, AI app).

## Trust and safety

- Nothing is written before you approve a preview, and existing files are never overwritten without asking.
- Skills and packages are never installed without approval. Candidates are vetted by reading their full `SKILL.md` and scripts; red flags (remote shell execution, secret access, hooks, prompt-override text) are rejected. The reviewed commit is pinned.
- Facts such as framework versions and setup steps are checked against docs, not memory. Anything unverified is labelled `ASSUMPTION:`.
- No telemetry. Project contents never leave your machine; the only network use is documentation and skill lookup.
- `allowed-tools` is limited to read-only tools plus questions, so every write and command still goes through your permission prompts.
- Found a vulnerability? See [SECURITY.md](SECURITY.md).

## Compatibility

| Environment | Status |
|---|---|
| Claude Code (CLI, desktop, IDE) | Primary target |
| Other Agent Skills-compatible agents | Core flow works; questions fall back to numbered plain text |
| Without Python | Works; detection and validation are done by hand using the same checklist |
| Offline | Works; skill discovery is skipped and version-sensitive facts are flagged |

It composes with other skills (spec, plan, security, TDD, design) when installed and does those steps itself when not.

## FAQ

**Does it work on an existing codebase?** Yes. Detected facts count as decided; it asks about the delta and merges into your existing `CLAUDE.md`.

**It's a tiny script, not an app.** It refuses to inflate: you get a short `CLAUDE.md` and a few-line spec.

**Can it run in CI or scripts?** `--from answers.json` is non-interactive and validates input.

**Will it lock me into a stack?** No. Defaults are starting points; the decision table lists the rejected alternatives so you can overrule.

## Development

```bash
python tools/lint_skill.py     # frontmatter, size, links, orphan references, script self-tests
```

`skills/groundbreaker/evals/` holds end-to-end scenarios and trigger tests. See [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
