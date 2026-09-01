const base = import.meta.env.BASE_URL;
export const searchIndex = [
  { category: 'Docs', title: 'Overview', href: `${base}docs/`, text: 'PlanOnce v1.0, core contract, project state, and documentation map.' },
  { category: 'Docs', title: 'Getting Started', href: `${base}docs/getting-started/`, text: 'Install, verify, use planonce-task, and complete the one approval moment.' },
  { category: 'Workflow', title: 'Workflows', href: `${base}docs/workflows/`, text: 'Greenfield and Brownfield Small, Normal, and Large routes.' },
  { category: 'Workflow', title: 'Reliability Layer', href: `${base}docs/reliability/`, text: 'Plan fingerprints, revision-bound evidence, failure routing, workspace safety, and evals.' },
  { category: 'Docs', title: 'Runtime Architecture', href: `${base}docs/architecture/`, text: 'PlanOnce authority, Agent OS standards, GSD execution/audit, and portable skills.' },
  { category: 'Provider', title: 'Providers', href: `${base}docs/providers/`, text: '14 provider targets, exact Skills CLI IDs, paths, and compatibility caveats.' },
  { category: 'Docs', title: 'Security & Review', href: `${base}docs/security-review/`, text: 'Security scan, finding-scoped fixes, readiness review, and supply-chain audit.' },
  { category: 'Reference', title: 'Artifact Schemas', href: `${base}docs/artifacts/`, text: 'CONTEXT, DESIGN, PLAN, STATE, VERIFY, frontmatter, and plan digest relationship.' },
  { category: 'Reference', title: 'Evaluation Harness', href: `${base}docs/evals/`, text: 'Deterministic evals and external-agent adapter protocol.' },
  { category: 'Reference', title: 'Troubleshooting', href: `${base}docs/troubleshooting/`, text: 'Discovery, Kiro, Kilo, stale evidence, worktree, lock, and amendment problems.' },
  { category: 'Reference', title: 'Design System', href: `${base}docs/design-system/`, text: 'Orbital design language, typography, motion theme, provider assets, and accessibility.' },
];
