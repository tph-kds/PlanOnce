# Changelog

## 0.7.0 — Workflow Reliability Layer

- Added `planonce-task`, a route-only generic entry point that selects the smallest safe Greenfield/Brownfield workflow without creating a second plan.
- Added `planonce.* /v1` versioned artifact frontmatter across implementation templates.
- Added deterministic approved-plan SHA-256 integrity for Normal/Large workflows.
- Added revision + working-tree-bound verification freshness; code changes invalidate stale evidence.
- Split execution failures into `FIX_REVERIFY`, `BLOCKED_AMEND`, and `DIAGNOSE`.
- Added workspace preflight guidance and atomic cooperative scope locks under `.planonce/locks/`.
- Added deterministic runtime evals to the release gate and a provider-neutral external coding-agent eval adapter protocol.
- Added standard-library helpers `reliability.py`, `route_task.py`, `run_evals.py`, and `run_agent_evals.py`; no daemon/database/runtime dependency added.

## 0.6.0 — Runtime-harmonized production workflows

- Recovered the uploaded mixed `.claude` installation into a clean provider-neutral PlanOnce architecture; active GSD hooks/commands are no longer shipped at repository root.
- Vendored an exact Agent OS v3.0.0 source export under `upstream/agent-os/SOURCE/` with no embedded `.git` metadata.
- Preserved the uploaded GSD Core v1.12.0 runtime and Claude `core,audit` surface under `upstream/gsd-core/`, de-localizing machine-specific absolute paths and keeping the profile inert.
- Added `docs/RUNTIME_ARCHITECTURE.md`, `docs/WORKFLOW_ENGINE.md`, and `docs/CLAUDE_CORE_AUDIT_PROFILE.md` to define one orchestration authority and the normalized Greenfield/Brownfield stage machine.
- Added self-contained `UPSTREAM_RUNTIME.md` contracts to all six implementation workflows so targeted Agent Skills installs retain the required upstream behavior without invoking raw `/gsd:*` or Agent OS commands.
- Updated the GSD pin to v1.12.0 / `ceed559`, recursive upstream integrity manifests, release validation, and portability checks.
- Removed distributable `.git`, active `.claude`, installer staging/state, Python caches, and machine-specific settings from the release.

## 0.4.0 — Multi-provider distribution hardening

- Added a validated `providers/registry.json` as the source of truth for exact `npx skills --agent` IDs and current installation paths.
- Added first-class provider adapters for Kilo Code (`kilo`), Kiro (`kiro-cli`), Roo Code (`roo`), and Windsurf (`windsurf`).
- Expanded documented and tested provider targets to Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot, Cline, Kilo Code, Kiro, Roo Code, Windsurf, Qwen Code, Goose, and OpenHands.
- Added `scripts/install_matrix.py` to generate precise provider-targeted `npx skills add` commands from the registry without performing installation.
- Added `docs/PROVIDER_MATRIX.md` with exact IDs, project/global paths, OpenCode compatibility paths, Kiro custom-agent resources, and Kilo's current native-path vs Skills-CLI legacy-path discrepancy.
- Expanded every self-contained skill's provider guidance so copy-only installers keep Kilo/Kiro/Roo/Windsurf instructions with the skill.
- Hardened validation/tests so provider display names cannot silently drift from actual Skills CLI IDs.

## 0.3.0 — Security, review, and distribution hardening

- Added `planonce-security`: read-only-by-default diff/codebase security review with threat modeling, repo-native deterministic scans, independent finding verification, origin/confidence/severity, and fix recommendations.
- Added `planonce-security-fix`: explicit Finding-ID remediation with staleness checks, regression/reproducer evidence, minimal scope, compatibility preservation, re-scan, and fresh verification.
- Added `planonce-review`: diff-first code/production-readiness review, requirement and operations audit, introduced-vs-pre-existing classification, backlog surfacing, and explicit ship decisions.
- Added `planonce-skill-audit`: static-first Agent Skill/plugin supply-chain review with no execution of untrusted candidate scripts/hooks/MCP servers.
- Integrated review/security routing into all six Greenfield/Brownfield Small/Normal/Large workflows; Large requires security + final production review.
- Added optional security-tool guidance for Semgrep, OSV-Scanner, Trivy, Gitleaks, and Snyk Agent Scan without auto-install or hidden network use.
- Added root Claude Code and Codex plugin manifests while preserving one canonical `skills/` tree and `npx skills` as the primary cross-provider install path.
- Added install, review, security tooling, research provenance, and release-gate documentation.
- Added deterministic skill-pack self-audit, consolidated release gate, expanded eval fixtures, and plugin/install contract tests.
- Added `.planonce/POLICY.yml` project policy for review/security/network/human gates, high-confidence review filtering, read-only production evidence checks, and full skill-resource self-audit.


## 0.2.0 — Production-oriented workflow pack

- Pinned Agent OS v3.0.0 and GSD Core v1.11.0 as auditable methodology sources; no runtime auto-update.
- Made every Agent Skill self-contained for installers that copy only individual skill directories.
- Added provider guidance for Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot, Cline, and generic runtimes.
- Added one planning authority, plan-amendment protocol, resumable state, bounded waves, fresh-context fallbacks, and human gates.
- Added Small/Normal/Large escalation rules, one-way-door/security triggers, rollback and threat-model gates.
- Added evidence contract, UAT/final-diff audit, risk-scaled production checks, and optional AI/LLM quality/cost/latency evaluation.
- Added upstream provenance/hash verification, repository validator, CI contract tests, and routing/failure-mode eval fixtures.
