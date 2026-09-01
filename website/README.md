# PlanOnce website

Astro + TypeScript + MDX website for **PlanOnce v1.0.0**, modernized around the design principle:

> **Orbital engineering. Calm control. Evidence in motion.**

The implementation stays static-first and deliberately avoids React islands for animation. Motion is supplied by `motion/mini`, Astro `ClientRouter`, handwritten CSS, and lifecycle-safe `astro:page-load` setup.

## What changed

- canonical standalone release snapshot in `project-metadata.json` + generated `src/data/release.generated.ts`;
- 14 generated provider records and 11 first-class adapters;
- local theme-safe provider SVG assets under `public/providers/` with a third-party trademark policy;
- `ProviderLogo` + static constellation + accessible gentle ticker, with no runtime provider logo CDN;
- moon-orbit hero state diagram, evidence/control-loop storytelling, workflow lanes, reliability failure routing, animated counters, selective border beam, icon-based copy/star/theme controls;
- Astro `ClientRouter` with idempotent `astro:page-load` initialization and `astro:after-swap` theme restoration;
- grouped docs IA: START / CORE CONCEPTS / OPERATIONS / REFERENCE;
- breadcrumbs, previous/next, mobile docs dialog, Edit-on-GitHub, TOC scrollspy, search categories, and new Artifacts / Evals / Troubleshooting pages;
- global reduced-motion contract and responsive behavior down to 390px.

## Development

```bash
npm ci
npm run validate
npm run check
npm run build
npm run dev
```

Validation is intentionally layered:

```bash
npm run check:release
npm run check:modernization
node scripts/validate-source.mjs
```

`npm run sync:metadata` regenerates release facts from the standalone snapshot and, when this folder lives inside the full repository, can also observe root `VERSION` / `RELEASE_MANIFEST.json`.

## Provider assets

`public/providers/**/mark-light.svg` and `mark-dark.svg` are PlanOnce-authored **compatibility glyphs**, not copies of provider trademark artwork. Provider names and trademarks remain property of their respective owners. See `public/providers/THIRD_PARTY_BRANDS.md`.

If approved official assets are later supplied, keep the same local component/metadata contract and update `src/data/provider-brands.ts` instead of reintroducing runtime logo CDNs.

## Architecture

```text
src/components/       Astro UI primitives and product visualizations
src/data/             release/provider/search source-of-truth snapshots
src/layouts/          BaseLayout + grouped DocsLayout
src/motion/           semantic motion tokens
src/scripts/          lifecycle-safe browser setup
src/pages/docs/       MDX documentation
src/styles/           global / landing / docs / motion CSS
public/providers/     local provider compatibility assets
scripts/              release sync + source/modernization validators
```

The quality target is **quietly sophisticated, not loudly animated**.
