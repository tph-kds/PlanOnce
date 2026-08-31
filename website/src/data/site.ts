export const site = {
  name: 'PlanOnce',
  version: '0.7.0',
  description: 'Open-source production engineering control for building high-quality software with any AI coding agent.',
  install: 'npx skills add <owner>/planonce-agent-skills --all',
};

export const agents = [
  'Claude Code',
  'Codex',
  'OpenCode',
  'Kilo Code',
  'Kiro',
  'Roo Code',
  'Windsurf',
  'Cursor',
  'Gemini CLI',
  'GitHub Copilot',
  'Cline',
];

export const workflows = [
  { name: 'Greenfield small', skill: 'planonce-green-small', when: 'A narrow new feature with low coordination risk.', flow: ['context','micro-plan','approve','build','verify'] },
  { name: 'Greenfield normal', skill: 'planonce-green-normal', when: 'The default for scoped new product work.', flow: ['shape','approve','digest','waves','review'] },
  { name: 'Greenfield large', skill: 'planonce-green-large', when: 'Architecture-heavy or multi-phase new work.', flow: ['design','approve','digest','phases','readiness'] },
  { name: 'Brownfield small', skill: 'planonce-brown-small', when: 'A contained fix in an existing system.', flow: ['inspect','micro-plan','patch','regress','ship'] },
  { name: 'Brownfield normal', skill: 'planonce-brown-normal', when: 'The default for changing existing behavior.', flow: ['inspect','plan','digest','waves','review'] },
  { name: 'Brownfield large', skill: 'planonce-brown-large', when: 'Risky migrations, auth, APIs, or high-impact changes.', flow: ['map','design','approve','phases','readiness'] }
];

export const reliabilityControls = [
  { label: 'Route safely', name: 'planonce-task', copy: 'Select the smallest safe Greenfield/Brownfield workflow without becoming a second planner.' },
  { label: 'Freeze intent', name: 'Plan fingerprint', copy: 'Normal and Large plans receive a deterministic SHA-256 after human approval.' },
  { label: 'Prove freshness', name: 'Revision-bound evidence', copy: 'Verification binds to Git revision, relevant worktree state, and the accepted plan digest.' },
  { label: 'Recover correctly', name: 'Failure routing', copy: 'Separate implementation defects from plan contradictions with FIX_REVERIFY, BLOCKED_AMEND, and DIAGNOSE.' },
  { label: 'Protect the workspace', name: 'Snapshot + locks', copy: 'Preserve user changes, prefer isolation for high-risk work, and coordinate overlapping workers with optional scope locks.' },
  { label: 'Measure the framework', name: 'Executable evals', copy: 'Run deterministic workflow evals in the release gate and use the same adapter protocol for real coding agents.' },
];

export const qualitySkills = [
  { skill: 'planonce-security', label: 'Security scan', copy: 'Review diffs or codebases, classify findings, and recommend evidence-backed fixes.' },
  { skill: 'planonce-security-fix', label: 'Finding-scoped fix', copy: 'Fix one validated finding, then rerun correctness and security evidence.' },
  { skill: 'planonce-review', label: 'Production review', copy: 'Assess correctness, fresh evidence, operations, backlog, and ship readiness.' },
  { skill: 'planonce-skill-audit', label: 'Skill supply-chain audit', copy: 'Inspect external skills, plugins, hooks, scripts, and remote dependencies before trust.' }
];

export const projectFacts = [
  ['12', 'Agent Skills'],
  ['6', 'delivery workflows'],
  ['14', 'tracked provider targets'],
  ['7', 'deterministic runtime evals'],
];
