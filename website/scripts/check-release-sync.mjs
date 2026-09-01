import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (rel) => fs.readFileSync(path.join(root, rel), 'utf8');
const meta = JSON.parse(read('project-metadata.json'));
const pkg = JSON.parse(read('package.json'));
const release = read('src/data/release.generated.ts');
const providers = read('src/data/providers.generated.ts');
const failures = [];
const expect = (ok, message) => { if (!ok) failures.push(message); };

expect(pkg.version === meta.version, `package version ${pkg.version} != snapshot ${meta.version}`);
expect(release.includes(`version: '${meta.version}'`) || release.includes(`version: \"${meta.version}\"`), 'release.generated version drift');
for (const [key, value] of Object.entries({
  skillCount: meta.skillCount,
  workflowCount: meta.workflowCount,
  providerCount: meta.providerCount,
  firstClassProviderCount: meta.firstClassProviderCount,
  evalCount: meta.evalCount,
})) {
  expect(release.includes(`${key}: ${value}`), `release.generated ${key} drift`);
}
expect((providers.match(/\{ id:/g) || []).length === meta.providerCount, 'provider registry count drift');

const parent = path.resolve(root, '..');
const versionPath = path.join(parent, 'VERSION');
const manifestPath = path.join(parent, 'RELEASE_MANIFEST.json');
if (fs.existsSync(versionPath)) {
  expect(fs.readFileSync(versionPath, 'utf8').trim() === meta.version, 'root VERSION drift');
}
if (fs.existsSync(manifestPath)) {
  try {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    const version = manifest.version ?? manifest.release?.version;
    if (version) expect(version === meta.version, 'root RELEASE_MANIFEST version drift');
  } catch {
    failures.push('root RELEASE_MANIFEST.json is not valid JSON');
  }
}

if (failures.length) {
  console.error(`Release/source-of-truth check: FAIL (${failures.length})`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}
console.log(`Release/source-of-truth check: PASS (v${meta.version})`);
console.log(`${meta.providerCount} providers / ${meta.firstClassProviderCount} first-class / ${meta.skillCount} skills / ${meta.evalCount} evals`);
