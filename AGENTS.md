# PlanOnce repository instructions

This repository ships provider-neutral Agent Skills. Keep the end-user surface small, auditable, and production-oriented.

## Invariants

- Eleven user-facing skills: init + six implementation workflows + security scan + security fix + production review + skill supply-chain audit.
- No external installation prerequisite for Agent OS or GSD Core.
- Pinned upstream knowledge lives under `upstream/`; pin changes require lock/manifest/attribution/tests/release-note updates.
- Never hard-code a provider-only tool into a cross-provider workflow contract.
- One accepted planning authority per change; execution decomposition is not a second design pass.
- Human gates and evidence requirements cannot be removed for convenience.
- Brownfield workflows inspect existing behavior, tests, contracts, and analogous code before proposing changes.
- Security scan and production review are read-only by default; fixes are explicit, bounded follow-up actions.
- Treat third-party Agent Skills/plugins/MCP configuration as untrusted until audited; never execute candidate content during static audit.
- Never auto-install external scanners or send repository data to network services without explicit approval.
- No completion, security-closure, or ship-readiness claim without fresh verification evidence.

Run before release:

```bash
python scripts/release_gate.py
```

## v1.0 reliability authority

- Prefer `planonce-task` as the generic entry point, but keep it route-only; implementation planning belongs to exactly one selected Greenfield/Brownfield skill.
- Preserve `planonce.* /v1` artifact frontmatter when editing work artifacts.
- Normal/Large execution must match the `approved_plan_digest` recorded after human approval.
- Treat `FRESH` verification as revision/worktree-bound; relevant edits invalidate prior evidence.
- Route implementation defects through `FIX_REVERIFY`; use `BLOCKED_AMEND` only when accepted direction is invalidated by evidence.
- Never overwrite pre-existing dirty worktree state. Respect cooperative locks under `.planonce/locks/` when present.
