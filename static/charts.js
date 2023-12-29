document.querySelectorAll('#table-of-contents a').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
  
      const target = document.querySelector(link.getAttribute('href'));
      target.scrollIntoView({ behavior: 'smooth' });
    });
  });