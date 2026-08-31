# Captured GSD Claude core,audit surface

The uploaded PlanOnce repository contained GSD Core **v1.12.0** with `.gsd-profile` = `core,audit`. PlanOnce preserves that surfaced Claude installation here as inert source.

## Surfaced commands (15)

- `gsd-code-review.md`
- `gsd-config.md`
- `gsd-discuss-phase.md`
- `gsd-execute-phase.md`
- `gsd-help.md`
- `gsd-import.md`
- `gsd-new-project.md`
- `gsd-phase.md`
- `gsd-plan-phase.md`
- `gsd-quick.md`
- `gsd-review.md`
- `gsd-settings.md`
- `gsd-surface.md`
- `gsd-update.md`
- `gsd-verify-work.md`

## Surfaced agents (20)

- `gsd-advisor-researcher.md`
- `gsd-assumptions-analyzer.md`
- `gsd-code-fixer.md`
- `gsd-code-reviewer.md`
- `gsd-codebase-mapper.md`
- `gsd-debugger.md`
- `gsd-executor.md`
- `gsd-integration-checker.md`
- `gsd-nyquist-auditor.md`
- `gsd-pattern-mapper.md`
- `gsd-phase-researcher.md`
- `gsd-plan-checker.md`
- `gsd-planner.md`
- `gsd-project-researcher.md`
- `gsd-research-synthesizer.md`
- `gsd-roadmapper.md`
- `gsd-ui-auditor.md`
- `gsd-ui-checker.md`
- `gsd-ui-researcher.md`
- `gsd-verifier.md`

Supporting hooks: **39 files**  
Supporting scripts: **18 files**

## How PlanOnce uses this

PlanOnce does **not** expose these commands as competing end-user workflows. The six implementation skills compile the relevant semantics into the shared PlanOnce stage machine.

- Core planning/execution semantics: `new-project`, `discuss-phase`, `plan-phase`, `execute-phase`.
- Audit/review semantics: `verify-work`, `review`, `code-review`.
- Surface/phase/config helpers are source context for runtime behavior, not user-facing PlanOnce entry points.
- GSD capabilities that exist in the full runtime but are not surfaced in this captured profile do not become implicit PlanOnce requirements. PlanOnce security remains owned by `planonce-security` / `planonce-security-fix`.
