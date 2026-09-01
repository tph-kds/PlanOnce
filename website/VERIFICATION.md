# Website verification

This source package targets the PlanOnce **v1.0.0** website contract and is structured for deterministic, static-first validation.

## Release-source gate — no install required

The final ZIP can be validated immediately with Node.js, before installing dependencies:

```bash
npm run validate
```

That gate combines:

1. release/source-of-truth synchronization;
2. source architecture/content checks;
3. local provider-asset coverage and no provider-logo CDN runtime dependency;
4. base-path-safe documentation links for the `/PlanOnce/` GitHub Pages deployment;
5. ClientRouter lifecycle + Motion mini contracts;
6. keyboard contracts for search/provider tabs;
7. grouped docs IA, reference pages, reduced-motion and interaction contracts.

## Full compiler gates

In a normal network-enabled development environment:

```bash
npm ci
npm run check
npm run build
```

`node_modules/`, `.astro/`, and `dist/` are intentionally excluded from the release source ZIP. The committed `package-lock.json` is the reproducible dependency authority.

## Release facts

- 12 Agent Skills
- 6 delivery workflows
- 14 provider targets
- 11 first-class adapters
- 7 deterministic evals
- Agent OS 3.0.0
- GSD Core 1.12.0

## Visual QA targets

Capture landing/provider/workflow/reliability/docs/mobile-nav states at 1920, 1440, 1280, 1024, 768, and 390 pixels in light/dark themes; include reduced-motion states at 1440, 768, and 390.

No horizontal overflow is acceptable. Reduced motion must freeze ticker/orbit/border beam/path drawing and expose final counter values immediately.
