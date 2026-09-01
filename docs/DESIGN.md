# PlanOnce v1.0 design

PlanOnce is a **single-install, provider-neutral Agent Skills workflow pack** for production-grade AI-assisted coding.

## Product boundary

- End users install PlanOnce only.
- Agent OS and GSD Core are pinned vendored upstream engines. Their raw surfaces are inert; PlanOnce compiles the required behavior and remains the orchestration authority.
- Eleven user-facing skills stay stable: init + six Greenfield/Brownfield implementation workflows + security scan + security fix + production review + skill supply-chain audit.
- Runtime differences are isolated in capability adapters.
- Exact `npx skills --agent` IDs and install paths are versioned distribution data in `providers/registry.json`; display names are never used as guessed CLI IDs.
- Provider-specific manifests/adapters may improve ergonomics, but the canonical `skills/` tree remains single-source and portable.

## Authority

1. Human instructions and repository `AGENTS.md`/equivalent.
2. Approved `.planonce/PROJECT.md` and selected `.planonce/standards/`.
3. Accepted change `DESIGN.md` (Large) and `PLAN.md`/micro-plan.
4. Execution decomposition and `STATE.md`.

Lower layers may not silently contradict higher layers.

## Quality loop

Understand evidence → select standards → shape once → human approve → execute bounded slices → verify fresh evidence → security/review gates as required → requirement/diff audit → human ship.

## Distribution model

1. `npx skills add <owner>/planonce-agent-skills --all` is the primary community install surface.
2. Targeted installs use exact IDs from `providers/registry.json`, such as `opencode`, `kilo`, `kiro-cli`, `roo`, and `windsurf`.
3. First-class providers have a dedicated capability adapter under `providers/`; extended providers use `providers/generic.md` until specialization provides real value.
4. Path mismatches between an upstream provider and the Skills CLI are documented explicitly rather than hidden. Kilo Code is currently the notable example.
5. Provider limitations can change mechanics, never PlanOnce requirements, human gates, accepted plan, or evidence rigor.

The system optimizes for reliable production changes, not maximum autonomous code volume.
