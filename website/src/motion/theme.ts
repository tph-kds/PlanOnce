export const motionTheme = {
  duration: { snap: 0.16, ui: 0.28, gentle: 0.52, page: 0.32, ambient: 28 },
  stagger: { tight: 0.04, base: 0.08, relaxed: 0.14 },
  travel: { hover: 3, enter: 20, section: 36 },
  easing: { standard: [0.22, 1, 0.36, 1] as const },
} as const;

export const reduceMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
