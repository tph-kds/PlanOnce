# Research provenance — v0.4 provider/distribution + security/review hardening

Research reviewed on **2026-08-30**. PlanOnce v1.0 keeps the independently authored, provider-neutral security/review workflows and hardens multi-provider Agent Skills distribution informed by public patterns from the ecosystems below. No proprietary OpenAI/Anthropic security workflow is vendored or copied verbatim.

## Public references evaluated

- Anthropic Claude Code security-guidance: https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance
- Anthropic official Claude Security plugin: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-security
- Anthropic code-review / PR-review patterns: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review and https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit
- OpenAI Plugins / Codex plugin format: https://github.com/openai/plugins
- OpenAI public Codex Security skill surfaces (research only; proprietary plugin): https://github.com/openai/plugins/tree/main/plugins/codex-security
- Trail of Bits Agent Skills: https://github.com/trailofbits/skills
- Superpowers engineering/review discipline: https://github.com/obra/superpowers
- GitHub Awesome Copilot audit/install patterns: https://github.com/github/awesome-copilot
- Snyk Agent Scan: https://github.com/snyk/agent-scan
- Semgrep: https://github.com/semgrep/semgrep
- OSV-Scanner: https://github.com/google/osv-scanner
- Trivy: https://github.com/aquasecurity/trivy
- Gitleaks: https://github.com/gitleaks/gitleaks
- Agent Skills open standard: https://github.com/agentskills/agentskills
- Vercel Skills CLI: https://github.com/vercel-labs/skills
- Vercel Skills CLI agent registry: https://github.com/vercel-labs/skills/blob/main/src/agents.ts
- OpenCode Agent Skills docs: https://opencode.ai/docs/skills
- Kiro Agent Skills docs: https://kiro.dev/docs/cli/skills/ and https://kiro.dev/docs/skills/
- Kilo Code Agent Skills docs: https://kilo.ai/docs/customize/skills

## Patterns intentionally adopted

- Scan/review and fix are separate consent/mutation phases.
- Diff-first review limits noise and helps distinguish regressions from Brownfield debt.
- Security combines deterministic scanners/tests with semantic threat-model-guided analysis.
- High-impact findings get independent/fresh-context verification when possible.
- Code review filters weak findings and integrates requirements plus fresh verification evidence.
- Production readiness includes operations/observability/migration/rollback, not just unit tests.
- Third-party Agent Skills/plugins/MCP configuration are a supply-chain boundary and are statically inspected before candidate execution.
- Networked scanners and MCP execution require explicit policy/consent because repository or dependency data may leave the machine and MCP discovery may start processes.
- Portable Agent Skills remain the primary distribution surface; provider-native plugins are secondary adapters over the same canonical skill tree.
- Exact `npx skills --agent` IDs are treated as versioned release data rather than inferred from display names.
- Kiro custom-agent resource configuration is documented explicitly because default-agent and custom-agent discovery differ.
- Kilo's current native `.kilo/skills` preference and the Skills CLI's legacy `.kilocode/skills` mapping are both surfaced so users can verify discovery instead of relying on a hidden assumption.
- OpenCode's portable `.agents/skills` compatibility is used intentionally because it is recognized by both the Skills CLI and current OpenCode docs.

## Deliberately not adopted

- Provider-specific autonomous hooks in the portable core.
- Automatic patch application, commit, push, merge, or production mutation.
- Automatic scanner installation or hidden network calls.
- A claim that a clean LLM/security scan proves the repository is secure.
- Duplicated Claude/Codex skill trees or provider-specific forks of PlanOnce workflow logic.
