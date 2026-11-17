# Changelog

Format: [Keep a Changelog](https://keepachangelog.com), versions follow [SemVer](https://semver.org).

## [0.1.1] - 2026-11-17
### Added
- `scripts/check_answers.py`: validates `--from` files (enums, types, pasted secrets) before anything is written.
- `tools/test_scripts.py`: 20 behavior tests for the helper scripts, run in CI; verified to fail when the scripts are deliberately broken.

### Fixed
- `--from` no longer writes without approval: it previews unless `--yes` is given.
- Allowed values for every answers-file enum are now defined.
- Greenfield `CLAUDE.md` no longer claims unverifiable commands; slice 1 creates them.
- Placeholder check no longer flags generics such as `Array<Foo>`.
- Defined behavior when a UI project supplies no `ui` answers.

### Tested
- Non-interactive greenfield run (web app) and brownfield run (existing `CLAUDE.md` with user rules preserved verbatim); both validate clean.
- Not yet tested: interactive interview, skill discovery/vetting against real candidates, `refresh`.

## [0.1.0] - 2026-11-17
### Added
- `/groundbreaker init | skills | refresh | validate` with `--quick`, `--dry-run`, `--from`.
- Adaptive interview, project profiles, skill discovery and vetting checklist.
- Generators for SPEC, KICKOFF, ARCHITECTURE, DESIGN, CONSTRAINTS, CLAUDE.md, PLAN.
- `scripts/detect.py` and `scripts/validate.py`, plus `tools/lint_skill.py` and CI.
- Evals and trigger tests; sample output in `examples/pawprint`.

### Known limits
- Not yet run end to end on real projects; interview wording and default thresholds are unproven.
