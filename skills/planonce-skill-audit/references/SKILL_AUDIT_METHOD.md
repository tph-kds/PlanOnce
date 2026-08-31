# Agent Skill supply-chain audit

Agent Skills can bundle instructions, scripts, references, assets, hooks through provider plugin systems, and links to external executables. Treat them like executable process policy.

## Static-first checks

- Valid `SKILL.md` name/description and bounded trigger scope.
- No instruction that asks the agent to ignore higher-authority user/system policy.
- No hidden or surprising access to credentials, private data, wallets/payments, or destructive tools.
- No remote code execution from mutable URLs without verification/pinning.
- Review scripts for network access, filesystem writes, subprocesses, privilege changes, obfuscation, and secret handling.
- Review hooks for when they execute and what they can mutate.
- Review MCP declarations but do not start untrusted servers during static audit.
- Record source revision and license.

## Optional scanner

Snyk Agent Scan can analyze Agent Skills and MCP configurations for prompt injection, malicious code, credential handling, secret detection, untrusted content, and unverifiable dependencies. Its MCP discovery can execute configured stdio servers, so default PlanOnce audits should target skill files/directories and keep MCP execution disabled unless the user explicitly approves isolated execution.
