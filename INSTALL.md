# INSTALL.md — Instruções completas de instalação

Este arquivo descreve os passos para preparar e executar o projeto Jarvis em uma máquina Ubuntu (local/self-hosted).

Pré-requisitos (Ubuntu)

- Python 3.10+ (recomendado)
- Node.js 16+ / npm
- git
- sudo privileges para instalar serviços do sistema

1) Clonar o repositório

```bash
git clone <repo-url> jarvis
cd jarvis
```

2) Preparar ambiente Python (virtualenv)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Nota: se você não tiver PostgreSQL disponível durante o desenvolvimento, o backend usará um fallback SQLite (`jarvis.db`). Em produção, configure `DATABASE_URL` para seu PostgreSQL.

3) Variáveis de ambiente recomendadas

Crie um arquivo `.env` na raiz ou exporte variáveis no shell. Exemplo mínimo:

```env
JARVIS_JWT_SECRET=uma-senha-muito-forte-aqui
DATABASE_URL=postgresql://jarvis:password@localhost:5432/jarvis
REDIS_URL=redis://localhost:6379/0
```

4) Rodar o backend (desenvolvimento)

```bash
source .venv/bin/activate
uvicorn main:asgi_app --host 0.0.0.0 --port 8000 --reload
```

5) Rodar o frontend (desenvolvimento)

```bash
cd web
npm install
npm run dev
```

6) Usar o instalador inteligente (opcional)

O instalador detecta CPU/RAM/DISK/GPU e sugere um conjunto de componentes.

```bash
# ver recomendações
bash scripts/installer.sh --components

# modo interativo avançado
bash scripts/installer.sh --advanced

# instalar automaticamente os componentes recomendados
bash scripts/installer.sh --auto

# instalar um componente específico
bash scripts/installer.sh --install redis

# testar sem executar comandos
bash scripts/installer.sh --auto --dry-run
```

7) Banco de dados e cache (PostgreSQL / Redis) — mínimo rápido

--

Inicializar banco e criar usuário admin (desenvolvimento)

Após instalar dependências e antes de rodar o backend, crie as tabelas e um usuário `admin` (modo dev):

```bash
# dentro do .venv
PYTHONPATH=. python3 scripts/bootstrap_db.py --create-admin admin admin
```

O script usará `DATABASE_URL` (Postgres) se configurado; caso contrário criará `jarvis.db` (SQLite) na raiz do projeto.

Verificar Ollama (opcional)

Se você pretende usar IA local, confirme que o Ollama está escutando (porta padrão 11434):

```bash
python3 - <<'PY'
import socket
try:
	s=socket.socket(); s.settimeout(1); s.connect(('localhost',11434)); print('Ollama reachable')
except Exception:
	print('Ollama unreachable')
PY
```

Instalar PostgreSQL e criar database/usuário (exemplo):

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo -u postgres createuser --pwprompt jarvis
sudo -u postgres createdb --owner=jarvis jarvis
```

Instalar Redis:

```bash
sudo apt install -y redis-server
sudo systemctl enable --now redis-server
```

8) Executar cliente de teste Socket.IO

```bash
python3 scripts/test_socketio_client.py "echo hello && sleep 1 && echo done"
```

9) Usar o `cli.sh`

Exemplos:

```bash
./cli.sh start
./cli.sh stop
./cli.sh status
./cli.sh installer --advanced
```

10) Produção (suggestions)

- Use um processo manager (systemd, supervisor, pm2) para iniciar `uvicorn` com workers.
- Configure HTTPS (NGINX reverse proxy, certificados Let's Encrypt).
- Configure variáveis de ambiente seguras e rotacione `JARVIS_JWT_SECRET` regularmente.

11) Segurança e considerações de privacidade

- O projeto emite comandos do sistema; seja cuidadoso com quem tem acesso ao servidor.
- A `conscience` placeholder (`core/conscience.py`) deve ser estendida para bloquear ações perigosas.
- Para produção, não use o armazenamento de usuários em memória; migre para PostgreSQL com senha forte.

12) Próximos passos técnicos

- Integrar Ollama/Llama3 local em `core/ai.py` para IA offline.
- Adicionar STT/TTS (Vosk, Coqui TTS) em `core/voice.py`.
- Proteger Socket.IO no backend validando o JWT no evento `connect`.

Se quiser, posso executar um `--dry-run` do `scripts/installer.sh` nesta máquina agora para mostrar as recomendações detectadas.
