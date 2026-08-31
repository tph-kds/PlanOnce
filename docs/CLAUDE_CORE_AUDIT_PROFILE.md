# Preserved Claude GSD Core + Audit Profile

The uploaded project included GSD Core v1.12.0 installed locally for Claude with profile marker:

```text
core,audit
```

PlanOnce preserves the useful installed surface under:

```text
upstream/gsd-core/profiles/claude-core-audit/
```

The profile snapshot contains the surfaced commands, agents, hooks and supporting scripts, while intentionally excluding:

- `.claude/settings.local.json`;
- installer migration state;
- `.gsd-staging/`;
- absolute machine-specific Node/project paths.

This profile is **not activated automatically**. Its purpose is source provenance, auditability and maintaining PlanOnce's compiled behavior. Raw GSD commands are not required to use PlanOnce.

The core/audit surface captured from the uploaded installation includes the core project/discuss/plan/execute surface and review/verification commands such as `gsd-verify-work`, `gsd-review` and `gsd-code-review`, plus their required agents/runtime support.
