(() => {
  const files = [
    {label: 'README', path: 'README.md'},
    {label: 'INSTALL', path: 'INSTALL.md'},
    {label: 'Checklist', path: 'Checklist.md'},
    {label: 'AGENTS', path: 'AGENTS.md'},
    {label: 'Web README', path: 'web/README.md'}
  ];

  const fileListEl = document.getElementById('fileList');
  const docEl = document.getElementById('doc');
  const spinner = document.getElementById('spinner');
  const toggleMenu = document.getElementById('toggleMenu');
  const sidebar = document.getElementById('sidebar');

  let currentPath = null;
  let lastContent = null;

  function createLink(item){
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '?file=' + encodeURIComponent(item.path);
    a.textContent = item.label;
    a.addEventListener('click', (e)=>{
      e.preventDefault();
      loadAndShow(item.path, true);
      if(window.innerWidth < 900) sidebar.style.display = 'none';
    });
    li.appendChild(a);
    return li;
  }

  files.forEach(f=> fileListEl.appendChild(createLink(f)));

  toggleMenu.addEventListener('click', ()=>{
    sidebar.style.display = (sidebar.style.display === 'none' || !sidebar.style.display) ? 'block' : 'none';
  });

  async function fetchCandidate(path){
    // try ../path then /path
    const candidates = ['../' + path, '/' + path, path];
    for(const p of candidates){
      try{
        const res = await fetch(p, {cache: 'no-store'});
        if(res.ok) return {text: await res.text(), src: p};
      }catch(e){/* ignore */}
    }
    throw new Error('Não encontrou: ' + path);
  }

  async function loadAndShow(path, pushState){
    spinner.style.display = 'block';
    try{
      const {text, src} = await fetchCandidate(path);
      if(text === lastContent && currentPath === path){
        spinner.style.display = 'none';
        return;
      }
      lastContent = text;
      currentPath = path;
      const html = marked.parse(text);
      docEl.innerHTML = html;
      document.querySelectorAll('pre code').forEach((el)=>hljs.highlightElement(el));
      if(pushState) history.pushState({path}, '', '?file=' + encodeURIComponent(path));
      spinner.style.display = 'none';
    }catch(err){
      spinner.textContent = 'Erro ao carregar: ' + err.message;
    }
  }

  function getQueryFile(){
    const params = new URLSearchParams(location.search);
    return params.get('file');
  }

  // initial
  const q = getQueryFile();
  if(q){
    loadAndShow(q, false);
  }else{
    loadAndShow('README.md', false);
  }

  // polling: atualizar se o MD mudar (útil durante edição local)
  setInterval(async ()=>{
    if(!currentPath) return;
    try{
      const {text} = await fetchCandidate(currentPath);
      if(text !== lastContent){
        lastContent = text;
        const html = marked.parse(text);
        docEl.innerHTML = html;
        document.querySelectorAll('pre code').forEach((el)=>hljs.highlightElement(el));
      }
    }catch(e){/* ignore polling errors */}
  }, 5000);

  // handle back/forward
  window.addEventListener('popstate', (ev)=>{
    const p = getQueryFile() || 'README.md';
    loadAndShow(p, false);
  });
})();
