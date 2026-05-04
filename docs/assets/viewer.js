(() => {
  // URL Base para buscar os arquivos raw do seu repositório no GitHub
const REPO_RAW_URL = 'https://raw.githubusercontent.com/ksevendeveloper/Jarvis/main';

  const files = [
    {label: 'README', path: '/README.md'},
    {label: 'INSTALL', path: '/INSTALL.md'},
    {label: 'CHECKLIST', path: '/Checklist.md'}
  ];

  const fileListEl = document.getElementById('fileList');
  const docEl = document.getElementById('doc');
  const spinner = document.getElementById('spinner');
  const toggleMenu = document.getElementById('toggleMenu');
  const sidebar = document.getElementById('sidebar');
  const metaBox = document.getElementById('meta-block');

  let currentPath = null;
  let lastContent = null;

  // Renderiza a lista de links lateral
  function createLink(item){
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '?file=' + encodeURIComponent(item.path);
    a.textContent = item.label;
    a.addEventListener('click', (e)=>{
      e.preventDefault();
      loadAndShow(item.path, true);
      // Fecha o menu em telas pequenas após clicar
      if(window.innerWidth < 900 && sidebar) sidebar.style.display = 'none';
    });
    li.appendChild(a);
    return li;
  }

  if (fileListEl) {
    files.forEach(f => fileListEl.appendChild(createLink(f)));
  }

  if (toggleMenu && sidebar) {
    toggleMenu.addEventListener('click', ()=>{
      sidebar.style.display = (sidebar.style.display === 'none' || !sidebar.style.display) ? 'block' : 'none';
    });
  }

  // Busca o conteúdo diretamente do GitHub Raw
async function fetchCandidate(path){
  const url = REPO_RAW_URL + path;
  console.log("Tentando carregar:", url); // Isso mostrará o link exato no console
  
  try {
    const res = await fetch(url, { cache: 'no-store' });
    if(res.ok) return { text: await res.text(), src: url };
    
    // Se der 404, o erro será detalhado aqui
    throw new Error(`Erro ${res.status}: Não encontrado em ${url}`);
  } catch(e) {
    console.error("Falha no fetch:", e.message);
    throw e;
  }
}

  async function loadAndShow(path, pushState){
    if (!spinner || !docEl) return;
    spinner.style.display = 'block';
    
    try {
      const {text} = await fetchCandidate(path);
      
      // Evita re-renderizar se o conteúdo for idêntico
      if(text === lastContent && currentPath === path){
        spinner.style.display = 'none';
        return;
      }

      lastContent = text;
      currentPath = path;
      
      // Converte Markdown para HTML (Certifique-se que a lib 'marked' está carregada no HTML)
      docEl.innerHTML = marked.parse(text);

      // Atualiza link ativo no menu
      document.querySelectorAll('#fileList a').forEach(a => a.classList.remove('active'));
      const active = document.querySelector(`#fileList a[href="?file=${encodeURIComponent(path)}"]`);
      if(active) active.classList.add('active');

      // Syntax highlight para os blocos de código
      if (typeof hljs !== 'undefined') {
        document.querySelectorAll('pre code').forEach((el) => hljs.highlightElement(el));
      }
      
      if(pushState) history.pushState({path}, '', '?file=' + encodeURIComponent(path));
      spinner.style.display = 'none';
    } catch(err) {
      spinner.style.display = 'none';
      docEl.innerHTML = `<div class="error-msg" style="color: #ff4d4d; padding: 20px;">
        <strong>Erro ao carregar:</strong> ${err.message}<br>
        Verifique se o arquivo ${path} existe no repositório.
      </div>`;
    }
  }

  function getQueryFile(){
    const params = new URLSearchParams(location.search);
    return params.get('file');
  }

  // Inicialização: Tenta carregar do parâmetro da URL ou o README padrão
  const initialFile = getQueryFile() || '/README.md';
  loadAndShow(initialFile, false);

  // Carrega metadados (Versão/Autores) se o arquivo existir na raiz do repositório
  fetch(`${REPO_RAW_URL}/metadata.json`).then(r => r.json()).then(md => {
    if (metaBox) {
      metaBox.innerHTML = `<strong>Versão:</strong> ${md.version} | <strong>Autores:</strong> ${(md.authors || []).join(', ')}`;
    }
  }).catch(() => { /* metadata.json opcional */ });

  // Polling: Atualiza a cada 60 segundos (GitHub Raw tem cache e rate limits)
  setInterval(async () => {
    if(!currentPath) return;
    try {
      const {text} = await fetchCandidate(currentPath);
      if(text !== lastContent){
        lastContent = text;
        docEl.innerHTML = marked.parse(text);
        if (typeof hljs !== 'undefined') {
          document.querySelectorAll('pre code').forEach((el) => hljs.highlightElement(el));
        }
      }
    } catch(e) {}
  }, 60000);

  // Navegação pelos botões de avançar/voltar do browser
  window.addEventListener('popstate', () => {
    const p = getQueryFile() || '/README.md';
    loadAndShow(p, false);
  });
})();