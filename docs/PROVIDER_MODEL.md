# Provider-neutral execution model

PlanOnce separates **workflow semantics** from **provider installation mechanics**.

## Runtime capabilities

PlanOnce specifies semantic capabilities, not vendor tool names:

1. **Ask human** — approval, ambiguity resolution, destructive/one-way decision gate.
2. **Read/write** — inspect and modify repository files.
3. **Run command** — tests, builds, lint/type/security/migration checks.
4. **Fresh worker** — optional isolated context for a bounded plan slice.
5. **Isolated workspace** — optional worktree/sandbox.

Provider adapters in `providers/` map these capabilities to Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot, Cline, Kilo Code, Kiro, Roo Code, Windsurf, or a generic Agent Skills runtime.

If a capability is absent, use the documented fallback. Missing optional automation may reduce speed; it must not reduce human gates, scope discipline, or verification rigor.

## Installation identity is data

Exact Skills CLI provider IDs and paths are release data in `providers/registry.json`. Examples:

```text
Claude Code      claude-code
Codex            codex
OpenCode         opencode
Kilo Code        kilo
Kiro             kiro-cli
Roo Code         roo
Windsurf         windsurf
```

Do not derive IDs by lowercasing display names. Kiro is the clearest example: the valid Skills CLI ID is `kiro-cli`, not `kiro`.

## Support tiers

- **First-class:** PlanOnce has a dedicated capability adapter and explicit install/path guidance.
- **Extended:** the current Skills CLI has a validated Agent Skills target, but PlanOnce intentionally uses the generic capability adapter until runtime-specific behavior justifies specialization.
- **Generic:** any Agent Skills-compatible runtime can follow the canonical `SKILL.md` contract if it can ask a human, read/write files, and run or delegate verification commands.

See `docs/PROVIDER_MATRIX.md` for exact targets and current path caveats.
