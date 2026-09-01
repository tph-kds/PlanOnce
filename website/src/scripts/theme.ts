export function applyTheme() {
  const saved = localStorage.getItem('planonce-theme');
  const systemDark = matchMedia('(prefers-color-scheme: dark)').matches;
  document.documentElement.dataset.theme = saved || (systemDark ? 'dark' : 'light');
}

export function setupTheme(signal: AbortSignal) {
  applyTheme();
  document.querySelectorAll<HTMLElement>('[data-theme-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      localStorage.setItem('planonce-theme', next);
    }, { signal });
  });
}
