<!-------------------------------------------------
 This file is a copy of the repository README placed
 under docs/ so the docs viewer can serve it directly.
 Keep the root README.md as the source of truth and
 update it when needed; this copy can be refreshed by
 the developer or via a script.
--------------------------------------------------->

# Jarvis — Assistente Pessoal Self-Hosted

Jarvis é um assistente self-hosted projetado para rodar localmente em Ubuntu. Este repositório fornece:

- Backend em `FastAPI` com Socket.IO (ASGI) — orquestra ações do sistema e emite eventos em tempo real.
- Scaffold frontend em `web/` (Next.js) com autenticação JWT e cliente Socket.IO.
- Scripts de sistema em `scripts/` (instalador inteligente, utilitários, testes).
- Módulos core em `core/` para IA, voz e políticas (placeholders para integração futura).

- Arquitetura resumida
- `core/` — lógica do assistente, integração com IA local (Ollama/Llama3), `voice.py`, `conscience.py`.

![Arquitetura do Jarvis](images/architecture.svg)

> Versão: 0.1.0 — Autores: KSeven

Figura: Diagrama de arquitetura mostrando Next.js ↔ FastAPI ↔ Ollama / DB / Workers.
- `api/` — rotas REST e auth (`/api/auth/login`).
- `web/` — frontend Next.js (login, painel com eventos Socket.IO).
- `scripts/` — `installer.sh`, `run_command.sh`, `test_socketio_client.py`, entre outros.

Arquivo importantes
- `main.py` — aplicativo FastAPI + Socket.IO (ASGI).
- `cli.sh` — CLI para iniciar/parar, instalar, logs, etc.
- `scripts/installer.sh` — instalador inteligente (auto/advanced/dry-run).
- `api/auth.py` — endpoint `POST /api/auth/login` (JWT). Use `scripts/bootstrap_db.py` para criar usuário admin (dev).

Instalação e execução (resumo)

1) Dependências Python (virtualenv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crie o usuário admin (modo dev) após instalar dependências:

```bash
# dentro do venv
PYTHONPATH=. python3 scripts/bootstrap_db.py --create-admin admin admin
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

Observações adicionais
- O backend tentará usar `DATABASE_URL` (Postgres) se definido; caso contrário, o sistema faz fallback para um arquivo SQLite `jarvis.db` (útil para desenvolvimento).
- O `core/ai.JarvisAI` tenta se comunicar com Ollama via HTTP (por padrão `http://localhost:11434`). Configure `OLLAMA_HOST` e `OLLAMA_MODEL` via variáveis de ambiente se necessário.

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

Para instruções completas de instalação e exemplos de configuração, veja `INSTALL.md`.
# Jarvis — Assistente Pessoal Self-Hosted

Este documento traz a versão em `docs/` do README principal, pensado para visualização no site de documentação.

Jarvis é um assistente self-hosted projetado para rodar localmente em Ubuntu. Este repositório fornece:

- Backend em `FastAPI` com Socket.IO (ASGI) — orquestra ações do sistema e emite eventos em tempo real.
- Scaffold frontend em `web/` (Next.js) com autenticação JWT e cliente Socket.IO.
- Scripts de sistema em `scripts/` (instalador inteligente, utilitários, testes).
- Módulos core em `core/` para IA, voz e políticas (placeholders para integração futura).

Instalação rápida

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python3 scripts/bootstrap_db.py --create-admin admin admin
```

Execução em dev

```bash
uvicorn main:asgi_app --host 0.0.0.0 --port 8000 --reload
cd web && npm install && npm run dev
```

Observações importantes

- O backend tenta usar `DATABASE_URL` (Postgres) se definido; caso contrário faz fallback para `sqlite:///./jarvis.db`.
- O `core/ai.JarvisAI` usa Ollama via HTTP por padrão `http://localhost:11434`.

Veja também: [INSTALL.md](INSTALL.md) e [Checklist.md](Checklist.md).
