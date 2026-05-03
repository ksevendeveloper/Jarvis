# Jarvis — Assistente Pessoal Self-Hosted

Jarvis é um assistente self-hosted projetado para rodar localmente em Ubuntu. Este repositório fornece:

- Backend em `FastAPI` com Socket.IO (ASGI) — orquestra ações do sistema e emite eventos em tempo real.
- Scaffold frontend em `web/` (Next.js) com autenticação JWT e cliente Socket.IO.
- Scripts de sistema em `scripts/` (instalador inteligente, utilitários, testes).
- Módulos core em `core/` para IA, voz e políticas (placeholders para integração futura).

Arquitetura resumida
- `core/` — lógica do assistente, integração com IA local (Ollama/Llama3), `voice.py`, `conscience.py`.
- `api/` — rotas REST e auth (`/api/auth/login`).
- `web/` — frontend Next.js (login, painel com eventos Socket.IO).
- `scripts/` — `installer.sh`, `run_command.sh`, `test_socketio_client.py`, entre outros.

Arquivo importantes
- [main.py](main.py) — aplicativo FastAPI + Socket.IO (ASGI).
- [cli.sh](cli.sh) — CLI para iniciar/parar, instalar, logs, etc.
- [scripts/installer.sh](scripts/installer.sh) — instalador inteligente (auto/advanced/dry-run).
- [api/auth.py](api/auth.py) — endpoint `POST /api/auth/login` (JWT). Usuário padrão: `admin` / `admin` (in-memory).

Instalação e execução (resumo)

1) Dependências Python (virtualenv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Executar backend em desenvolvimento:

```bash
uvicorn main:asgi_app --host 0.0.0.0 --port 8000 --reload
```

3) Frontend (Next.js) — pasta `web/`:

```bash
cd web
npm install
npm run dev
```

4) Teste de integração simples (cliente de teste Socket.IO):

```bash
python3 scripts/test_socketio_client.py "echo hello && sleep 1 && echo done"
```

Instalador inteligente

Use `scripts/installer.sh` para detectar recursos do sistema e instalar componentes recomendados.

Exemplos:

```bash
# Mostrar recomendações
bash scripts/installer.sh --components

# Modo interativo avançado
bash scripts/installer.sh --advanced

# Instalar automaticamente o conjunto recomendado (usa sudo quando necessário)
bash scripts/installer.sh --auto

# Instalar um componente específico
bash scripts/installer.sh --install redis

# Dry-run (não executa comandos)
bash scripts/installer.sh --auto --dry-run
```

Autenticação e segurança

- Endpoint de login: `POST /api/auth/login` (JSON: `{ "username":"...", "password":"..." }`). Retorna JWT.
- O scaffold frontend salva o token no `localStorage` como `jarvis_token` e o utiliza para conectar ao Socket.IO.
- Configure a variável de ambiente `JARVIS_JWT_SECRET` para um valor forte antes de colocar em produção.

Endpoints importantes
- `GET /api/health` — health check
- `POST /api/execute` — executar comando shell (body JSON {"command":"ls -la"}) — emite eventos Socket.IO: `executing`, `success`, `error`.

Práticas e próximos passos recomendados
- Proteger o Socket.IO no backend validando o JWT no `connect`.
- Substituir o armazenamento in-memory de usuários por PostgreSQL e implementar registro/gestão de usuários.
- Integrar Ollama/Llama3 local em `core/ai.py` para processamento de prompts offline.
- Implementar STT/TTS local (Vosk/Coqui) em `core/voice.py`.
- Criar unit tests e CI, e adicionar instruções de deployment (systemd, Docker).

Para instruções completas de instalação e exemplos de configuração, veja `INSTALL.md`.
 
