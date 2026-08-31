# Security

PlanOnce skills can direct coding agents to read/write code and run repository commands. Treat every skill update as executable-process policy.

## Project rules

- Review third-party/upstream pin changes before release.
- Never auto-fetch or execute upstream methodology content at runtime.
- Never auto-install security scanners from a skill.
- Do not place secrets in `.planonce/` artifacts.
- Security-boundary, authorization, tenant-isolation, destructive-migration, payment/data-correctness, and other one-way-door changes use Large workflow gates.
- `planonce-security` is source-read-only by default; fixes require explicit `planonce-security-fix` intent.
- `planonce-skill-audit` treats third-party skills/plugins as untrusted and does not execute candidate scripts/hooks/MCP servers during default audit.
- Network/security services require repository authorization or explicit user consent; unavailable checks are not PASS.

Run the repository release gate before publishing:

```bash
python scripts/release_gate.py
```

Report vulnerabilities in PlanOnce itself privately to the repository maintainer rather than opening a public exploit issue.
