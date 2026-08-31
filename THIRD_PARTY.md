# Third-party upstream sources

PlanOnce is an independent Agent Skills workflow pack. It is not affiliated with or endorsed by the upstream projects below.

## Agent OS

- Project: https://github.com/buildermethods/agent-os
- Pin: `v3.0.0` / `809fb4e3e20451e3dd9ad9b253111776db373518`
- License: MIT; vendored license at `upstream/agent-os/LICENSE`
- Vendored form: exact release source exported with `git archive` into `upstream/agent-os/SOURCE/` with no `.git` metadata.
- PlanOnce use: standards discovery/index/injection, product context, and spec shaping.

## GSD Core

- Project: https://github.com/open-gsd/gsd-core
- Pin: `v1.12.0` / `ceed559`
- License: MIT; vendored license at `upstream/gsd-core/LICENSE`
- Vendored form: the uploaded installed v1.12.0 runtime is preserved under `upstream/gsd-core/runtime/`; the uploaded Claude `core,audit` surface is preserved under `upstream/gsd-core/profiles/claude-core-audit/`.
- Portability transform: machine-local absolute paths introduced by the local installer were de-localized; the transformation policy is documented in `upstream/gsd-core/TRANSFORMS.json`.
- PlanOnce use: current-state mapping, bounded execution, verification, audit/review, and state/phase discipline.

The upstream directories are **inert source/provenance material**. They are not auto-activated as root provider configuration and end users do not need to install Agent OS or GSD separately to use PlanOnce.

## Research-only references for security/review

PlanOnce's security/review skills are independently authored. Public behavior/documentation from Anthropic Claude Code/plugins, OpenAI/Codex security materials, Trail of Bits Skills, Superpowers, GitHub Awesome Copilot, Snyk Agent Scan, Semgrep, OSV-Scanner, Trivy, Gitleaks, the Agent Skills specification, and the Vercel Skills CLI informed design decisions.

No proprietary OpenAI or Anthropic hosted security implementation is vendored. Optional external scanners remain separate products with their own licenses, privacy terms, and installation processes.
