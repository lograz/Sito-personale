// Lorenzo Gravina — site interactions (no dependencies)
(() => {
  const root = document.documentElement;

  // Entrance: content is visible without JS; with JS, play one orchestrated reveal.
  const ready = () => requestAnimationFrame(() => root.classList.add('is-ready'));
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

  // Work index: hovering or focusing a project swaps the preview
  const items = document.querySelectorAll('.work-item');
  const figures = document.querySelectorAll('.work-preview figure');
  const activate = (slug) => {
    items.forEach(i => i.classList.toggle('is-active', i.dataset.slug === slug));
    figures.forEach(f => f.classList.toggle('is-active', f.dataset.slug === slug));
  };
  items.forEach(item => {
    const link = item.querySelector('a');
    link.addEventListener('mouseenter', () => activate(item.dataset.slug));
    link.addEventListener('focus', () => activate(item.dataset.slug));
  });

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
