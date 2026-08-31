# PlanOnce Runtime Harmonization Design

## Goal

Turn the current mixed PlanOnce + active Claude Agent OS/GSD installation into one professional, provider-neutral PlanOnce product that preserves the useful upstream engines without letting their commands/hooks become competing orchestration authorities.

## Problems observed in the uploaded repository

- Root `.claude/` is a live GSD `core,audit` installation with hundreds of runtime files, commands, agents and hooks.
- `.claude/settings.local.json` contains a machine-specific absolute Node path and activates GSD hooks on ordinary repository operations.
- Agent OS commands are active under `.claude/commands/agent-os`, while PlanOnce exposes separate user-facing workflows. This creates duplicate planning/execution entry points.
- A complete Agent OS clone is nested under `upstream/agent-os/agent-os/agent-os/` and includes `.git`, while the declared upstream pin is v3.0.0.
- PlanOnce docs/skills still reference GSD v1.11.0 even though the installed GSD runtime is v1.12.0 with `core,audit`.
- Root `.git`, Python caches and install staging artifacts are present in the distributable ZIP.

## Authority model

1. Human request and repository-level instructions.
2. PlanOnce project policy and accepted PlanOnce artifacts.
3. One accepted PlanOnce design/plan for the change.
4. PlanOnce execution waves and state.
5. Vendored Agent OS/GSD source is an implementation/methodology engine, never a second orchestration authority.

Agent OS supplies standards/product/spec-shaping semantics. GSD supplies brownfield discovery, execution waves, verification/audit and state/review semantics. PlanOnce owns routing, artifact names, human gates and final ship decisions.

## Runtime layout

```text
upstream/
  agent-os/
    SOURCE/                       exact v3.0.0 git archive, no .git
    manifest.json
    PROVENANCE.md
  gsd-core/
    runtime/                      installed v1.12.0 gsd-core runtime payload
    profiles/claude-core-audit/   installed profile surface: commands/agents/hooks/scripts
    manifest.json
    PROVENANCE.md
```

The root repository must not contain an active `.claude/` GSD installation. `.claude-plugin/` remains the PlanOnce Claude plugin manifest.

## Workflow engine

All six implementation workflows use the same stage machine:

`CLASSIFY -> CONTEXT -> SHAPE -> APPROVE -> EXECUTE -> VERIFY -> REVIEW -> SHIP`

Greenfield changes emphasize Agent OS product/standards/spec shaping. Brownfield changes add GSD-style current-state mapping before shaping. Large workflows require design and security/readiness gates. Small workflows minimize ceremony but still retain an explicit micro-plan and evidence.

## Upstream use

Each user-facing skill is self-contained and contains a small `UPSTREAM_RUNTIME.md` contract naming the exact upstream capabilities it compiles. It must not call raw `/gsd:*` or `/agent-os:*` commands as a prerequisite.

The vendored upstream tree exists for provenance, auditing, maintenance and future recompilation of PlanOnce skills. End users install PlanOnce only.

## Clean distribution rules

The release ZIP excludes root `.git`, `.claude`, `.pytest_cache`, `__pycache__`, GSD staging/install state, and machine-specific settings. Integrity manifests recursively hash vendored upstream files.

## Verification

Release gating must prove:

- no active root `.claude/` runtime;
- Agent OS source is exact v3.0.0 content;
- GSD runtime reports v1.12.0;
- the preserved Claude profile is `core,audit` and includes required core/audit commands;
- no machine-specific absolute paths remain;
- every workflow skill has a self-contained runtime contract;
- all repository tests, validator, upstream hash verification and static skill audit pass.
