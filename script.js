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
