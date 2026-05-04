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
