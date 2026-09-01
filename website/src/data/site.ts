import { release, releaseFacts } from './release.generated';

export const site = {
  name: 'PlanOnce',
  version: release.version,
  description: 'Open-source production engineering control for building high-quality software with any AI coding agent.',
  install: 'npx skills add tph-kds/PlanOnce --all',
};

export const agents = [
  'Claude Code', 'Codex', 'OpenCode', 'Kilo Code', 'Kiro', 'Roo Code',
  'Windsurf', 'Cursor', 'Gemini CLI', 'GitHub Copilot', 'Cline',
];

export const workflows = [
  { name: 'Greenfield small', lane: 'greenfield', size: 'Small', skill: 'planonce-green-small', when: 'A narrow new feature with low coordination risk.', gate: 'micro-plan approval', artifacts: 'CONTEXT → PLAN → VERIFY', flow: ['context','micro-plan','approve','build','verify'] },
  { name: 'Greenfield normal', lane: 'greenfield', size: 'Normal', skill: 'planonce-green-normal', when: 'The default for scoped new product work.', gate: 'accepted plan digest', artifacts: 'CONTEXT → DESIGN → PLAN → STATE → VERIFY', flow: ['shape','approve','digest','waves','review'] },
  { name: 'Greenfield large', lane: 'greenfield', size: 'Large', skill: 'planonce-green-large', when: 'Architecture-heavy or multi-phase new work.', gate: 'design + plan approval', artifacts: 'CONTEXT → DESIGN → PLAN → STATE → VERIFY', flow: ['design','approve','digest','phases','readiness'] },
  { name: 'Brownfield small', lane: 'brownfield', size: 'Small', skill: 'planonce-brown-small', when: 'A contained fix in an existing system.', gate: 'scope + regression intent', artifacts: 'CONTEXT → PLAN → VERIFY', flow: ['inspect','micro-plan','patch','regress','ship'] },
  { name: 'Brownfield normal', lane: 'brownfield', size: 'Normal', skill: 'planonce-brown-normal', when: 'The default for changing existing behavior.', gate: 'accepted plan digest', artifacts: 'CONTEXT → DESIGN → PLAN → STATE → VERIFY', flow: ['inspect','plan','digest','waves','review'] },
  { name: 'Brownfield large', lane: 'brownfield', size: 'Large', skill: 'planonce-brown-large', when: 'Risky migrations, auth, APIs, or high-impact changes.', gate: 'design + readiness approval', artifacts: 'CONTEXT → DESIGN → PLAN → STATE → VERIFY', flow: ['map','design','approve','phases','readiness'] }
];

export const reliabilityControls = [
  { label: 'Route', name: 'planonce-task', copy: 'Select the smallest safe Greenfield/Brownfield workflow without becoming a second planner.' },
  { label: 'Freeze intent', name: 'Plan fingerprint', copy: 'Normal and Large plans receive a deterministic SHA-256 after human approval.' },
  { label: 'Execute safely', name: 'Workspace safety', copy: 'Preserve user changes, isolate high-risk work, and coordinate overlapping scopes.' },
  { label: 'Prove freshness', name: 'Revision-bound evidence', copy: 'Verification binds to revision, relevant worktree state, and the accepted plan digest.' },
  { label: 'Recover correctly', name: 'Failure routing', copy: 'Defects take FIX_REVERIFY; plan contradictions take BLOCKED_AMEND; uncertainty takes DIAGNOSE.' },
  { label: 'Review', name: 'Executable evals', copy: 'Fresh evidence and deterministic evals feed production review rather than marketing confidence.' },
];

export const qualitySkills = [
  { skill: 'planonce-security', label: 'Security scan', copy: 'Review diffs or codebases, classify findings, and recommend evidence-backed fixes.' },
  { skill: 'planonce-security-fix', label: 'Finding-scoped fix', copy: 'Fix one validated finding, then rerun correctness and security evidence.' },
  { skill: 'planonce-review', label: 'Production review', copy: 'Assess correctness, fresh evidence, operations, backlog, and ship readiness.' },
  { skill: 'planonce-skill-audit', label: 'Skill supply-chain audit', copy: 'Inspect external skills, plugins, hooks, scripts, and remote dependencies before trust.' }
];

export const projectFacts = releaseFacts;
