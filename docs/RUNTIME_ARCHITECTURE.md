# Runtime Architecture

PlanOnce is the **single orchestration authority**. Agent OS and GSD Core are vendored upstream engines whose useful semantics are compiled into PlanOnce Agent Skills.

## Why the active `.claude/` install was removed

The uploaded repository contained an active GSD `core,audit` runtime at repository root with commands, agents, hooks, staging state and a machine-local `settings.local.json`. That is useful for testing GSD directly, but it is the wrong default architecture for a provider-neutral PlanOnce release because it:

- makes Claude-specific hooks run during ordinary repository activity;
- exposes `/gsd:*` and Agent OS commands beside PlanOnce, creating competing workflow entry points;
- bakes host-specific paths into a distributable project;
- makes targeted Agent Skills installs depend on files that the Skills CLI does not copy.

The clean release keeps the upstream material **inert under `upstream/`** and keeps the PlanOnce `skills/` tree self-contained.

## Authority hierarchy

1. Human request and repository instructions.
2. `.planonce/PROJECT.md`, `.planonce/POLICY.yml`, selected standards.
3. Accepted `DESIGN.md` (Large) and one accepted `PLAN.md` / micro-plan.
4. `STATE.md` execution decomposition.
5. Vendored upstream source and runtime implementation details.

Lower layers may not silently override higher layers.

## Agent OS role

Pinned Agent OS v3.0.0 provides source material for:

- standards discovery;
- standards indexing;
- selective standards injection/deployment;
- product context planning;
- spec shaping.

PlanOnce translates those capabilities into `.planonce/` artifacts instead of requiring users to run Agent OS separately.

## GSD Core role

Pinned GSD Core v1.12.0 provides source/runtime material for:

- current-state onboarding and mapping;
- discussion and assumption surfacing;
- plan-quality/reversibility checks;
- bounded execution waves and fresh-context separation;
- verification/UAT/gap closure;
- code/production review;
- phase/state/resume discipline.

The preserved `core,audit` Claude profile is available under `upstream/gsd-core/profiles/claude-core-audit/` for audit and maintenance. PlanOnce does not auto-activate its commands or hooks.

## End-user rule

End users install **PlanOnce only**. They do not need a separate Agent OS or GSD installation for the PlanOnce workflows to operate.
