import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (rel) => fs.readFileSync(path.join(root, rel), 'utf8');
const exists = (rel) => fs.existsSync(path.join(root, rel));
const failures = [];
const expect = (condition, message) => { if (!condition) failures.push(message); };

const required = [
  'src/components/Icon.astro',
  'src/components/ProviderLogo.astro',
  'src/components/ProviderConstellation.astro',
  'src/components/ProviderTicker.astro',
  'src/components/AnimatedCounter.astro',
  'src/components/BorderBeam.astro',
  'src/components/DocsBreadcrumbs.astro',
  'src/components/DocsMobileNav.astro',
  'src/components/HeadingAnchor.astro',
  'src/motion/theme.ts',
  'src/scripts/app.ts',
  'src/scripts/theme.ts',
  'src/scripts/motion.ts',
  'src/scripts/search.ts',
  'src/scripts/providers.ts',
  'src/data/release.generated.ts',
  'src/data/providers.generated.ts',
  'src/data/provider-brands.ts',
  'scripts/sync-project-metadata.mjs',
  'scripts/check-release-sync.mjs',
  'src/pages/docs/artifacts.mdx',
  'src/pages/docs/evals.mdx',
  'src/pages/docs/troubleshooting.mdx',
  'public/providers/THIRD_PARTY_BRANDS.md',
];
for (const rel of required) expect(exists(rel), `missing ${rel}`);

const packageJson = JSON.parse(read('package.json'));
expect(packageJson.version === '1.0.0', 'package version must be 1.0.0');
expect(packageJson.dependencies?.motion === '13.1.1', 'Motion must be pinned to 13.1.1');
expect(Boolean(packageJson.scripts?.['check:release']), 'check:release script missing');
expect(Boolean(packageJson.scripts?.['check:modernization']), 'check:modernization script missing');

const sourceFiles = [];
const walk = (dir) => {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['node_modules', 'dist', '.astro'].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else sourceFiles.push(full);
  }
};
walk(root);
const runtimeSources = sourceFiles
  .filter((file) => /\.(astro|ts|tsx|js|mjs|mdx|css)$/.test(file))
  .filter((file) => !file.endsWith('modernization-contract.mjs'));
const runtimeText = runtimeSources.map((file) => fs.readFileSync(file, 'utf8')).join('\n');
expect(!/cdn\.simpleicons\.org|cdn\.jsdelivr\.net\/npm\/simple-icons/.test(runtimeText), 'runtime provider CDN URL remains');
expect(!/logo-fallback[\s\S]{0,100}\b(GO|OH|KI|RO)\b/.test(runtimeText), 'visible two-letter provider fallback remains');
expect(!runtimeText.includes('providers.slice(0,3)'), 'provider filler duplication remains');

if (exists('src/layouts/BaseLayout.astro')) {
  const base = read('src/layouts/BaseLayout.astro');
  expect(base.includes('ClientRouter'), 'ClientRouter missing');
  expect(base.includes('astro:page-load'), 'astro:page-load lifecycle missing');
  expect(base.includes('astro:after-swap'), 'astro:after-swap theme lifecycle missing');
}
if (exists('src/scripts/search.ts')) {
  const search = read('src/scripts/search.ts');
  for (const key of ['ArrowDown', 'ArrowUp', 'Enter']) expect(search.includes(key), `search keyboard behavior missing: ${key}`);
}
if (exists('src/scripts/providers.ts')) {
  const providerScript = read('src/scripts/providers.ts');
  for (const key of ['ArrowRight', 'ArrowLeft', 'Home', 'End']) expect(providerScript.includes(key), `provider tab keyboard behavior missing: ${key}`);
}
if (exists('src/scripts/app.ts')) {
  const app = read('src/scripts/app.ts');
  expect(app.includes('setupHeadingAnchors'), 'docs heading-anchor setup missing');
}

if (exists('src/scripts/motion.ts')) {
  const motion = read('src/scripts/motion.ts');
  expect(motion.includes("from 'motion/mini'") || motion.includes('from "motion/mini"'), 'Motion mini import missing');
  expect(!/\beasing\s*:/.test(motion), 'Motion animate options must use ease, not easing');
}

if (exists('src/layouts/DocsLayout.astro')) {
  const docs = read('src/layouts/DocsLayout.astro');
  for (const section of ['START', 'CORE CONCEPTS', 'OPERATIONS', 'REFERENCE']) {
    expect(docs.includes(section), `docs IA group missing: ${section}`);
  }
  for (const feature of ['DocsBreadcrumbs', 'DocsMobileNav', 'Previous', 'Next']) {
    expect(docs.includes(feature), `docs feature missing: ${feature}`);
  }
}

const providerIds = [
  'claude-code', 'codex', 'opencode', 'cursor', 'gemini-cli', 'github-copilot',
  'cline', 'kilo', 'kiro-cli', 'roo', 'windsurf', 'qwen-code', 'goose', 'openhands'
];
for (const id of providerIds) {
  expect(exists(`public/providers/${id}/mark-light.svg`), `missing light provider asset: ${id}`);
  expect(exists(`public/providers/${id}/mark-dark.svg`), `missing dark provider asset: ${id}`);
}

if (exists('src/styles/motion.css')) {
  const css = read('src/styles/motion.css');
  expect(css.includes('prefers-reduced-motion: reduce'), 'global reduced-motion contract missing');
  expect(css.includes('conic-gradient'), 'border-beam implementation missing');
}

if (failures.length) {
  console.error(`Modernization contract: FAIL (${failures.length})`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}
console.log('Modernization contract: PASS');
console.log('Provider assets: 14 light + 14 dark local SVGs');
console.log('Motion + ClientRouter lifecycle contract: PASS');
console.log('Docs IA + new reference pages contract: PASS');
console.log('Version + release source contract: PASS');
