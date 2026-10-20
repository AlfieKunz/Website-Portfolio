function initProgressBars() {
  document.addEventListener('DOMContentLoaded', () => {
    const th = document.createElement('th');
    th.className = 'count extra-col';
    th.textContent = 'Progress';
    const dueTh = document.querySelector('table tr:nth-child(1) th.count:nth-last-of-type(2)');

    dueTh.after(th);

    // Insert stacked bar for each deck row
    document.querySelectorAll('table tr.deck').forEach(tr => {
      const deckId = tr.id;
      const { all: total, mature, young, suspended, learning, new: new_cards } = window.deckStats[deckId];
      const dueTd = tr.querySelectorAll('td[align="end"]')[2];

      // container
      const td = document.createElement('td');
      td.className = 'count extra-col';
      const container = document.createElement('div');
      container.className = 'stacked-bar-container';

      const pct = x => total > 0 ? (x / total) * 100 : 0;
      [
        { val: mature, cls: 'segment-mature', label: `Mature` },
        { val: young, cls: 'segment-young', label: `Young` },
        { val: suspended, cls: 'segment-suspended', label: `Suspended` },
        { val: learning, cls: 'segment-learning', label: `Learning` },
        { val: new_cards, cls: 'segment-new', label: `New` }
      ].forEach(seg => {
        const div = document.createElement('div');
        div.className = `segment ${seg.cls}`;
        div.style.width = pct(seg.val) + '%';
        div.title = `${seg.label}: ${seg.val}`; // tooltip text
        container.appendChild(div);
      });

      td.appendChild(container);
      dueTd.after(td);
    });
  });
}

initProgressBars()
