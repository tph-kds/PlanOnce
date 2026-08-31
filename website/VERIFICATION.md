# Website verification

This website source is synchronized to PlanOnce v0.7.0 and packaged as canonical Astro + TypeScript + MDX + CSS source only.

## Verified in the packaging environment

- source validator: PASS
- website version/content synchronization: PASS
- 14-provider website matrix matches the PlanOnce v0.7 provider registry: PASS
- MDX frontmatter and TOC heading ids across 8 documentation pages: PASS
- TypeScript data modules compile with the available TypeScript compiler: PASS
- CSS brace structure across global/landing/docs styles: PASS
- stale v0.6 and legacy signal-lime token scan: PASS
- normal/light/dark moon-orbit logo assets present: PASS
- canonical generated HTML in source: 0 files

## Build gate

The canonical publication gate is:

```bash
npm install
npm run validate
npm run check
npm run build
npm run preview
```

In the packaging environment, `npm install` could not complete within the network timeout, so a dependency-backed Astro build is not claimed here. Generated `dist/` HTML is intentionally not included in the source ZIP.
