# PlanOnce Website

Landing page and technical documentation for **PlanOnce v0.7.0 - Workflow Reliability Layer**.

PlanOnce is an open-source framework for building high-quality software with any AI coding agent. This website mirrors the current release concepts: route-only workflow selection, one planning authority, plan fingerprints, revision-bound evidence, failure routing, workspace safety, executable evals, security/readiness gates, pinned Agent OS/GSD upstream engines, and multi-provider installation.

## Stack

- Astro 7.2.9
- TypeScript 6
- MDX
- handwritten modular CSS
- native browser interactions

Canonical source lives under `src/`. Generated HTML belongs only in `dist/` after `npm run build` and is intentionally not committed or packaged.

## Brand

The v0.7 site uses the PlanOnce moon-orbit identity under `public/brand/`:

```text
brand/
├── planonce-logo-primary.png
├── planonce-logo-normal.png
├── planonce-logo-light.png
├── planonce-logo-dark.png
├── planonce-mark-primary.png
├── planonce-mark-normal.png
├── planonce-mark-light.png
└── planonce-mark-dark.png
```

The mark combines a crescent moon, orbit, sequence nodes, and guiding star. Light and dark variants are swapped by theme; the interface keeps live text for the primary brand name for accessibility and rendering quality.

## Local development

```bash
npm install
npm run validate
npm run check
npm run dev
```

Production build:

```bash
npm run build
npm run preview
```

## Documentation routes

```text
/docs/
/docs/getting-started/
/docs/workflows/
/docs/reliability/
/docs/architecture/
/docs/providers/
/docs/security-review/
/docs/design-system/
```

## Provider data

`src/data/providers.ts` mirrors the PlanOnce v0.7 provider matrix with 14 tracked targets: Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot, Cline, Kilo Code, Kiro, Roo Code, Windsurf, Qwen Code, Goose, and OpenHands.

Kilo and Kiro keep explicit caveats because current discovery/install behavior differs from the most portable `.agents/skills` path.

## Publishing hygiene

Do not commit:

- `node_modules/`
- `.astro/`
- `dist/`
- generated static preview folders

The public source should remain Astro + TypeScript + MDX + CSS plus intentional public brand assets.
