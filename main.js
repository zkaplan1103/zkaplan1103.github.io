document.documentElement.classList.add('js');

// Reveal sections as they scroll into view
const io = new IntersectionObserver((entries) => {
  for (const e of entries) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// Work page filters. Without JS every card shows.
const chips = document.querySelectorAll('.filters button');
if (chips.length) {
  const cards = document.querySelectorAll('[data-type]');
  const apply = (type) => {
    chips.forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.filter === type)));
    cards.forEach((card) => { card.hidden = type !== 'all' && card.dataset.type !== type; card.classList.add('in'); });
    const url = new URL(location);
    type === 'all' ? url.searchParams.delete('type') : url.searchParams.set('type', type);
    history.replaceState(null, '', url);
  };
  chips.forEach((c) => c.addEventListener('click', () => apply(c.dataset.filter)));
  const start = new URLSearchParams(location.search).get('type');
  apply([...chips].some((c) => c.dataset.filter === start) ? start : 'all');
}
