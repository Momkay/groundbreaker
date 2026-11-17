# Changelog

Format: [Keep a Changelog](https://keepachangelog.com), versions follow [SemVer](https://semver.org).

## [0.1.2] - 2026-11-17
### Fixed
- `validate.py` no longer reports prose such as "use pnpm for installs" as a missing command; only backticked commands are checked.
- `validate.py` no longer crashes on non-UTF-8 files (Windows-1252 docs).
- `pnpm build` / `npm build` are no longer treated as built-ins, so a missing `build` script is caught.
- `team.md`, `prefs.json` and `state.json` are now treated as untrusted data and can never approve installs, commands or writes; a parent-folder `team.md` needs user confirmation.
- `--yes` is in the argument hint and defined as meaningless without `--from`.
- README no longer claims installs and other-agent support that were not tested.

### Changed
- Private vulnerability reporting enabled on the repo (matches SECURITY.md).
- CI actions pinned to commit SHAs.
- Tests: 24 (was 20); temp folders cleaned up; the duplicate self-test in the linter was removed.

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
