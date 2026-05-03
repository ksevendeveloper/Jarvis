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

Instalador inteligente:

O projeto inclui `scripts/installer.sh` que detecta CPU, RAM, disco e GPU e recomenda um plano de instalação.

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

# Rodar em dry-run para ver os comandos sem executar
bash scripts/installer.sh --auto --dry-run
```

CLI do sistema:

O `cli.sh` foi refatorado para aceitar comandos e opções completas. Exemplos:

```bash
./cli.sh start
./cli.sh stop
./cli.sh installer --advanced
./cli.sh install postgres
./cli.sh logs
```

Voz e "conscience":

Adicionados placeholders em `core/voice.py` e `core/conscience.py` para futuras integrações de STT/TTS e políticas de segurança.


Endpoints importantes:
- `GET /api/health` — health check
- `POST /api/execute` — executar comando shell (body JSON {"command":"ls -la"})

Socket.IO:
- Conectar ao endpoint Socket.IO do servidor (ponto ASGI montado automaticamente). Eventos emitidos: `status`, `executing`, `success`, `error`.

Próximos passos sugeridos:
- Scaffold frontend React/Next.js em `web/`
- Integrar Ollama / Llama3 em `core/ai.py`
- Adicionar integração com PostgreSQL e Redis
 
