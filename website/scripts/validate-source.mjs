import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (rel) => fs.readFileSync(path.join(root, rel), 'utf8');
const exists = (rel) => fs.existsSync(path.join(root, rel));
const errors = [];
const warnings = [];
const required = [
  'astro.config.mjs','package.json','project-metadata.json','src/pages/index.astro',
  'src/layouts/BaseLayout.astro','src/layouts/DocsLayout.astro','src/styles/global.css',
  'src/styles/landing.css','src/styles/docs.css','src/styles/motion.css','src/data/site.ts',
  'src/data/release.generated.ts','src/data/providers.generated.ts','src/data/provider-brands.ts',
  'src/scripts/app.ts','src/scripts/theme.ts','src/scripts/search.ts','src/scripts/providers.ts','src/scripts/motion.ts',
  'public/llms.txt','public/site.webmanifest','public/providers/THIRD_PARTY_BRANDS.md',
  'src/pages/docs/index.mdx','src/pages/docs/getting-started.mdx','src/pages/docs/workflows.mdx',
  'src/pages/docs/reliability.mdx','src/pages/docs/architecture.mdx','src/pages/docs/providers.mdx',
  'src/pages/docs/security-review.mdx','src/pages/docs/artifacts.mdx','src/pages/docs/evals.mdx',
  'src/pages/docs/troubleshooting.mdx','src/pages/docs/design-system.mdx'
];
for (const rel of required) if (!exists(rel)) errors.push(`Missing required file: ${rel}`);

const allFiles = [];
const walk = (dir) => {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['node_modules','dist','.astro'].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    entry.isDirectory() ? walk(full) : allFiles.push(full);
  }
};
walk(root);
for (const file of allFiles) {
  if (!/\.(astro|mdx|css|ts|mjs|json|txt|svg)$/.test(file)) continue;
  const rel = path.relative(root, file).replace(/\\/g,'/');
  if (rel === 'scripts/validate-source.mjs' || rel === 'scripts/modernization-contract.mjs') continue;
  const text = fs.readFileSync(file, 'utf8');
  if (/\b(TODO|TBD|FIXME)\b/.test(text)) errors.push(`Placeholder token found in ${rel}`);
  if (/cdn\.simpleicons\.org|cdn\.jsdelivr\.net\/npm\/simple-icons/.test(text)) errors.push(`Remote provider logo CDN found in ${rel}`);
}
if (allFiles.some((file) => file.endsWith('.html'))) errors.push('Canonical source contains generated HTML.');

const pkg = JSON.parse(read('package.json'));
if (pkg.version !== '1.0.0') errors.push('Website package version must be 1.0.0.');
if (pkg.dependencies?.astro !== '7.2.9') errors.push('Astro must be pinned to 7.2.9.');
if (pkg.dependencies?.['@astrojs/mdx'] !== '7.0.8') errors.push('@astrojs/mdx must be pinned to 7.0.8.');
if (pkg.dependencies?.motion !== '13.1.1') errors.push('Motion must be pinned to 13.1.1.');
for (const script of ['build','check','validate','check:release','check:modernization']) if (!pkg.scripts?.[script]) errors.push(`Missing npm script: ${script}`);

const providerIds = ['claude-code','codex','opencode','cursor','gemini-cli','github-copilot','cline','kilo','kiro-cli','roo','windsurf','qwen-code','goose','openhands'];
const providers = read('src/data/providers.generated.ts');
for (const id of providerIds) {
  if (!providers.includes(`id: '${id}'`)) errors.push(`Provider registry missing: ${id}`);
  for (const theme of ['light','dark']) if (!exists(`public/providers/${id}/mark-${theme}.svg`)) errors.push(`Provider ${id} missing ${theme} asset.`);
}
if ((providers.match(/\{ id:/g) || []).length !== 14) errors.push('Provider registry must contain exactly 14 providers.');
if ((providers.match(/tier: 'first-class'/g) || []).length !== 11) errors.push('Provider registry must contain exactly 11 first-class providers.');

const base = read('src/layouts/BaseLayout.astro');
for (const token of ['ClientRouter','astro:page-load','astro:after-swap','SoftwareSourceCode']) if (!base.includes(token)) errors.push(`BaseLayout missing ${token}.`);
const app = read('src/scripts/app.ts');
for (const token of ['AbortController','setupTheme','setupSearch','setupProviders','setupMotion']) if (!app.includes(token)) errors.push(`Lifecycle app missing ${token}.`);
const motion = read('src/scripts/motion.ts');
if (!motion.includes("from 'motion/mini'")) errors.push('Motion mini import missing.');
const motionCss = read('src/styles/motion.css');
for (const token of ['prefers-reduced-motion:reduce','conic-gradient','provider-travel','::view-transition-old']) if (!motionCss.replaceAll(' ','').includes(token.replaceAll(' ',''))) errors.push(`Motion CSS missing ${token}.`);

const landing = read('src/pages/index.astro');
for (const token of ['<ProviderConstellation />','<ProviderTicker />','<ReliabilityLoop />','<WorkflowRail />','<ProviderTabs />','<BrandOrbit />','<BorderBeam>','FIX_REVERIFY','BLOCKED_AMEND']) if (!landing.includes(token)) errors.push(`Landing contract missing: ${token}`);
if (landing.includes('ProviderMarquee')) errors.push('Legacy ProviderMarquee remains on landing.');
if (!landing.includes('site.install')) errors.push('Landing install command is not sourced from site data.');

const docsLayout = read('src/layouts/DocsLayout.astro');
for (const token of ['START','CORE CONCEPTS','OPERATIONS','REFERENCE','DocsBreadcrumbs','DocsMobileNav','Previous','Next','Edit on GitHub']) if (!docsLayout.includes(token)) errors.push(`Docs layout missing ${token}.`);
for (const file of allFiles.filter((file) => file.endsWith('.mdx'))) {
  const rel = path.relative(root, file).replace(/\\/g, '/');
  const text = fs.readFileSync(file, 'utf8');
  if (/\]\(\/docs\//.test(text) || /^\s*href:\s*\/docs\//m.test(text)) {
    errors.push(`Base-unsafe /docs/ link found in ${rel}`);
  }
}

for (const rel of required.filter((rel) => rel.endsWith('.mdx'))) {
  const text = read(rel);
  if (!text.startsWith('---\n')) errors.push(`Missing frontmatter in ${rel}`);
  if (!text.includes('layout: ../../layouts/DocsLayout.astro')) errors.push(`DocsLayout missing in ${rel}`);
  if (!text.includes('description:')) errors.push(`Description missing in ${rel}`);
  if (!text.includes('toc:')) errors.push(`TOC metadata missing in ${rel}`);
}

const reliability = read('src/pages/docs/reliability.mdx');
for (const token of ['planonce.state/v1','approved_plan_digest','FIX_REVERIFY','BLOCKED_AMEND','DIAGNOSE','.planonce/locks/','Executable evals']) if (!reliability.includes(token)) errors.push(`Reliability docs missing: ${token}`);
const artifacts = read('src/pages/docs/artifacts.mdx');
for (const token of ['CONTEXT.md','DESIGN.md','PLAN.md','STATE.md','VERIFY.md','SHA-256']) if (!artifacts.includes(token)) errors.push(`Artifact docs missing: ${token}`);

const globalCss = read('src/styles/global.css');
if (globalCss.includes('Playfair')) errors.push('Playfair remains in production typography after simplification.');
if (!globalCss.includes('--cyan:') || !globalCss.includes('--violet:')) errors.push('Orbital color tokens missing.');
if (!globalCss.includes(':focus-visible')) errors.push('Focus-visible styling missing.');

const manifest = JSON.parse(read('public/site.webmanifest'));
if (manifest.name !== 'PlanOnce') errors.push('Web manifest name mismatch.');

const stale = allFiles.filter((file) => /\.(astro|mdx|ts|txt|md)$/.test(file)).filter((file) => !file.endsWith('modernization-contract.mjs')).filter((file) => /PlanOnce v0\.[0-9]\.0|v0\.[0-9]\b/.test(fs.readFileSync(file,'utf8')));
for (const file of stale) errors.push(`Stale pre-v1.0 release copy found in ${path.relative(root,file)}`);

if (errors.length) {
  console.error(`PlanOnce website source validation: FAIL (${errors.length})`);
  errors.forEach((error) => console.error(`- ${error}`));
  warnings.forEach((warning) => console.error(`- warning: ${warning}`));
  process.exit(1);
}
console.log('PlanOnce website source validation: PASS');
console.log(`Checked ${allFiles.length} source/public files.`);
console.log('Release v1.0.0 + generated facts: PASS');
console.log('Provider matrix 14 / first-class 11 + local assets: PASS');
console.log('ClientRouter + lifecycle-safe scripts + Motion mini: PASS');
console.log('Grouped docs IA + Artifacts/Evals/Troubleshooting: PASS');
console.log('Reduced motion + no legacy provider CDN/marquee: PASS');
