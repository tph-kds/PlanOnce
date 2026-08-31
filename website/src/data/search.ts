const base = import.meta.env.BASE_URL;
export const searchIndex = [
  { title: 'Overview', href: `${base}docs/`, text: 'PlanOnce v1.0, core contract, project state, and documentation map.' },
  { title: 'Getting started', href: `${base}docs/getting-started/`, text: 'Install PlanOnce, initialize a project, use planonce-task, and run your first controlled change.' },
  { title: 'Workflow guide', href: `${base}docs/workflows/`, text: 'Greenfield and brownfield workflows for small, normal, and large changes, escalation, human gates, and recovery.' },
  { title: 'Reliability layer', href: `${base}docs/reliability/`, text: 'Artifact schemas, plan fingerprints, revision-bound evidence, failure routing, workspace locks, and executable evals.' },
  { title: 'Runtime architecture', href: `${base}docs/architecture/`, text: 'PlanOnce authority, Agent OS v3.0.0, GSD Core v1.12.0 core audit source, state artifacts, and provider-neutral execution.' },
  { title: 'Providers', href: `${base}docs/providers/`, text: 'Claude Code, Codex, OpenCode, Kilo Code, Kiro, Roo Code, Windsurf, Cursor, Gemini CLI, Copilot, Cline, Qwen Code, Goose, OpenHands, and generic runtimes.' },
  { title: 'Security and review', href: `${base}docs/security-review/`, text: 'Security scans, finding-scoped fixes, stale evidence handling, production review, readiness statuses, and skill supply-chain audit.' },
  { title: 'Design system', href: `${base}docs/design-system/`, text: 'Moon-orbit brand system, color hierarchy, layout, motion discipline, logo variants, and accessibility rules.' }
];
