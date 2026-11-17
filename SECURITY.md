# Security policy

## Scope
groundbreaker ships instructions and two read-only helper scripts (`detect.py`, `validate.py`). Reports of interest: prompt-injection paths through skill vetting, scripts that read or write more than documented, unsafe defaults in generated files, or anything that bypasses the approval gates.

## Reporting
Use GitHub's private vulnerability reporting on this repository ("Security" tab -> "Report a vulnerability"). Please do not open a public issue for vulnerabilities. Expect an acknowledgement within a few days.

## Design guarantees (a violation is a bug)
- No file is written, and no skill or package installed, without explicit approval.
- Scripts are stdlib-only, read-only, make no network calls.
- No telemetry; project contents are never sent anywhere.
- Skill content fetched from elsewhere is treated as untrusted data.
