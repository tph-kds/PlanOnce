import { animate } from 'motion/mini';
import { motionTheme, reduceMotion } from '../motion/theme';

export function setupMotion(signal: AbortSignal) {
  const reduced = reduceMotion();
  const observers: IntersectionObserver[] = [];

  const observeOnce = (selector: string, run: (node: HTMLElement) => void, opts: IntersectionObserverInit = { threshold: 0.12 }) => {
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const node = entry.target as HTMLElement;
        run(node);
        observer.unobserve(node);
      }
    }, opts);
    document.querySelectorAll<HTMLElement>(selector).forEach((node) => observer.observe(node));
    observers.push(observer);
  };

  const observeGroup = (selector: string, run: (nodes: HTMLElement[]) => void) => {
    const nodes = Array.from(document.querySelectorAll<HTMLElement>(selector));
    if (!nodes.length) return;
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const root = entry.target as HTMLElement;
        observer.unobserve(root);
        run(nodes);
        break;
      }
    }, { threshold: 0.08 });
    const first = nodes[0];
    if (first) observer.observe(first.closest('.provider-showcase, .workflow-rails, .evidence-chain, .reliability-loop-nodes, .security-readiness, .authority-map, .docs-paths, .provider-constellation') as HTMLElement || first);
    observers.push(observer);
  };

  if (reduced) {
    document.querySelectorAll<HTMLElement>('.reveal').forEach((node) => node.dataset.visible = 'true');
    document.querySelectorAll<HTMLElement>('.provider-item, .evidence-step, .workflow-nodes article, .gate-card, .authority-node, .docs-path, .provider-constellation li, .compare-row, .release-fact').forEach(n => n.dataset.visible = 'true');
    return;
  }

  // Generic reveal — softer, with blur
  observeOnce('.reveal', (node) => {
    node.dataset.visible = 'true';
    animate(node, { opacity: [0, 1], transform: ['translateY(14px)', 'translateY(0px)'], filter: ['blur(4px)', 'blur(0px)'] } as any, { duration: motionTheme.duration.gentle, ease: motionTheme.easing.standard as any });
  });

  // Provider showcase — staggered orbit lift with scale + metallic sheen
  (() => {
    const grids = document.querySelectorAll<HTMLElement>('.provider-grid');
    grids.forEach(grid => {
      const items = Array.from(grid.querySelectorAll<HTMLElement>('.provider-item'));
      if (!items.length) return;
      items.forEach(el => { el.style.opacity = '0'; el.style.transform = 'translateY(14px) scale(0.97)'; });
      const obs = new IntersectionObserver((entries) => {
        for (const e of entries) if (e.isIntersecting) {
          obs.unobserve(e.target);
          items.forEach((el, i) => {
            animate(el, { opacity: [0, 1], transform: ['translateY(14px) scale(0.97)', 'translateY(0px) scale(1)'] }, { duration: 0.54, delay: i * 0.055, ease: motionTheme.easing.standard as any });
          });
        }
      }, { threshold: 0.12 });
      obs.observe(grid);
      observers.push(obs);
    });
  })();

  // Provider constellation — sequential pop
  (() => {
    const list = document.querySelector('.provider-constellation');
    if (!list) return;
    const items = Array.from(list.querySelectorAll<HTMLElement>('li'));
    items.forEach(el => { el.style.opacity = '0'; el.style.transform = 'translateY(10px) scale(0.98)'; });
    const obs = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) {
        obs.unobserve(e.target);
        items.forEach((el, i) => animate(el, { opacity: [0,1], transform: ['translateY(10px) scale(0.98)', 'translateY(0) scale(1)'] }, { duration: 0.46, delay: i*0.045, ease: motionTheme.easing.standard as any } as any));
      }
    }, { threshold: 0.15 });
    obs.observe(list);
    observers.push(obs);
  })();

  // Evidence chain — left slide with line growth
  (() => {
    const chain = document.querySelector('.evidence-chain');
    if (!chain) return;
    const steps = Array.from(chain.querySelectorAll<HTMLElement>('.evidence-step'));
    const arrows = Array.from(chain.querySelectorAll<HTMLElement>('.evidence-arrow'));
    steps.forEach(el => { el.style.opacity='0'; el.style.transform='translateX(-12px)'; });
    arrows.forEach(el => { el.style.transform='scaleY(0)'; (el as HTMLElement).style.transformOrigin='top'; });
    const obs = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) {
        obs.unobserve(e.target);
        steps.forEach((el,i)=> animate(el, { opacity:[0,1], transform:['translateX(-12px)','translateX(0px)'] }, { duration:0.48, delay:i*0.09, ease: motionTheme.easing.standard as any } as any));
        arrows.forEach((el,i)=> animate(el, { transform:['scaleY(0)','scaleY(1)'] }, { duration:0.42, delay:0.12+i*0.09, ease: [0.22,1,0.36,1] as any } as any));
      }
    }, { threshold:0.18 });
    obs.observe(chain);
    observers.push(obs);
  })();

  // Workflow lanes — card tilt + stagger
  (() => {
    const lanes = document.querySelectorAll<HTMLElement>('.workflow-lane');
    lanes.forEach(lane => {
      const cards = Array.from(lane.querySelectorAll<HTMLElement>('.workflow-nodes article'));
      cards.forEach(el=> { el.style.opacity='0'; el.style.transform='translateY(12px) rotateX(4deg)'; (el as any).style.transformOrigin='center top'; });
      const obs = new IntersectionObserver((entries)=>{
        for(const e of entries) if(e.isIntersecting){
          obs.unobserve(e.target);
          cards.forEach((el,i)=> animate(el, { opacity:[0,1], transform:['translateY(12px) rotateX(4deg)','translateY(0px) rotateX(0deg)'] }, { duration:0.5, delay:i*0.07, ease: motionTheme.easing.standard as any } as any));
        }
      },{threshold:0.14});
      obs.observe(lane);
      observers.push(obs);
    });
  })();

  // Reliability loop — SVG + nodes pop with orbit pulse
  observeOnce('[data-workflow-path]', (node) => animate(node, { strokeDashoffset: [1, 0] }, { duration: 0.9, ease: 'ease-out' } as any));
  observeOnce('[data-reliability-path]', (node) => animate(node, { opacity: [0.25, 1] }, { duration: 0.7 } as any));
  (() => {
    const loop = document.querySelector('.reliability-loop-nodes');
    if (!loop) return;
    const cards = Array.from(loop.querySelectorAll<HTMLElement>('article'));
    cards.forEach(el=> { el.style.opacity='0'; el.style.transform='scale(0.96) translateY(8px)'; });
    const obs = new IntersectionObserver((entries)=>{
      for(const e of entries) if(e.isIntersecting){
        obs.unobserve(e.target);
        cards.forEach((el,i)=> animate(el, { opacity:[0,1], transform:['scale(0.96) translateY(8px)','scale(1) translateY(0px)'] }, { duration:0.46, delay:i*0.06, ease: motionTheme.easing.standard as any } as any));
      }
    },{threshold:0.15});
    obs.observe(loop);
    observers.push(obs);
  })();

  // Security gates + authority
  (() => {
    const gates = Array.from(document.querySelectorAll<HTMLElement>('.gate-card'));
    gates.forEach(el=> { el.style.opacity='0'; el.style.transform='translateY(10px) scale(0.98)'; });
    const obs = new IntersectionObserver((entries)=>{
      for(const e of entries) if(e.isIntersecting){
        obs.unobserve(e.target);
        gates.forEach((el,i)=> animate(el, { opacity:[0,1], transform:['translateY(10px) scale(0.98)','translateY(0) scale(1)'] }, { duration:0.5, delay:i*0.08, ease: motionTheme.easing.standard as any } as any));
      }
    },{threshold:0.16});
    const sec = document.querySelector('.security-readiness');
    if(sec) obs.observe(sec);
    observers.push(obs);
  })();
  (() => {
    const map = document.querySelector('.authority-map');
    if(!map) return;
    const nodes = Array.from(map.querySelectorAll<HTMLElement>('.authority-node, .authority-arrow, .authority-output span'));
    nodes.forEach(el=> { el.style.opacity='0'; el.style.transform='translateY(10px)'; });
    const obs = new IntersectionObserver((entries)=>{
      for(const e of entries) if(e.isIntersecting){
        obs.unobserve(e.target);
        nodes.forEach((el,i)=> animate(el, { opacity:[0,1], transform:['translateY(10px)','translateY(0)'] }, { duration:0.44, delay:i*0.05, ease: motionTheme.easing.standard as any } as any));
      }
    },{threshold:0.15});
    obs.observe(map);
    observers.push(obs);
  })();

  // Compare panel — split reveal with divider grow
  (() => {
    const panel = document.querySelector('.compare-panel');
    if(!panel) return;
    const cols = Array.from(panel.querySelectorAll<HTMLElement>('.compare-col'));
    cols.forEach((el, idx)=> { el.style.opacity='0'; el.style.transform = idx===0 ? 'translateX(-12px)' : 'translateX(12px)'; });
    const obs = new IntersectionObserver((entries)=>{
      for(const e of entries) if(e.isIntersecting){
        obs.unobserve(e.target);
        cols.forEach((el,i)=> animate(el, { opacity:[0,1], transform:[i===0?'translateX(-12px)':'translateX(12px)','translateX(0)'] }, { duration:0.52, delay:i*0.08, ease: motionTheme.easing.standard as any } as any));
      }
    },{threshold:0.15});
    obs.observe(panel);
    observers.push(obs);
  })();

  // Release facts — counter + lift
  (() => {
    const facts = Array.from(document.querySelectorAll<HTMLElement>('.release-fact'));
    facts.forEach(el=> { el.style.opacity='0'; el.style.transform='translateY(8px)'; });
    const obs = new IntersectionObserver((entries)=>{
      for(const e of entries) if(e.isIntersecting){
        obs.unobserve(e.target);
        facts.forEach((el,i)=> animate(el, { opacity:[0,1], transform:['translateY(8px)','translateY(0)'] }, { duration:0.42, delay:i*0.06, ease: motionTheme.easing.standard as any } as any));
      }
    },{threshold:0.2});
    const strip = document.querySelector('.fact-strip');
    if(strip) obs.observe(strip);
    observers.push(obs);
  })();

  // Docs paths + FAQ — card tilt
  (() => {
    const paths = Array.from(document.querySelectorAll<HTMLElement>('.docs-path'));
    paths.forEach(el=> { el.style.opacity='0'; el.style.transform='translateY(10px) rotateX(2deg)'; (el as any).style.transformOrigin='center bottom'; });
    const obs = new IntersectionObserver((entries)=>{
      for(const e of entries) if(e.isIntersecting){
        obs.unobserve(e.target);
        paths.forEach((el,i)=> animate(el, { opacity:[0,1], transform:['translateY(10px) rotateX(2deg)','translateY(0) rotateX(0)'] }, { duration:0.48, delay:i*0.07, ease: motionTheme.easing.standard as any } as any));
      }
    },{threshold:0.14});
    const wrap = document.querySelector('.docs-paths');
    if(wrap) obs.observe(wrap);
    observers.push(obs);
  })();

  observeOnce('[data-counter]', (node) => {
    const target = Number(node.dataset.counter || node.textContent || 0);
    const started = performance.now();
    const duration = 650;
    const tick = (now: number) => {
      const p = Math.min(1, (now - started) / duration);
      node.textContent = String(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1 && !signal.aborted) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });

  // Docs content — per-element distinct transforms
  (() => {
    const selectors = [
      { sel: '.docs-content h2', transform: ['translateX(-10px)','translateX(0px)'] as any, dur: 0.44 },
      { sel: '.docs-content h3', transform: ['translateX(-8px)','translateX(0px)'] as any, dur: 0.4 },
      { sel: '.docs-content p', transform: ['translateY(6px)','translateY(0px)'] as any, dur: 0.42 },
      { sel: '.docs-content pre', transform: ['translateY(8px) scale(0.99)','translateY(0px) scale(1)'] as any, dur: 0.46 },
      { sel: '.docs-content blockquote', transform: ['translateX(-8px)','translateX(0px)'] as any, dur: 0.42 },
      { sel: '.docs-content table', transform: ['translateY(8px)','translateY(0px)'] as any, dur: 0.44 },
      { sel: '.docs-content ul, .docs-content ol', transform: ['translateY(6px)','translateY(0px)'] as any, dur: 0.42 },
    ];
    selectors.forEach(({sel, transform, dur})=>{
      observeOnce(sel, (node)=>{
        node.style.opacity='0';
        (node as any).style.filter='blur(3px)';
        animate(node, { opacity:[0,1], transform, filter:['blur(3px)','blur(0px)'] } as any, { duration: dur, ease: motionTheme.easing.standard as any });
      }, { threshold: 0.1 });
    });
  })();

  signal.addEventListener('abort', () => observers.forEach((observer) => observer.disconnect()), { once: true });
}
