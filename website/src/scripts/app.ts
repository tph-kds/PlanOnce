import { setupTheme } from './theme';
import { setupSearch } from './search';
import { setupProviders } from './providers';
import { setupMotion } from './motion';
import { setupSmooth } from './smooth';

let controller: AbortController | undefined;

function prefixBaseLinks() {
  const base = import.meta.env.BASE_URL;
  if (base === '/') return;
  document.querySelectorAll<HTMLAnchorElement>('a[href^="/"]').forEach((link) => {
    const href = link.getAttribute('href') || '';
    if (href.startsWith(base) || href.startsWith('//')) return;
    if (/^\/(docs|llms|brand|providers|site\.webmanifest)/.test(href)) link.href = `${base.replace(/\/$/, '')}${href}`;
  });
}

function setupHeadingAnchors(signal: AbortSignal) {
  document.querySelectorAll<HTMLElement>('.docs-content h2[id], .docs-content h3[id]').forEach((heading) => {
    if (heading.querySelector(':scope > .heading-anchor-copy')) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'heading-anchor-copy';
    button.textContent = '#';
    button.setAttribute('aria-label', `Copy link to ${heading.textContent?.trim() || 'section'}`);
    button.setAttribute('data-copy', new URL(`#${heading.id}`, location.href).href);
    heading.append(button);
  });
  signal.addEventListener('abort', () => {}, { once: true });
}

function setupCopy(signal: AbortSignal) {
  document.querySelectorAll<HTMLElement>('[data-copy]').forEach((button) => {
    button.addEventListener('click', async () => {
      const text = button.getAttribute('data-copy') || '';
      try { await navigator.clipboard.writeText(text); button.dataset.copied = 'true'; }
      catch { button.dataset.copied = 'error'; }
      window.setTimeout(() => delete button.dataset.copied, 1400);
    }, { signal });
  });
}

function setupChrome(signal: AbortSignal) {
  const menu = document.querySelector<HTMLElement>('[data-mobile-menu]');
  document.querySelector<HTMLElement>('[data-menu-toggle]')?.addEventListener('click', (event) => {
    const button = event.currentTarget as HTMLElement;
    const open = menu?.dataset.open !== 'true';
    if (menu) menu.dataset.open = String(open);
    button.setAttribute('aria-expanded', String(open));
  }, { signal });

  const docsDialog = document.querySelector<HTMLDialogElement>('[data-docs-menu]');
  document.querySelector<HTMLElement>('[data-docs-menu-open]')?.addEventListener('click', () => docsDialog?.showModal(), { signal });
  document.querySelector<HTMLElement>('[data-docs-menu-close]')?.addEventListener('click', () => docsDialog?.close(), { signal });

  const sentinel = document.querySelector('[data-header-sentinel]');
  const header = document.querySelector<HTMLElement>('[data-site-header]');
  if (sentinel && header) {
    const observer = new IntersectionObserver((entries) => { const entry = entries[0]; if (entry) header.dataset.compact = String(!entry.isIntersecting); }, { threshold: 0.1 });
    observer.observe(sentinel);
    signal.addEventListener('abort', () => observer.disconnect(), { once: true });
  }

  const tocLinks = [...document.querySelectorAll<HTMLAnchorElement>('.docs-toc a[href^="#"]')];
  if (tocLinks.length) {
    const headingObserver = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a,b) => a.boundingClientRect.top-b.boundingClientRect.top)[0];
      if (!visible) return;
      tocLinks.forEach((link) => link.dataset.active = String(link.hash === `#${visible.target.id}`));
    }, { rootMargin: '-15% 0px -70% 0px' });
    tocLinks.forEach((link) => { const heading = document.getElementById(link.hash.slice(1)); if (heading) headingObserver.observe(heading); });
    signal.addEventListener('abort', () => headingObserver.disconnect(), { once: true });
  }
}

function setupProgress(signal: AbortSignal) {
  const dot = document.querySelector<HTMLElement>('[data-progress-dot]');
  const update = () => {
    if (!dot) return;
    const max = document.documentElement.scrollHeight - innerHeight;
    dot.style.setProperty('--progress', String(max > 0 ? scrollY / max : 0));
  };
  update();
  addEventListener('scroll', update, { passive: true, signal });
  addEventListener('resize', update, { passive: true, signal });
}

export function initApp() {
  controller?.abort();
  controller = new AbortController();
  const { signal } = controller;
  prefixBaseLinks();
  setupTheme(signal);
  setupSearch(signal);
  setupProviders(signal);
  setupHeadingAnchors(signal);
  setupCopy(signal);
  setupChrome(signal);
  setupProgress(signal);
  setupSmooth(signal);
  setupMotion(signal);
}
