    (function(){
      var mq = window.matchMedia('(max-width:720px)');
      var menu = document.getElementById('menuItems');
      var toggle = document.getElementById('menuToggle');
      function update(){
        if(mq.matches){
          toggle.style.display='inline-block';
          menu.style.display='none';
          toggle.setAttribute('aria-expanded','false');
        } else {
          toggle.style.display='none';
          menu.style.display='flex';
        }
      }

      if (toggle) {
        toggle.addEventListener('click', function(){
          var shown = menu.style.display === 'block';
          menu.style.display = shown ? 'none' : 'block';
          toggle.setAttribute('aria-expanded', String(!shown));
        });
        mq.addListener(update);
        update();
      }
    })();