export type ProviderTier = 'first-class' | 'extended';

export type Provider = {
  id: string;
  name: string;
  tier: ProviderTier;
  projectPath: string;
  globalPath: string;
  note?: string;
};

export const providers: Provider[] = [
  { id: 'claude-code', name: 'Claude Code', tier: 'first-class', projectPath: '.claude/skills', globalPath: '~/.claude/skills' },
  { id: 'codex', name: 'Codex', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.codex/skills' },
  { id: 'opencode', name: 'OpenCode', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.config/opencode/skills', note: 'OpenCode also discovers .opencode/skills and .claude/skills at project scope.' },
  { id: 'cursor', name: 'Cursor', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.cursor/skills' },
  { id: 'gemini-cli', name: 'Gemini CLI', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.gemini/skills' },
  { id: 'github-copilot', name: 'GitHub Copilot', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.copilot/skills' },
  { id: 'cline', name: 'Cline', tier: 'first-class', projectPath: '.agents/skills', globalPath: '~/.agents/skills' },
  { id: 'kilo', name: 'Kilo Code', tier: 'first-class', projectPath: '.kilocode/skills', globalPath: '~/.kilocode/skills', note: 'Current Skills CLI mapping is legacy .kilocode/skills; current Kilo docs prefer .kilo/skills and also support .agents/skills. Verify discovery after install.' },
  { id: 'kiro-cli', name: 'Kiro', tier: 'first-class', projectPath: '.kiro/skills', globalPath: '~/.kiro/skills', note: 'Default Kiro agents discover skills automatically. Custom agents must expose skill://.kiro/skills/*/SKILL.md in resources.' },
  { id: 'roo', name: 'Roo Code', tier: 'first-class', projectPath: '.roo/skills', globalPath: '~/.roo/skills' },
  { id: 'windsurf', name: 'Windsurf', tier: 'first-class', projectPath: '.windsurf/skills', globalPath: '~/.codeium/windsurf/skills' },
  { id: 'qwen-code', name: 'Qwen Code', tier: 'extended', projectPath: '.qwen/skills', globalPath: '~/.qwen/skills' },
  { id: 'goose', name: 'Goose', tier: 'extended', projectPath: '.goose/skills', globalPath: '~/.config/goose/skills' },
  { id: 'openhands', name: 'OpenHands', tier: 'extended', projectPath: '.openhands/skills', globalPath: '~/.openhands/skills' },
];

export const firstClassProviders = providers.filter((provider) => provider.tier === 'first-class');

export function installCommand(providerId?: string) {
  if (!providerId) return 'npx skills add <owner>/planonce-agent-skills --all';
  return `npx skills add <owner>/planonce-agent-skills --skill '*' -a ${providerId} -y`;
}

export const allFirstClassCommand = [
  'npx skills add <owner>/planonce-agent-skills',
  "--skill '*'",
  ...firstClassProviders.flatMap((provider) => ['-a', provider.id]),
  '-y',
].join(' ');
