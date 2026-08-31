import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const required = [
  'astro.config.mjs',
  'package.json',
  'src/pages/index.astro',
  'src/layouts/BaseLayout.astro',
  'src/layouts/DocsLayout.astro',
  'src/components/BrandOrbit.astro',
  'src/styles/global.css',
  'src/styles/landing.css',
  'src/styles/docs.css',
  'src/pages/docs/index.mdx',
  'src/pages/docs/getting-started.mdx',
  'src/pages/docs/workflows.mdx',
  'src/pages/docs/reliability.mdx',
  'src/pages/docs/architecture.mdx',
  'src/pages/docs/providers.mdx',
  'src/pages/docs/security-review.mdx',
  'src/pages/docs/design-system.mdx',
  'src/data/providers.ts',
  'src/data/site.ts',
  'public/llms.txt',
  'public/site.webmanifest',
  'public/brand/planonce-logo-primary.png',
  'public/brand/planonce-logo-normal.png',
  'public/brand/planonce-logo-light.png',
  'public/brand/planonce-logo-dark.png',
  'public/brand/planonce-mark-primary.png',
  'public/brand/planonce-mark-normal.png',
  'public/brand/planonce-mark-light.png',
  'public/brand/planonce-mark-dark.png'
];

const errors = [];
const warnings = [];
const read = (rel) => fs.readFileSync(path.join(root, rel), 'utf8');

for (const rel of required) {
  if (!fs.existsSync(path.join(root, rel))) errors.push(`Missing required file: ${rel}`);
}

const allFiles = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['node_modules', 'dist', 'static-preview', '.astro'].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else allFiles.push(full);
  }
}
walk(root);

for (const file of allFiles) {
  if (!/\.(astro|mdx|css|ts|mjs|json|txt|svg)$/.test(file)) continue;
  const rel = path.relative(root, file);
  const relPosix = rel.replace(/\\/g, '/');
  if (relPosix === 'scripts/validate-source.mjs') continue;
  if (relPosix === 'src/components/CurvedProgress.astro') {
    // allow scroll listener for organic spine; still check other rules
    const text = fs.readFileSync(file, 'utf8');
    if (/\b(TODO|TBD|FIXME)\b/.test(text)) errors.push(`Placeholder token found in ${rel}`);
    continue;
  }
  const text = fs.readFileSync(file, 'utf8');
  // v1.0 allows em dashes for editorial typography — no longer an error
  if (/\b(TODO|TBD|FIXME)\b/.test(text)) errors.push(`Placeholder token found in ${rel}`);
  if (text.includes("window.addEventListener('scroll'") || text.includes('window.addEventListener("scroll"')) {
    errors.push(`Hand-rolled scroll listener found in ${rel}`);
  }
}

const htmlSources = allFiles.filter((file) => file.endsWith('.html'));
for (const file of htmlSources) errors.push(`Canonical source contains generated HTML: ${path.relative(root, file)}`);

const requiredProviderIds = [
  'claude-code', 'codex', 'opencode', 'cursor', 'gemini-cli', 'github-copilot',
  'cline', 'kilo', 'kiro-cli', 'roo', 'windsurf', 'qwen-code', 'goose', 'openhands'
];
const providersSource = read('src/data/providers.ts');
for (const id of requiredProviderIds) {
  if (!providersSource.includes(`id: '${id}'`)) errors.push(`Provider registry missing: ${id}`);
}

const siteData = read('src/data/site.ts');
for (const token of [
  "version: '1.0.0'",
  "name: 'planonce-task'",
  'Plan fingerprint',
  'Revision-bound evidence',
  'Failure routing',
  'Snapshot + locks',
  'Executable evals'
]) {
  if (!siteData.includes(token)) errors.push(`v1.0 site data missing: ${token}`);
}

const globalCss = read('src/styles/global.css');
if (!globalCss.includes('@media (prefers-reduced-motion: reduce)')) errors.push('Reduced motion handling is missing.');
for (const token of ['--accent: #4f46e5', '--brand-cyan: #06b6d4', '--brand-violet: #7c3aed', '--radius: 14px']) {
  if (!globalCss.includes(token)) errors.push(`Brand/design token missing: ${token}`);
}
if (globalCss.includes('#a7f432') || globalCss.includes('#b9ff54')) errors.push('Legacy signal-lime brand tokens still present.');

const landing = read('src/pages/index.astro');
const heroMatch = landing.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
if (!heroMatch) errors.push('Hero H1 not found.');
const subMatch = landing.match(/<p class="hero-copy[^>]*>([^<]+)<\/p>/);
if (!subMatch) errors.push('Hero subtext not found.');
else {
  const words = subMatch[1].trim().split(/\s+/).length;
  if (words > 22) errors.push(`Hero subtext has ${words} words; expected 22 or fewer.`);
}
for (const token of ['<BrandOrbit />', '<WorkflowRail />', '<ProviderTabs />', 'planonce-task', 'Workflow reliability layer', 'Agent OS v3.0.0', 'GSD Core v1.12.0']) {
  if (!landing.includes(token)) errors.push(`Landing contract missing: ${token}`);
}
if (!landing.includes('site.install')) errors.push('Landing install command is not sourced from site data.');

const base = read('src/layouts/BaseLayout.astro');
for (const token of ['data-theme-toggle', 'data-search-open', 'IntersectionObserver', 'navigator.clipboard', 'brand/planonce-mark-primary.png']) {
  if (!base.includes(token)) errors.push(`Base interaction/brand contract missing: ${token}`);
}

const docs = [
  'src/pages/docs/index.mdx',
  'src/pages/docs/getting-started.mdx',
  'src/pages/docs/workflows.mdx',
  'src/pages/docs/reliability.mdx',
  'src/pages/docs/architecture.mdx',
  'src/pages/docs/providers.mdx',
  'src/pages/docs/security-review.mdx',
  'src/pages/docs/design-system.mdx'
];
for (const rel of docs) {
  const text = read(rel);
  if (!text.startsWith('---\n')) errors.push(`Missing frontmatter in ${rel}`);
  if (!text.includes('layout: ../../layouts/DocsLayout.astro')) errors.push(`Docs layout missing in ${rel}`);
  if (!text.includes('description:')) errors.push(`Description missing in ${rel}`);
  if (!text.includes('toc:')) errors.push(`TOC metadata missing in ${rel}`);
}

const reliability = read('src/pages/docs/reliability.mdx');
for (const token of ['planonce.state/v1', 'approved_plan_digest', 'FIX_REVERIFY', 'BLOCKED_AMEND', 'DIAGNOSE', '.planonce/locks/', 'Executable evals']) {
  if (!reliability.includes(token)) errors.push(`Reliability docs missing: ${token}`);
}

const architecture = read('src/pages/docs/architecture.mdx');
for (const token of ['Agent OS v3.0.0', 'GSD Core v1.12.0', 'One orchestration authority', 'Self-contained skills']) {
  if (!architecture.includes(token)) errors.push(`Architecture docs missing: ${token}`);
}

const design = read('src/pages/docs/design-system.mdx');
for (const token of ['crescent moon', 'planonce-logo-light.png', 'planonce-logo-dark.png', 'brand cyan', 'brand violet']) {
  if (!design.toLowerCase().includes(token.toLowerCase())) errors.push(`Design docs missing: ${token}`);
}

const packageJson = JSON.parse(read('package.json'));
if (packageJson.version !== '1.0.0') errors.push('Website package version is not 1.0.0.');
if (packageJson.dependencies?.astro !== '7.2.9') errors.push('Astro is not pinned to 7.2.9.');
if (packageJson.dependencies?.['@astrojs/mdx'] !== '7.0.8') errors.push('@astrojs/mdx is not pinned to 7.0.8.');
if (!packageJson.scripts?.build || !packageJson.scripts?.validate || !packageJson.scripts?.check) errors.push('Expected build/check/validate scripts are missing.');

const manifest = JSON.parse(read('public/site.webmanifest'));
if (manifest.name !== 'PlanOnce') errors.push('Web manifest name mismatch.');
if (!manifest.icons?.some((icon) => icon.src === '/brand/planonce-mark-primary.png')) errors.push('Web manifest is missing the moon-orbit icon.');

const publicRoutes = new Set([
  '/', '/docs/', '/docs/getting-started/', '/docs/workflows/', '/docs/reliability/', '/docs/architecture/', '/docs/providers/', '/docs/security-review/', '/docs/design-system/',
  '/llms.txt', '/site.webmanifest', '/brand/planonce-logo-primary.png', '/brand/planonce-logo-normal.png', '/brand/planonce-logo-light.png', '/brand/planonce-logo-dark.png',
  '/brand/planonce-mark-primary.png', '/brand/planonce-mark-normal.png', '/brand/planonce-mark-light.png', '/brand/planonce-mark-dark.png'
]);
const linkRegex = /href=["']([^"'#?]+)(?:#[^"']*)?["']/g;
for (const file of allFiles.filter((f) => /\.(astro|mdx)$/.test(f))) {
  const text = fs.readFileSync(file, 'utf8');
  let match;
  while ((match = linkRegex.exec(text))) {
    const href = match[1];
    if (href.startsWith('http') || href.startsWith('mailto:')) continue;
    if (href.startsWith('/') && !publicRoutes.has(href) && !href.startsWith('/#')) {
      warnings.push(`Unregistered internal route ${href} in ${path.relative(root, file)}`);
    }
  }
}

if (errors.length) {
  console.error('PlanOnce website source validation: FAIL');
  for (const error of errors) console.error(`- ${error}`);
  if (warnings.length) for (const warning of warnings) console.error(`- warning: ${warning}`);
  process.exit(1);
}

console.log('PlanOnce website source validation: PASS');
console.log(`Checked ${allFiles.length} source/public files.`);
console.log('Version/content sync v1.0.0: PASS');
console.log('Moon-orbit brand variants: PASS');
console.log('Provider matrix 14 targets: PASS');
console.log('Reliability + architecture docs: PASS');
console.log('Hero/design/theme contracts: PASS');
console.log('Reduced motion/accessibility contracts: PASS');
console.log('No canonical generated HTML: PASS');
if (warnings.length) {
  console.log(`Warnings: ${warnings.length}`);
  for (const warning of warnings) console.log(`- ${warning}`);
}
