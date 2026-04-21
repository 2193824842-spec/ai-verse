// Enhance prose: pros/cons grid + FAQ grid
(function () {
  const prose = document.querySelector('.prose');
  if (!prose) return;

  // ── Pros / Cons grid ──────────────────────────────────────────
  const PRO_LABELS = /^(opportunities|pros|优势|机会|投资机会)$/i;
  const CON_LABELS = /^(risks|cons|劣势|风险|投资风险)$/i;

  // Collect consecutive h3+ul pairs that are pro/con
  const h3s = Array.from(prose.querySelectorAll('h3'));
  h3s.forEach((h3) => {
    const label = h3.textContent.trim();
    const isPro = PRO_LABELS.test(label);
    const isCon = CON_LABELS.test(label);
    if (!isPro && !isCon) return;

    // Must be sibling pair: h3 followed immediately by ul
    const ul = h3.nextElementSibling;
    if (!ul || ul.tagName !== 'UL') return;

    // Check if already wrapped
    if (h3.closest('.callout-card')) return;

    // Find the partner h3 (the other of the pair)
    const parent = h3.parentElement;
    const partner = isPro
      ? findNextSibling(h3, (el) => el.tagName === 'H3' && CON_LABELS.test(el.textContent.trim()))
      : findNextSibling(h3, (el) => el.tagName === 'H3' && PRO_LABELS.test(el.textContent.trim()));

    // Only wrap if partner exists and is close (within 4 siblings)
    if (!partner || !isCloseSibling(h3, partner, 4)) return;

    // Only process the pro side to avoid double-wrapping
    if (!isPro) return;

    const proH3 = h3;
    const proUl = ul;
    const conH3 = partner;
    const conUl = conH3.nextElementSibling;
    if (!conUl || conUl.tagName !== 'UL') return;

    // Build grid
    const grid = document.createElement('div');
    grid.className = 'pros-cons-grid';

    const proCard = document.createElement('div');
    proCard.className = 'callout-card callout-pro';
    proH3.className = '';
    proCard.appendChild(proH3);
    proCard.appendChild(proUl);

    const conCard = document.createElement('div');
    conCard.className = 'callout-card callout-con';
    conH3.className = '';
    conCard.appendChild(conH3);
    conCard.appendChild(conUl);

    grid.appendChild(proCard);
    grid.appendChild(conCard);

    // Insert grid where proH3 was (it's been detached)
    parent.insertBefore(grid, conH3.nextSibling || null);
    // conH3 was already moved into conCard
  });

  // ── FAQ grid ──────────────────────────────────────────────────
  const FAQ_LABEL = /faq|frequently asked|常见问题/i;

  const h2s = Array.from(prose.querySelectorAll('h2'));
  h2s.forEach((h2) => {
    if (!FAQ_LABEL.test(h2.textContent)) return;
    if (h2.closest('.faq-section')) return;

    // Collect h3+p pairs until next h2
    const items = [];
    let el = h2.nextElementSibling;
    while (el && el.tagName !== 'H2') {
      if (el.tagName === 'H3') {
        const p = el.nextElementSibling;
        if (p && (p.tagName === 'P' || p.tagName === 'UL')) {
          items.push({ h3: el, p });
        }
      }
      el = el.nextElementSibling;
    }
    if (items.length === 0) return;

    const section = document.createElement('div');
    section.className = 'faq-section';

    const heading = document.createElement('h2');
    heading.textContent = h2.textContent;
    section.appendChild(heading);

    const grid = document.createElement('div');
    grid.className = 'faq-grid';

    items.forEach(({ h3, p }) => {
      const item = document.createElement('div');
      item.className = 'faq-item';
      h3.className = '';
      item.appendChild(h3);
      item.appendChild(p);
      grid.appendChild(item);
    });

    section.appendChild(grid);
    h2.parentElement.insertBefore(section, h2);
    h2.remove();
  });

  function findNextSibling(el, test) {
    let cur = el.nextElementSibling;
    let steps = 0;
    while (cur && steps < 6) {
      if (test(cur)) return cur;
      cur = cur.nextElementSibling;
      steps++;
    }
    return null;
  }

  function isCloseSibling(a, b, maxSteps) {
    let cur = a.nextElementSibling;
    for (let i = 0; i < maxSteps; i++) {
      if (!cur) return false;
      if (cur === b) return true;
      cur = cur.nextElementSibling;
    }
    return false;
  }
})();
