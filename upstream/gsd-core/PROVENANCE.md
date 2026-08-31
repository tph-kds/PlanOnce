# GSD Core provenance

- Repository: `https://github.com/open-gsd/gsd-core`
- Release: `v1.12.0`
- Release commit: `ceed559`
- License: MIT
- Captured runtime: Claude local installation from the uploaded repository, installed with profile marker `core,audit`.

`runtime/` preserves the full GSD v1.12.0 runtime payload that was installed under `.claude/gsd-core`, with only machine-local absolute paths de-localized according to `TRANSFORMS.json`.

`profiles/claude-core-audit/` preserves the actual surfaced commands, agents, hooks and scripts from that installation, with the same de-localization transforms, but it is intentionally inert. Machine-specific `settings.local.json`, installer state and staging directories are excluded from the PlanOnce release.

PlanOnce uses GSD semantics for current-state mapping, bounded execution waves, verification/audit, review and state/resume discipline. PlanOnce remains the orchestration and planning authority.
