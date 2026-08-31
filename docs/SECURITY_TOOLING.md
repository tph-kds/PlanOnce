# Security tooling

PlanOnce security reviews are **tool-aware, not tool-dependent**. Always prefer **repo-native** checks already configured by the project. External tools are **optional** and PlanOnce **must not auto-install** any scanner or silently enable network access.

| Tool | Typical role | Network / privacy note | PlanOnce behavior |
|---|---|---|---|
| Semgrep | SAST, bug/security guardrails | Some registry/platform modes use network/telemetry | Reuse configured local/CI rules first; record exact mode |
| OSV-Scanner | Dependency vulnerability scan | Online mode queries vulnerability/package services with dependency metadata; offline mode exists | Run only when available/approved |
| Trivy | Filesystem/container vulnerabilities, secrets, IaC misconfiguration | Vulnerability DB/update may use network | Prefer project-pinned config; record scanners used |
| Gitleaks | Secret scanning | Commonly local/offline | Use when repository/team already adopts it |
| Snyk Agent Scan | Agent Skill/MCP supply-chain analysis | Requires Snyk service/token; MCP discovery may execute configured servers | Skill-directory static analysis only by default; MCP execution requires explicit consent + sandbox |

## Scanner selection order

1. Repository CI/security scripts and lockfile policies.
2. Existing local scanner configuration already committed to the repo.
3. Optional locally available tools that fit the risk.
4. Recommend an additional tool only when it closes a meaningful evidence gap.

A tool that is not installed produces `NOT_RUN`, not `PASS`.

## Network consent

Before a new security command contacts a third-party service or uploads/sends dependency/project metadata, explain what leaves the machine and ask for consent unless repository policy has already authorized that service.

## Untrusted repositories

Do not execute repository scripts/package-manager hooks or untrusted MCP servers merely to get more scan coverage. Use a sandbox/disposable environment first. Static inspection can proceed without executing candidate code.
