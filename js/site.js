// Lorenzo Gravina — site interactions
// Usa Motion (js/motion.min.js) se disponibile; senza, il sito resta completo con le transizioni CSS.
(() => {
  const root = document.documentElement;
  const M = window.Motion;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const useMotion = !!(M && M.animate && !reduce);
  const spring = useMotion && M.spring;
  if (useMotion) root.classList.add('has-motion');

  // ---------- 2. Ingresso dell'hero: parola per parola, a molla ----------
  const playEntrance = () => {
    root.classList.add('is-ready');
    if (!useMotion) return;
    const words = [...document.querySelectorAll('.reveal-line > span')];
    if (!words.length) return;
    try {
      const anim = M.animate(words,
        { transform: ['translateY(105%)', 'translateY(0%)'] },
        { type: spring, bounce: 0.25, visualDuration: 0.6, delay: M.stagger(0.055) });
      Promise.resolve(anim.finished || anim).then(() => words.forEach(w => { w.style.transform = 'none'; }));
    } catch (e) {
      words.forEach(w => { w.style.transform = 'none'; });
    }
  };
  const ready = () => requestAnimationFrame(playEntrance);
  if (document.fonts && document.fonts.ready) {
    Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 600))]).then(ready);
  } else { ready(); }

  // Header border once the page scrolls
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // ---------- 1. Indice dei lavori: anteprima a tendina + inclinazione ----------
  const items = [...document.querySelectorAll('.work-item')];
  const figures = [...document.querySelectorAll('.work-preview figure')];
  const preview = document.querySelector('.work-preview');
  const tilt = document.querySelector('.work-preview .tilt');
  const desktop = matchMedia('(min-width: 901px) and (pointer: fine)');
  let current = Math.max(0, figures.findIndex(f => f.classList.contains('is-active')));

  const activate = (slug) => {
    const idx = figures.findIndex(f => f.dataset.slug === slug);
    items.forEach(i => i.classList.toggle('is-active', i.dataset.slug === slug));
    if (idx < 0 || idx === current) return;

    if (!useMotion || !desktop.matches) {
      figures.forEach((f, i) => f.classList.toggle('is-active', i === idx));
      current = idx;
      return;
    }

    const dir = idx > current ? 1 : -1;
    const prev = figures[current];
    const next = figures[idx];
    current = idx;
    figures.forEach(f => {
      f.style.zIndex = f === next ? 2 : f === prev ? 1 : 0;
      if (f !== next && f !== prev) f.classList.remove('is-active');
    });
    next.classList.add('is-active');
    const from = dir > 0 ? 'inset(100% 0% 0% 0%)' : 'inset(0% 0% 100% 0%)';
    const wipe = M.animate(next, { clipPath: [from, 'inset(0% 0% 0% 0%)'] },
      { type: spring, bounce: 0, visualDuration: 0.55 });
    const img = next.querySelector('img');
    if (img) M.animate(img, { transform: ['scale(1.12)', 'scale(1)'] }, { duration: 0.9, ease: [0.2, 0.7, 0.1, 1] });
    Promise.resolve(wipe.finished || wipe).then(() => {
      if (figures[current] === next && prev !== next) prev.classList.remove('is-active');
    });
  };

  items.forEach(item => {
    const link = item.querySelector('a');
    link.addEventListener('mouseenter', () => activate(item.dataset.slug));
    link.addEventListener('focus', () => activate(item.dataset.slug));
  });

  const index = document.querySelector('.work-index');
  if (useMotion && index && tilt) {
    let frame = 0, lastX = 0, lastY = 0;
    const toTilt = (rx, ry) => M.animate(tilt,
      { transform: `rotateX(${rx}deg) rotateY(${ry}deg)` },
      { type: spring, stiffness: 140, damping: 18 });
    index.addEventListener('pointermove', (e) => {
      if (!desktop.matches) return;
      lastX = e.clientX; lastY = e.clientY;
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        const r = preview.getBoundingClientRect();
        const x = Math.max(-1, Math.min(1, (lastX - (r.left + r.width / 2)) / (r.width)));
        const y = Math.max(-1, Math.min(1, (lastY - (r.top + r.height / 2)) / (r.height)));
        toTilt((-y * 5).toFixed(2), (x * 7).toFixed(2));
      });
    });
    index.addEventListener('pointerleave', () => toTilt(0, 0));
  }

  // ---------- 5. Transizione tra pagine (View Transitions) ----------
  // Il titolo ha un nome fisso in HTML; la copertina lo riceve solo sull'elemento visibile,
  // perché due elementi con lo stesso nome annullerebbero la transizione.
  const coverFor = (slug) => desktop.matches
    ? figures.find(f => f.dataset.slug === slug)
    : document.querySelector(`.work-item[data-slug="${slug}"] .thumb`);
  const clearCovers = () => document.querySelectorAll('[data-vt]').forEach(el => { el.style.viewTransitionName = ''; });

  items.forEach(item => {
    item.querySelector('a').addEventListener('click', () => {
      clearCovers();
      const el = coverFor(item.dataset.slug);
      if (el) el.style.viewTransitionName = `cover-${item.dataset.slug}`;
    });
  });

  // Ritorno alla home da un case study: la copertina torna al suo posto nella lista
  window.addEventListener('pagereveal', (e) => {
    if (!e.viewTransition || !items.length) return;
    const from = window.navigation && navigation.activation && navigation.activation.from;
    const slug = from && from.url ? from.url.split('/').pop().replace('.html', '').split(/[?#]/)[0] : '';
    if (!items.some(i => i.dataset.slug === slug)) return;
    if (desktop.matches) {
      figures.forEach(f => f.classList.toggle('is-active', f.dataset.slug === slug));
      current = figures.findIndex(f => f.dataset.slug === slug);
      items.forEach(i => i.classList.toggle('is-active', i.dataset.slug === slug));
    }
    const el = coverFor(slug);
    if (el) el.style.viewTransitionName = `cover-${slug}`;
    e.viewTransition.finished.finally(clearCovers);
  });
  window.addEventListener('pageshow', (e) => { if (e.persisted) clearCovers(); });

  // ---------- 3. Case study: copertina legata allo scroll, schermate che entrano una volta ----------
  const cover = document.querySelector('.cs-cover');
  if (useMotion && cover && M.scroll) {
    M.scroll((progress) => {
      const s = 0.92 + 0.08 * progress;
      cover.style.transform = `scale(${s.toFixed(4)})`;
    }, { target: cover, offset: ['start end', 'start 0.2'] });
  }

  const shots = [...document.querySelectorAll('.gallery figure')];
  if (useMotion && shots.length && M.inView) {
    const below = shots.filter(el => el.getBoundingClientRect().top > window.innerHeight * 0.9);
    below.forEach(el => { el.style.opacity = '0'; el.style.transform = 'translateY(40px)'; });
    const seen = new WeakSet();
    M.inView(below, (el) => {
      if (seen.has(el)) return;
      seen.add(el);
      // le schermate sulla stessa riga entrano in sequenza
      const row = el.classList.contains('wide') ? 0 : shots.filter(s => !s.classList.contains('wide')).indexOf(el) % 3;
      const anim = M.animate(el,
        { opacity: [0, 1], transform: ['translateY(40px)', 'translateY(0px)'] },
        { type: spring, bounce: 0.15, visualDuration: 0.6, delay: row * 0.09 });
      Promise.resolve(anim.finished || anim).then(() => { el.style.opacity = ''; el.style.transform = ''; });
    }, { margin: '0px 0px -12% 0px' });
  }

  // ---------- 4. Bottone magnetico nel blocco contatti (solo desktop) ----------
  const magnet = document.querySelector('.contact .btn.primary');
  const contactBox = document.querySelector('.contact');
  if (useMotion && magnet && contactBox && matchMedia('(pointer: fine)').matches) {
    let pulled = false, frame = 0, px = 0, py = 0;
    const moveTo = (x, y) => M.animate(magnet,
      { transform: `translate(${x}px, ${y}px)` },
      { type: spring, stiffness: 260, damping: 16 });
    contactBox.addEventListener('pointermove', (e) => {
      px = e.clientX; py = e.clientY;
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        const r = magnet.getBoundingClientRect();
        const dx = px - (r.left + r.width / 2);
        const dy = py - (r.top + r.height / 2);
        const reach = Math.max(r.width, r.height) * 0.5 + 70;
        if (Math.hypot(dx, dy) < reach) {
          pulled = true;
          moveTo((dx * 0.3).toFixed(1), (dy * 0.4).toFixed(1));
        } else if (pulled) {
          pulled = false;
          moveTo(0, 0);
        }
      });
    });
    contactBox.addEventListener('pointerleave', () => { if (pulled) { pulled = false; moveTo(0, 0); } });
  }

  // Contact spotlight follows the pointer (a nod to the old site's lime glow)
  const contact = document.querySelector('.contact');
  if (contact && matchMedia('(pointer: fine)').matches) {
    contact.addEventListener('pointermove', (e) => {
      const r = contact.getBoundingClientRect();
      contact.style.setProperty('--mx', `${e.clientX - r.left}px`);
      contact.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  }

  // Copy e-mail address (fallback when no mail app opens)
  document.querySelectorAll('[data-copy]').forEach(btn => {
    const status = btn.parentElement.querySelector('.copy-status');
    btn.addEventListener('click', async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        if (status) status.textContent = 'Indirizzo copiato';
      } catch (e) {
        const link = btn.parentElement.querySelector('.mail');
        const range = document.createRange(); range.selectNodeContents(link);
        const sel = getSelection(); sel.removeAllRanges(); sel.addRange(range);
        if (status) status.textContent = 'Indirizzo selezionato: premi Ctrl+C per copiarlo';
      }
    });
  });

  // Footer year
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
