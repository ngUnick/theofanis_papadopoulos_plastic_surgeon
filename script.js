// Mobile nav toggle & basic utilities
(function(){
  const nav = document.querySelector('.navlinks');
  const toggle = document.querySelector('#menuToggle');
  if(toggle){
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
  }
  // Highlight active link
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.links a').forEach(a => {
    const href = a.getAttribute('href');
    if(href === path) a.classList.add('active');
  });
})();




// Live search with letter-accurate highlighting across titles & descriptions
(function () {
  const input = document.getElementById('procSearch');
  const sections = Array.from(document.querySelectorAll('.proc-section'));
  const resultCount = document.getElementById('resultCount');

  // Build cache of all cards
  const cards = [];
  sections.forEach(section => {
    section.querySelectorAll('.proc-grid .proc-card').forEach(card => {
      const titleEl = card.querySelector('.proc-title');
      const descEl  = card.querySelector('.proc-desc');
      cards.push({
        section,
        card,
        titleEl,
        descEl,
        titleText: titleEl?.textContent || '',
        descText:  descEl?.textContent  || ''
      });
    });
  });

  function escapeRegExp(str){
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function highlight(text, query){
    if(!query) return text;
    const pattern = new RegExp(escapeRegExp(query), 'gi'); // letter-to-letter, case-insensitive
    return text.replace(pattern, match => `<mark class="hl">${match}</mark>`);
  }

  function updateSectionVisibility() {
    sections.forEach(section => {
      const visibleCards = section.querySelectorAll('.proc-grid .proc-card:not([data-hidden="true"])').length;
      section.classList.toggle('is-hidden', visibleCards === 0);
    });
  }

  function onSearch(){
    const q = input.value.trim();
    let visible = 0;

    cards.forEach(item => {
      const { card, titleEl, descEl, titleText, descText } = item;

      // reset content to original
      titleEl.innerHTML = titleText;
      descEl.innerHTML  = descText;

      if(!q){
        card.style.display = '';
        card.removeAttribute('data-hidden');
        visible++;
        return;
      }

      const hay = (titleText + ' ' + descText).toLowerCase();
      const ok = hay.includes(q.toLowerCase());

      if(ok){
        titleEl.innerHTML = highlight(titleText, q);
        descEl.innerHTML  = highlight(descText, q);
        card.style.display = '';
        card.removeAttribute('data-hidden');
        visible++;
      }else{
        card.style.display = 'none';
        card.setAttribute('data-hidden','true');
      }
    });

    updateSectionVisibility();

    resultCount.textContent = q
      ? `${visible} αποτέλεσμα(τα) για «${q}»`
      : 'Εμφάνιση όλων των επεμβάσεων';
  }

  input.addEventListener('input', onSearch);

  // Optional: keyboard Esc clears search
  input.addEventListener('keydown', (e) => {
    if(e.key === 'Escape'){
      input.value = '';
      onSearch();
    }
  });

  // Initial layout check (no search)
  onSearch();
})();











// Mobile nav toggle & basic utilities
(function(){
  const nav = document.querySelector('.navlinks');
  const toggle = document.querySelector('#menuToggle');
  if (toggle && nav) {
    const links = nav.querySelector('.links');

    const setExpanded = (open) => {
      if (!toggle) return;
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    };

    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
      setExpanded(nav.classList.contains('open'));
    });

    // Close on escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        setExpanded(false);
      }
    });

    // Close if clicking outside the menu
    document.addEventListener('click', (e) => {
      if (!nav.contains(e.target) && nav.classList.contains('open')) {
        nav.classList.remove('open');
        setExpanded(false);
      }
    });

    // Close if we resize back above the burger breakpoint (1120px)
    const closeIfDesktop = () => {
      if (window.innerWidth > 1120 && nav.classList.contains('open')) {
        nav.classList.remove('open');
        setExpanded(false);
      }
    };
    window.addEventListener('resize', closeIfDesktop);
  }

  // Highlight active link
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path) a.classList.add('active');
  });
})();





// media.js
// (function () {
//   const q = document.getElementById('mediaSearch');
//   const count = document.getElementById('mediaCount');
//   const grid = document.getElementById('mediaGrid');
//   const cards = Array.from(grid.querySelectorAll('.media-card'));
//   const chips = Array.from(document.querySelectorAll('.chipbar .chip'));
//   let tag = 'all';

//   function applyFilter() {
//     const term = (q?.value || '').trim().toLowerCase();
//     let visible = 0;

//     cards.forEach(card => {
//       const matchesText = !term || (card.dataset.title || '').toLowerCase().includes(term);
//       const matchesTag = tag === 'all' || (card.dataset.tags || '').split(' ').includes(tag);
//       const show = matchesText && matchesTag;
//       card.style.display = show ? '' : 'none';
//       visible += show ? 1 : 0;
//     });

//     if (count) {
//       count.textContent = visible === cards.length
//         ? 'Εμφάνιση όλων των βίντεο'
//         : `Εμφάνιση ${visible} από ${cards.length} βίντεο`;
//     }
//   }

//   q?.addEventListener('input', applyFilter);

//   chips.forEach(c => {
//     c.addEventListener('click', () => {
//       chips.forEach(x => { x.classList.remove('is-active'); x.setAttribute('aria-selected', 'false'); });
//       c.classList.add('is-active'); c.setAttribute('aria-selected', 'true');
//       tag = c.dataset.mediaFilter || 'all';
//       applyFilter();
//     });
//   });

//   applyFilter();
// })();



// media.js
// (function () {
//   const cards = document.querySelectorAll('.media-card[data-ytid]');
//   cards.forEach(card => {
//     const id = card.getAttribute('data-ytid');
//     const img = card.querySelector('img.card-img');
//     if (!id || !img) return;
//     img.src = `https://img.youtube.com/vi/${id}/hqdefault.jpg`;
//     // Optional: 16:9 ratio via existing CSS classes; alt text already set in HTML.
//     img.referrerPolicy = 'no-referrer';
//     img.loading = 'lazy';
//     img.decoding = 'async';
//   });
// })();
