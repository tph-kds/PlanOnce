type ProviderPayload = { id: string; name: string; projectPath: string; globalPath: string; note?: string; command: string };

export function setupProviders(signal: AbortSignal) {
  document.querySelectorAll<HTMLElement>('[data-provider-tabs]').forEach((root) => {
    const dataNode = root.querySelector<HTMLScriptElement>('[data-provider-data]');
    const panel = root.querySelector<HTMLElement>('[data-provider-live]');
    if (!dataNode || !panel) return;
    const providers = JSON.parse(dataNode.textContent || '[]') as ProviderPayload[];
    const tabs = [...root.querySelectorAll<HTMLButtonElement>('[data-provider-tab]')];

    const select = (id: string, focus = false) => {
      const provider = providers.find((item) => item.id === id);
      if (!provider) return;
      tabs.forEach((tab) => {
        const active = tab.dataset.providerTab === id;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        if (active && focus) tab.focus({ preventScroll: true });
      });
      panel.querySelector<HTMLElement>('[data-provider-name]')!.textContent = provider.name;
      panel.querySelector<HTMLElement>('[data-provider-command]')!.textContent = provider.command;
      const copy = panel.querySelector<HTMLElement>('[data-provider-copy]');
      copy?.setAttribute('data-copy', provider.command);
      panel.querySelector<HTMLElement>('[data-provider-project]')!.textContent = provider.projectPath;
      panel.querySelector<HTMLElement>('[data-provider-global]')!.textContent = provider.globalPath;
      const note = panel.querySelector<HTMLElement>('[data-provider-note]');
      if (note) note.textContent = provider.note || 'Standard PlanOnce skill discovery path.';
      panel.dataset.activeProvider = id;
    };

    tabs.forEach((tab) => tab.addEventListener('click', () => select(tab.dataset.providerTab || ''), { signal }));
    root.querySelector<HTMLElement>('[role="tablist"]')?.addEventListener('keydown', (event) => {
      if (!['ArrowRight', 'ArrowLeft', 'Home', 'End'].includes(event.key)) return;
      const selectedIndex = Math.max(0, tabs.findIndex((tab) => tab.getAttribute('aria-selected') === 'true'));
      let nextIndex = selectedIndex;
      if (event.key === 'ArrowRight') nextIndex = (selectedIndex + 1) % tabs.length;
      if (event.key === 'ArrowLeft') nextIndex = (selectedIndex - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') nextIndex = 0;
      if (event.key === 'End') nextIndex = tabs.length - 1;
      event.preventDefault();
      select(tabs[nextIndex]?.dataset.providerTab || '', true);
    }, { signal });

    select(providers[0]?.id || '');
  });
}
