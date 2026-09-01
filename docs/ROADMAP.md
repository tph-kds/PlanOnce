# Roadmap

## v0.3 — production security and review gates

- Security diff/codebase scan with evidence-based findings.
- Explicit finding-scoped security fixes with re-verification.
- Diff-first code/production-readiness review with backlog separation and ship decision.
- Agent Skill/plugin supply-chain audit before install/update.
- Primary cross-provider `npx skills` distribution plus native Claude Code and Codex plugin manifests.
- Release-gate self-audit and optional deterministic scanner guidance.

## Next evidence-driven candidates

Add only after real usage demonstrates need:

- executable routing/effectiveness evals across Claude Code, Codex, and OpenCode;
- signed release/fingerprint publication and update-diff audit;
- optional adapters for production observability evidence (without creating a mandatory SaaS dependency);
- policy packs for organization-specific security/ship thresholds;
- additional native provider packaging only where the provider has a stable public manifest contract.

Do not add a daemon, database, orchestration service, or auto-installed scanner without evidence that the portable skill model is insufficient.

## v1.0 — Workflow Reliability Layer (implemented)

- route-only `planonce-task` entry point;
- versioned Markdown artifact frontmatter;
- approved-plan SHA-256 integrity;
- revision/worktree-bound verification freshness;
- explicit `FIX_REVERIFY` / `BLOCKED_AMEND` / `DIAGNOSE` failure routing;
- cooperative scope locks and workspace-safety contract;
- deterministic runtime evals in the release gate;
- provider-neutral external coding-agent eval adapter protocol.

## Next maturity work

Favor depth over more commands: production pattern packs, semantic upstream-drift review, more real-agent fixture benchmarks, artifact schema migration tests, and measured routing/verification quality across providers.
