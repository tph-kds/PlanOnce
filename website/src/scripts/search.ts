import { searchIndex } from '../data/search';

function resultLinks(results: HTMLElement) {
  return [...results.querySelectorAll<HTMLAnchorElement>('a.search-result')];
}

function setActiveResult(results: HTMLElement, index: number) {
  const links = resultLinks(results);
  if (!links.length) return -1;
  const normalized = ((index % links.length) + links.length) % links.length;
  links.forEach((link, current) => {
    const active = current === normalized;
    link.dataset.active = String(active);
    link.setAttribute('aria-current', active ? 'true' : 'false');
  });
  links[normalized]?.scrollIntoView({ block: 'nearest' });
  return normalized;
}

function render(results: HTMLElement, query = '') {
  const q = query.trim().toLowerCase();
  const matches = searchIndex
    .filter((item) => !q || `${item.category} ${item.title} ${item.text}`.toLowerCase().includes(q))
    .slice(0, 10);
  results.replaceChildren();
  if (!matches.length) {
    const empty = document.createElement('div');
    empty.className = 'search-empty';
    empty.textContent = 'No matching documentation found.';
    results.append(empty);
    return -1;
  }
  let lastCategory = '';
  for (const item of matches) {
    if (item.category !== lastCategory) {
      const heading = document.createElement('div');
      heading.className = 'search-category';
      heading.textContent = item.category;
      results.append(heading);
      lastCategory = item.category;
    }
    const link = document.createElement('a');
    link.className = 'search-result';
    link.href = item.href;
    link.innerHTML = `<strong></strong><span></span>`;
    link.querySelector('strong')!.textContent = item.title;
    link.querySelector('span')!.textContent = item.text;
    results.append(link);
  }
  return setActiveResult(results, 0);
}

export function setupSearch(signal: AbortSignal) {
  const dialog = document.querySelector<HTMLDialogElement>('[data-search-dialog]');
  const input = document.querySelector<HTMLInputElement>('[data-search-input]');
  const results = document.querySelector<HTMLElement>('[data-search-results]');
  let trigger: HTMLElement | null = null;
  let activeIndex = -1;
  if (!dialog || !input || !results) return;

  const open = (source?: HTMLElement | null) => {
    trigger = source || null;
    input.value = '';
    activeIndex = render(results);
    if (!dialog.open) dialog.showModal();
    queueMicrotask(() => input.focus());
  };
  const close = () => dialog.close();

  document.querySelectorAll<HTMLElement>('[data-search-open]').forEach((button) => button.addEventListener('click', () => open(button), { signal }));
  dialog.querySelector<HTMLElement>('[data-search-close]')?.addEventListener('click', close, { signal });
  input.addEventListener('input', () => { activeIndex = render(results, input.value); }, { signal });
  input.addEventListener('keydown', (event) => {
    const links = resultLinks(results);
    if (!links.length) return;
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      activeIndex = setActiveResult(results, activeIndex + 1);
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      activeIndex = setActiveResult(results, activeIndex - 1);
    } else if (event.key === 'Home') {
      event.preventDefault();
      activeIndex = setActiveResult(results, 0);
    } else if (event.key === 'End') {
      event.preventDefault();
      activeIndex = setActiveResult(results, links.length - 1);
    } else if (event.key === 'Enter' && activeIndex >= 0) {
      event.preventDefault();
      links[activeIndex]?.click();
    }
  }, { signal });
  results.addEventListener('mousemove', (event) => {
    const link = (event.target as HTMLElement).closest<HTMLAnchorElement>('a.search-result');
    if (!link) return;
    const index = resultLinks(results).indexOf(link);
    if (index >= 0) activeIndex = setActiveResult(results, index);
  }, { signal });
  dialog.addEventListener('close', () => trigger?.focus(), { signal });
  document.addEventListener('keydown', (event) => {
    const target = event.target as HTMLElement | null;
    const typing = !!target?.closest('input, textarea, [contenteditable="true"]');
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault(); open(document.activeElement as HTMLElement);
    } else if (event.key === '/' && !typing && !dialog.open) {
      event.preventDefault(); open(document.activeElement as HTMLElement);
    }
  }, { signal });
}
