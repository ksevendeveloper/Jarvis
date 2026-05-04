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

    // Fetch GitHub stars and forks and render counters on the FAB
    (function(){
      var repoOwner = 'ksevendeveloper';
      var repoName = 'Jarvis';
      var storageKey = 'gh_stats_' + repoOwner + '_' + repoName;
      var cacheTtl = 15 * 60 * 1000; // 15 minutes

      function renderCounts(data){
        var a = document.querySelector('.github-fab');
        if(!a) return;
        var stars = data.stargazers_count || 0;
        var forks = data.forks_count || 0;
        var s = a.querySelector('.gh-stars');
        var f = a.querySelector('.gh-forks');
        if(!s){ s = document.createElement('span'); s.className = 'gh-count gh-stars'; a.appendChild(s); }
        if(!f){ f = document.createElement('span'); f.className = 'gh-count gh-forks'; a.appendChild(f); }
        s.textContent = stars.toLocaleString();
        f.textContent = forks.toLocaleString();
      }

      function fetchAndCache(){
        var url = 'https://api.github.com/repos/' + repoOwner + '/' + repoName;
        fetch(url).then(function(r){ if(!r.ok) throw new Error('GitHub API error'); return r.json(); })
        .then(function(json){
          try{ localStorage.setItem(storageKey, JSON.stringify({ts:Date.now(), data:json})); }catch(e){}
          renderCounts(json);
        }).catch(function(){
          // on error, try cached
          var cached = null;
          try{ cached = JSON.parse(localStorage.getItem(storageKey)); }catch(e){}
          if(cached && cached.data) renderCounts(cached.data);
        });
      }

      // use cache if fresh
      try{
        var cached = JSON.parse(localStorage.getItem(storageKey));
        if(cached && (Date.now() - cached.ts) < cacheTtl){ renderCounts(cached.data); }
        else { fetchAndCache(); }
      }catch(e){ fetchAndCache(); }
    })();