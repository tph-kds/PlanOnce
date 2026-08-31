# Security review method

PlanOnce Security is a provider-neutral synthesis of public AppSec patterns, not a copy of any proprietary security workflow.

## Principles

1. **Diff-first when reviewing a change.** Attribute new regressions separately from legacy debt.
2. **Threat model before hunting.** Security review follows real assets, entry points, and trust boundaries.
3. **Deterministic + semantic.** Linters/scanners catch known patterns; agent reasoning covers cross-file business/security logic. Neither replaces the other.
4. **Verify findings.** A high-severity claim needs a concrete path, preconditions, and preferably a test/reproducer or independent challenge.
5. **Fix separately.** Review is read-only by default. Use `planonce-security-fix` only after a finding is selected.
6. **Evidence before status.** Missing or failed checks remain visible.

## Optional tooling and privacy

- **Semgrep:** SAST/code guardrails. Prefer an existing project configuration. Remote registry/app modes can have network/telemetry implications; follow repository policy.
- **OSV-Scanner:** dependency vulnerability scanning. Online mode sends dependency metadata to vulnerability/package services; offline mode is available after database preparation.
- **Trivy:** filesystem/container vulnerability, secret, and misconfiguration scanning.
- **Gitleaks:** secret scanning when already adopted by the repository/team.
- **Snyk Agent Scan:** useful for Agent Skill/MCP supply-chain review. Do not scan untrusted MCP configs in a way that starts servers without explicit consent and isolation.

Do not download or install these tools merely because this skill mentions them. If unavailable, record `NOT_RUN` and provide an optional command recommendation.

## Severity and confidence

Severity describes impact/exploitability; confidence describes evidence quality. Do not use high severity to hide low confidence.

- Critical/High: verify independently before treating as a release blocker whenever possible.
- Medium/Low: report when actionable and evidenced; avoid noisy style-only security commentary.

## AI/agent security

When the product uses LLMs, MCP, tools, RAG, browsers, or external content, also inspect: indirect prompt injection, tool permission scope, untrusted-content + destructive-tool combinations, secret exposure to model context, tenant/context isolation, output-to-action validation, and auditability.
