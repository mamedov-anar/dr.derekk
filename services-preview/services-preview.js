(() => {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function revealFragment() {
    if (!window.location.hash) return;
    let identifier;
    try {
      identifier = decodeURIComponent(window.location.hash.slice(1));
    } catch (_) {
      return;
    }
    const target = document.getElementById(identifier);
    if (!target) return;
    const parent = target.closest('details');
    if (parent) parent.open = true;
    target.scrollIntoView({ behavior: reducedMotion.matches ? 'auto' : 'smooth', block: 'start' });
  }

  document.querySelectorAll('details').forEach((detail) => {
    detail.addEventListener('toggle', () => {
      if (!detail.open || reducedMotion.matches) return;
      const content = detail.querySelector('.service-content, .care-content') || detail;
      content.classList.remove('is-opening');
      requestAnimationFrame(() => content.classList.add('is-opening'));
    });
    detail.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape' || !detail.open) return;
      detail.open = false;
      detail.querySelector('summary')?.focus();
      event.stopPropagation();
    });
  });

  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('[data-reveal]').forEach((element) => observer.observe(element));
  }

  window.addEventListener('hashchange', revealFragment);
  if (window.location.hash) requestAnimationFrame(revealFragment);

  document.addEventListener('visibilitychange', () => {
    document.querySelectorAll('.hero-photo img').forEach((photo) => {
      photo.style.animationPlayState = document.hidden ? 'paused' : 'running';
    });
  });
})();
