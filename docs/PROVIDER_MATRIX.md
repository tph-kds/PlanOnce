# Provider installation matrix

Checked against the current `vercel-labs/skills` agent registry on **2026-08-30**. The exact `--agent` IDs below are treated as release data in `providers/registry.json`; do not rename them from display-name intuition.

## Recommended install patterns

Install all PlanOnce skills to all agents selected/discovered by the Skills CLI:

```bash
npx skills add <owner>/planonce-agent-skills --all
```

Install all PlanOnce skills to a selected provider set:

```bash
npx skills add <owner>/planonce-agent-skills --skill '*' -a claude-code -a codex -a opencode -a kilo -a kiro-cli -a roo -a cursor -a gemini-cli -a github-copilot -a cline -a windsurf -y
```

Extended portable targets can be added with the same command:

```bash
npx skills add <owner>/planonce-agent-skills --skill '*' -a qwen-code -a goose -a openhands -y
```

## Validated target IDs

| Provider | Exact `npx` agent ID | Skills CLI project path | Global path | PlanOnce support |
|---|---|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` | First-class adapter |
| Codex | `codex` | `.agents/skills/` | `~/.codex/skills/` | First-class adapter + root Codex plugin |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` | First-class adapter; OpenCode also discovers `.opencode/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` | First-class adapter |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` | First-class adapter |
| GitHub Copilot | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` | First-class adapter |
| Cline | `cline` | `.agents/skills/` | `~/.agents/skills/` | First-class adapter |
| Kilo Code | `kilo` | current CLI: `.kilocode/skills/` | current CLI: `~/.kilocode/skills/` | First-class adapter; see Kilo compatibility note |
| Kiro | `kiro-cli` | `.kiro/skills/` | `~/.kiro/skills/` | First-class adapter; custom-agent resource note applies |
| Roo Code | `roo` | `.roo/skills/` | `~/.roo/skills/` | First-class adapter |
| Windsurf | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` | First-class adapter |
| Qwen Code | `qwen-code` | `.qwen/skills/` | `~/.qwen/skills/` | Extended / generic adapter |
| Goose | `goose` | `.goose/skills/` | `~/.config/goose/skills/` | Extended / generic adapter |
| OpenHands | `openhands` | `.openhands/skills/` | `~/.openhands/skills/` | Extended / generic adapter |

The Skills CLI supports additional agents beyond this table. PlanOnce only claims an explicit provider tier when the ID/path is pinned in `providers/registry.json`; other Agent Skills-compatible runtimes use `providers/generic.md`.

## OpenCode

Use the exact target ID:

```bash
npx skills add <owner>/planonce-agent-skills --skill '*' -a opencode -y
```

Current OpenCode docs discover all of these project sources:

```text
.opencode/skills/
.claude/skills/
.agents/skills/
```

The current Skills CLI uses `.agents/skills/` for project-scope OpenCode installation, which is therefore a portable and officially recognized path.

## Kilo Code

Use the exact target ID:

```bash
npx skills add <owner>/planonce-agent-skills --skill '*' -a kilo -y
```

There is an upstream path transition worth keeping visible:

- current Kilo Code docs prefer `.kilo/skills/` and `~/.kilo/skills/`;
- Kilo also discovers the portable `.agents/skills/` compatibility directory;
- the current `vercel-labs/skills` main branch still maps `kilo` to the legacy `.kilocode/skills/` path.

Because the Skills CLI maintains a canonical Agent Skills copy during its normal project installation flow, PlanOnce recommends the default project install and then verifying discovery in Kilo. If you bypass the CLI and copy manually, prefer `.kilo/skills/` or the portable `.agents/skills/` path from Kilo's current documentation.

## Kiro

Use **`kiro-cli`**, not `kiro`:

```bash
npx skills add <owner>/planonce-agent-skills --skill '*' -a kiro-cli -y
```

Kiro's default agent automatically discovers workspace `.kiro/skills/` and global `~/.kiro/skills/`.

For a custom Kiro agent, add skills to its `resources`:

```json
{
  "resources": [
    "skill://.kiro/skills/*/SKILL.md",
    "skill://~/.kiro/skills/*/SKILL.md"
  ]
}
```

## Roo Code and Windsurf

```bash
npx skills add <owner>/planonce-agent-skills --skill '*' -a roo -a windsurf -y
```

PlanOnce keeps these adapters capability-based. Provider-specific modes may change how commands or edits are executed, but do not change the accepted PlanOnce plan, human gates, or evidence requirements.

## Generate commands from the registry

Maintainers and advanced users can avoid hand-typing IDs:

```bash
python scripts/install_matrix.py --list
python scripts/install_matrix.py --providers opencode,kilo,kiro-cli,roo
python scripts/install_matrix.py --providers claude-code,codex,opencode,cursor,gemini-cli --repo tph-kds/planonce-agent-skills
```

The helper prints the `npx skills add ...` command; it never downloads or installs anything itself.
