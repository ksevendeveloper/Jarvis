# Jarvis — Assistente Pessoal Self-Hosted

Backend minimal com FastAPI + Socket.IO (ASGI). Estrutura inicial para orquestrar IA local, comandos do sistema e um painel web.

Instalação rápida (virtualenv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Executar em modo desenvolvimento:

```bash
uvicorn main:asgi_app --host 0.0.0.0 --port 8000 --reload
```

Endpoints importantes:
- `GET /api/health` — health check
- `POST /api/execute` — executar comando shell (body JSON {"command":"ls -la"})

Socket.IO:
- Conectar ao endpoint Socket.IO do servidor (ponto ASGI montado automaticamente). Eventos emitidos: `status`, `executing`, `success`, `error`.

Próximos passos sugeridos:
- Scaffold frontend React/Next.js em `web/`
- Integrar Ollama / Llama3 em `core/ai.py`
- Adicionar integração com PostgreSQL e Redis
 
