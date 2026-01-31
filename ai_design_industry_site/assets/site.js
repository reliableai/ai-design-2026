(function(){
  const btn = document.querySelector('[data-toggle="nav"]');
  const nav = document.querySelector('[data-navlinks]');
  if(btn && nav){
    btn.addEventListener('click', () => nav.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      const within = nav.contains(e.target) || btn.contains(e.target);
      if(!within) nav.classList.remove('open');
    });
  }
  // Active link highlighting
  const path = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  document.querySelectorAll('[data-navlinks] a').forEach(a => {
    const href = (a.getAttribute('href') || '').toLowerCase();
    if(href === path) a.classList.add('active');
  });
})();