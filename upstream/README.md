# Vendored upstream engines

This directory is deliberately **inert**. It exists so PlanOnce can audit, maintain and recompile the upstream behavior it depends on without asking end users to install separate workflow frameworks.

- `agent-os/SOURCE/` — exact Agent OS v3.0.0 release source exported with `git archive`; no nested `.git` metadata.
- `gsd-core/runtime/` — GSD Core v1.12.0 installed runtime captured from the uploaded project and de-localized to remove machine-specific absolute paths.
- `gsd-core/profiles/claude-core-audit/` — the actual Claude `core,audit` surfaced commands/agents/hooks/scripts captured from the uploaded install, preserved for audit but not auto-activated.

PlanOnce user-facing workflows live only in `skills/`. Do not add active provider runtime directories such as root `.claude/` back into release archives.
