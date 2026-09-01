export function setupSmooth(signal: AbortSignal) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  // Lenis-like lerp without hijacking native scroll — use scroll-behavior + scrub
  // We smooth the visual progress by rAF interpolation of scrollY for parallax, not by blocking wheel.
  // For anchor clicks, use native smooth with offset
  const header = document.querySelector<HTMLElement>('[data-site-header]');
  const getOffset = () => (header?.offsetHeight || 68) + 12;

  // Smooth anchor navigation
  document.querySelectorAll<HTMLAnchorElement>('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href')!.slice(1);
      if (!id) return;
      const target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - getOffset();
      window.scrollTo({ top, behavior: 'smooth' });
      history.pushState(null, '', `#${id}`);
    }, { signal });
  });

  // Scrubbed parallax for sections — continuous, not stepped
  const sections = Array.from(document.querySelectorAll<HTMLElement>('.section, .hero, .provider-showcase, .fact-strip'));
  if (!sections.length) return;
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const vh = window.innerHeight;
      for (const el of sections) {
        const rect = el.getBoundingClientRect();
        // progress 0 at bottom of viewport, 1 at top
        const progress = Math.max(0, Math.min(1, (vh - rect.top) / (vh + rect.height)));
        // subtle parallax: previous section lifts slightly as next arrives — no hard cut
        const y = (1 - progress) * 6; // max 6px lift
        const scale = 1 - (1 - progress) * 0.006;
        // only apply when in view range to avoid layout thrash
        if (rect.top < vh && rect.bottom > 0) {
          el.style.setProperty('--scroll-progress', String(progress));
          // use transform on inner container to avoid fighting reveal
          if (!el.matches('.hero')) {
            el.style.transform = `translateY(${y * 0.18}px) scale(${scale})`;
            el.style.willChange = 'transform';
          }
        }
      }
      ticking = false;
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true, signal });
  window.addEventListener('resize', onScroll, { passive: true, signal });
  onScroll();

  // View-timeline fallback: add class when section is entering for CSS scrub
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        const el = e.target as HTMLElement;
        if (e.isIntersecting) {
          el.dataset.scrollVisible = 'true';
          // unobserve after first to keep scrub via onScroll
          io.unobserve(el);
        }
      }
    }, { threshold: 0.08, rootMargin: '0px 0px -8% 0px' });
    sections.forEach(s => io.observe(s));
    signal.addEventListener('abort', () => io.disconnect(), { once: true });
  }
}
