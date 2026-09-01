// Generated/synchronized provider registry snapshot for the standalone website package.
export type ProviderTier = 'first-class' | 'extended';
export type Provider = {
  id: string;
  cliId: string;
  name: string;
  tier: ProviderTier;
  projectPath: string;
  globalPath: string;
  note?: string;
};

export const providers: Provider[] = [
  { id: 'claude-code', cliId: 'claude-code', name: 'Claude Code', tier: 'first-class', projectPath: '.claude/skills', globalPath: '~/.claude/skills' },
  { id: 'codex', cliId: 'codex', name: 'Codex', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.codex/skills' },
  { id: 'opencode', cliId: 'opencode', name: 'OpenCode', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.config/opencode/skills', note: 'OpenCode also discovers .opencode/skills and .claude/skills at project scope.' },
  { id: 'cursor', cliId: 'cursor', name: 'Cursor', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.cursor/skills' },
  { id: 'gemini-cli', cliId: 'gemini-cli', name: 'Gemini CLI', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.gemini/skills' },
  { id: 'github-copilot', cliId: 'github-copilot', name: 'GitHub Copilot', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.copilot/skills' },
  { id: 'cline', cliId: 'cline', name: 'Cline', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.agents/skills' },
  { id: 'kilo', cliId: 'kilo', name: 'Kilo Code', tier: 'first-class', projectPath: '.kilocode/skills', globalPath: '~/.kilocode/skills', note: 'Skills CLI compatibility mapping may differ from current Kilo discovery paths; verify project discovery after install.' },
  { id: 'kiro-cli', cliId: 'kiro-cli', name: 'Kiro', tier: 'first-class', projectPath: '.kiro/skills', globalPath: '~/.kiro/skills', note: 'Custom Kiro agents must expose skill://.kiro/skills/*/SKILL.md in resources.' },
  { id: 'roo', cliId: 'roo', name: 'Roo Code', tier: 'first-class', projectPath: '.roo/skills', globalPath: '~/.roo/skills' },
  { id: 'windsurf', cliId: 'windsurf', name: 'Windsurf', tier: 'first-class', projectPath: '.windsurf/skills', globalPath: '~/.codeium/windsurf/skills' },
  { id: 'qwen-code', cliId: 'qwen-code', name: 'Qwen Code', tier: 'extended', projectPath: '.qwen/skills', globalPath: '~/.qwen/skills' },
  { id: 'goose', cliId: 'goose', name: 'Goose', tier: 'extended', projectPath: '.goose/skills', globalPath: '~/.config/goose/skills' },
  { id: 'openhands', cliId: 'openhands', name: 'OpenHands', tier: 'extended', projectPath: '.openhands/skills', globalPath: '~/.openhands/skills' },
];

export const firstClassProviders = providers.filter((provider) => provider.tier === 'first-class');
export const extendedProviders = providers.filter((provider) => provider.tier === 'extended');

export function installCommand(providerId?: string) {
  if (!providerId) return 'npx skills add tph-kds/PlanOnce --all';
  return `npx skills add tph-kds/PlanOnce --skill '*' -a ${providerId} -y`;
}
