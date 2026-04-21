// Enhance prose: pros/cons grid + FAQ grid
(function () {
  const prose = document.querySelector('.prose');
  if (!prose) return;

  // ── Pros / Cons grid ──────────────────────────────────────────
  const PRO_LABELS = /^(opportunities|pros|优势|机会|投资机会)$/i;
  const CON_LABELS = /^(risks|cons|劣势|风险|投资风险)$/i;

  const allH3 = Array.from(prose.querySelectorAll('h3'));
  const processed = new Set();

  allH3.forEach((h3) => {
    if (processed.has(h3)) return;
    const label = h3.textContent.trim();
    if (!PRO_LABELS.test(label)) return;

    const proUl = h3.nextElementSibling;
    if (!proUl || proUl.tagName !== 'UL') return;

    // Find the con h3 within next 4 siblings after proUl
    let conH3 = null;
    let cur = proUl.nextElementSibling;
    for (let i = 0; i < 4; i++) {
      if (!cur) break;
      if (cur.tagName === 'H3' && CON_LABELS.test(cur.textContent.trim())) {
        conH3 = cur;
        break;
      }
      cur = cur.nextElementSibling;
    }
    if (!conH3) return;

    const conUl = conH3.nextElementSibling;
    if (!conUl || conUl.tagName !== 'UL') return;

    processed.add(h3);
    processed.add(conH3);

    // Record insertion point BEFORE moving any nodes
    const insertBefore = conUl.nextSibling;
    const parent = h3.parentElement;

    const grid = document.createElement('div');
    grid.className = 'pros-cons-grid';

    const proCard = document.createElement('div');
    proCard.className = 'callout-card callout-pro';
    proCard.appendChild(h3);
    proCard.appendChild(proUl);

    const conCard = document.createElement('div');
    conCard.className = 'callout-card callout-con';
    conCard.appendChild(conH3);
    conCard.appendChild(conUl);

    grid.appendChild(proCard);
    grid.appendChild(conCard);

    parent.insertBefore(grid, insertBefore);
  });

  // ── FAQ grid ──────────────────────────────────────────────────
  const FAQ_LABEL = /faq|frequently asked|常见问题/i;

  Array.from(prose.querySelectorAll('h2')).forEach((h2) => {
    if (!FAQ_LABEL.test(h2.textContent)) return;
    if (h2.closest('.faq-section')) return;

    const items = [];
    let el = h2.nextElementSibling;
    while (el && el.tagName !== 'H2') {
      if (el.tagName === 'H3') {
        const next = el.nextElementSibling;
        if (next && (next.tagName === 'P' || next.tagName === 'UL')) {
          items.push([el, next]);
        }
      }
      el = el.nextElementSibling;
    }
    if (items.length === 0) return;

    const insertBefore = h2.nextSibling;
    const parent = h2.parentElement;

    const section = document.createElement('div');
    section.className = 'faq-section';

    const heading = h2.cloneNode(true);
    heading.className = '';
    section.appendChild(heading);

    const grid = document.createElement('div');
    grid.className = 'faq-grid';

    items.forEach(([h3, p]) => {
      const item = document.createElement('div');
      item.className = 'faq-item';
      item.appendChild(h3);
      item.appendChild(p);
      grid.appendChild(item);
    });

    section.appendChild(grid);
    parent.insertBefore(section, insertBefore);
    h2.remove();
  });
})();
