# Installation

PlanOnce's **primary** distribution surface is the open Agent Skills format. This keeps one canonical skill tree portable across Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot, Cline, Kilo Code, Kiro, Roo Code, Windsurf, Qwen Code, Goose, OpenHands, and other compatible runtimes.

PlanOnce has **no runtime dependency that the end user must install separately** for Agent OS or GSD Core. Their pinned source/runtime material is vendored for PlanOnce maintenance; security scanners, MCP servers, and daemons remain optional.

## Easiest: install all skills

Install every PlanOnce skill through the Skills CLI:

```bash
npx skills add tph-kds/PlanOnce --all
```

This is the simplest community-facing command because `--all` installs every skill to all selected/supported agent targets without individual prompts.

For project-local copies that should be committed rather than linked:

```bash
npx skills add tph-kds/PlanOnce --all --copy -y
```

Use `-g` only when PlanOnce should be global rather than project-scoped.

## Install to selected providers

Use exact Skills CLI agent IDs, not product display names:

```bash
npx skills add tph-kds/PlanOnce --skill '*' -a claude-code -a codex -a opencode -a kilo -a kiro-cli -a roo -a cursor -a gemini-cli -a github-copilot -a cline -a windsurf -y
```

Additional tracked Agent Skills targets:

```bash
npx skills add tph-kds/PlanOnce --skill '*' -a qwen-code -a goose -a openhands -y
```

Common one-provider commands:

```bash
npx skills add tph-kds/PlanOnce --skill '*' -a opencode -y
npx skills add tph-kds/PlanOnce --skill '*' -a kilo -y
npx skills add tph-kds/PlanOnce --skill '*' -a kiro-cli -y
npx skills add tph-kds/PlanOnce --skill '*' -a roo -y
npx skills add tph-kds/PlanOnce --skill '*' -a windsurf -y
```

See `docs/PROVIDER_MATRIX.md` for the pinned ID/path matrix and provider-specific caveats.

## Important Kilo Code path note

Current Kilo Code documentation prefers:

```text
project: .kilo/skills/
global:  ~/.kilo/skills/
portable compatibility: .agents/skills/
```

The current `vercel-labs/skills` main branch still maps the `kilo` agent ID to the legacy `.kilocode/skills/` path. PlanOnce does not hide this discrepancy. Use the normal project-scope `npx skills` flow and verify that Kilo discovers `planonce-init`; if copying manually, prefer `.kilo/skills/` or `.agents/skills/` from current Kilo documentation.

## Important Kiro custom-agent note

The exact Skills CLI target is **`kiro-cli`**.

Kiro's default agent discovers `.kiro/skills/` automatically. If you use a custom Kiro agent, include the skill resource glob in `.kiro/agents/<agent>.json`:

```json
{
  "resources": [
    "skill://.kiro/skills/*/SKILL.md",
    "skill://~/.kiro/skills/*/SKILL.md"
  ]
}
```

Kiro can then expose installed skills as slash commands using their canonical skill names.

## OpenCode path compatibility

The exact target is `opencode`:

```bash
npx skills add tph-kds/PlanOnce --skill '*' -a opencode -y
```

Current OpenCode documentation discovers `.opencode/skills/`, `.claude/skills/`, and portable `.agents/skills/` at project scope. The current Skills CLI uses `.agents/skills/` for OpenCode, so PlanOnce remains directly discoverable without duplicating the skill tree.

## Claude Code plugin surface

The repository root contains `.claude-plugin/plugin.json`; Claude Code plugins auto-discover the root `skills/` directory. For local/plugin development, point Claude Code at the repository directory with its plugin-directory workflow. The Agent Skills install above remains the recommended cross-provider path.

Do not rely on a custom marketplace manifest until the repository owner/name and publishing workflow are finalized and tested against the current Claude Code release; marketplace source schemas can evolve.

## Codex plugin surface

The repository root contains `.codex-plugin/plugin.json` and points its `skills` field at `./skills/`. This makes the same source tree usable as a Codex plugin without duplicating skills. The cross-provider `npx skills` installation remains the primary community path.

## Other providers

Roo Code, Windsurf, Qwen Code, Goose, OpenHands, and other Agent Skills-capable clients use the same portable skill pack. First-class adapters live in `providers/`; un-specialized runtimes fall back to `providers/generic.md`.

Provider-specific capabilities are optional optimizations. Missing subagents, special slash syntax, or isolated workspaces may reduce convenience, but never weaken PlanOnce human gates, scope discipline, or verification rigor.

## Generate a precise command locally

The repository includes a non-installing command generator backed by `providers/registry.json`:

```bash
python scripts/install_matrix.py --list
python scripts/install_matrix.py --providers opencode,kilo,kiro-cli,roo
```

It validates exact `npx` IDs and prints the command you can run.

## Verify after install

Ask the target agent to list or invoke one of these canonical skill names:

- `planonce-init`
- `planonce-green-small`, `planonce-green-normal`, `planonce-green-large`
- `planonce-brown-small`, `planonce-brown-normal`, `planonce-brown-large`
- `planonce-security`, `planonce-security-fix`
- `planonce-review`
- `planonce-skill-audit`

Examples:

```text
/planonce-brown-normal
/planonce-review
```

If a client does not expose slash commands, use natural language:

```text
Use planonce-review to review this diff for production readiness.
```

If a provider does not discover the skill, first check its installed path against `docs/PROVIDER_MATRIX.md`, then confirm the `SKILL.md` frontmatter is valid and restart/reload the provider session if skill discovery happens at session startup.
