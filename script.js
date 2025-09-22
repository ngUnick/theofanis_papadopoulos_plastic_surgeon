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
