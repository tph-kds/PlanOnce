export type ProviderBrand = {
  id: string;
  name: string;
  sourceUrl: string;
  sourceType: 'official' | 'simple-icons' | 'compatibility-glyph';
  licenseOrTrademarkNote: string;
  lightAsset: string;
  darkAsset: string;
  preserveBrandColors: boolean;
};

const brand = (id: string, name: string, sourceUrl: string, preserveBrandColors = true, sourceType: ProviderBrand['sourceType'] = 'compatibility-glyph', note?: string): ProviderBrand => ({
  id,
  name,
  sourceUrl,
  sourceType,
  licenseOrTrademarkNote: note ?? 'Local compatibility glyph; provider name/trademark belongs to its respective owner. Replace only with an approved official asset.',
  lightAsset: `/providers/${id}/mark-light.svg`,
  darkAsset: `/providers/${id}/mark-dark.svg`,
  preserveBrandColors,
});

export const providerBrands: Record<string, ProviderBrand> = Object.fromEntries([
  brand('claude-code', 'Claude Code', 'https://www.anthropic.com/', true, 'simple-icons', 'Anthropic A glyph path from Simple Icons (CC0) rendered as brand card; trademark belongs to Anthropic.'),
  brand('codex', 'Codex', 'https://openai.com/codex/', true, 'simple-icons', 'OpenAI spiral path from Simple Icons (CC0) rendered as brand card; trademark belongs to OpenAI.'),
  brand('opencode', 'OpenCode', 'https://opencode.ai/', true, 'compatibility-glyph', 'High-fidelity compatibility mark (terminal) authored for PlanOnce; Opencode trademark belongs to its owner.'),
  brand('cursor', 'Cursor', 'https://cursor.com/', true, 'compatibility-glyph', 'High-fidelity cursor mark authored for PlanOnce; Cursor trademark belongs to its owner.'),
  brand('gemini-cli', 'Gemini CLI', 'https://github.com/google-gemini/gemini-cli', true, 'simple-icons', 'Google Gemini sparkle path from Simple Icons (CC0); trademark belongs to Google.'),
  brand('github-copilot', 'GitHub Copilot', 'https://github.com/features/copilot', true, 'simple-icons', 'GitHub Copilot path from Simple Icons (CC0); trademark belongs to GitHub/Microsoft.'),
  brand('cline', 'Cline', 'https://cline.bot/', true, 'compatibility-glyph', 'High-fidelity hexagon-C mark authored for PlanOnce; Cline trademark belongs to its owner.'),
  brand('kilo', 'Kilo Code', 'https://kilo.ai/', true, 'compatibility-glyph', 'High-fidelity K mark authored for PlanOnce; Kilo trademark belongs to its owner.'),
  brand('kiro-cli', 'Kiro', 'https://kiro.dev/', true, 'compatibility-glyph', 'High-fidelity mountain/bell mark authored for PlanOnce; Kiro trademark belongs to its owner.'),
  brand('roo', 'Roo Code', 'https://roocode.com/', true, 'compatibility-glyph', 'High-fidelity kangaroo mark authored for PlanOnce; Roo Code trademark belongs to its owner.'),
  brand('windsurf', 'Windsurf', 'https://windsurf.com/', true, 'simple-icons', 'Windsurf wave path from Simple Icons (CC0); trademark belongs to Windsurf.'),
  brand('qwen-code', 'Qwen Code', 'https://github.com/QwenLM/qwen-code', true, 'compatibility-glyph', 'High-fidelity Q mark authored for PlanOnce; Qwen trademark belongs to Alibaba.'),
  brand('goose', 'Goose', 'https://block.github.io/goose/', true, 'compatibility-glyph', 'High-fidelity goose mark authored for PlanOnce; Goose trademark belongs to Block.'),
  brand('openhands', 'OpenHands', 'https://www.all-hands.dev/', true, 'compatibility-glyph', 'High-fidelity hand mark authored for PlanOnce; OpenHands trademark belongs to its owner.'),
].map((entry) => [entry.id, entry]));
