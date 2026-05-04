<!-------------------------------------------------
 Copy of root INSTALL.md placed under docs/ for viewer
--------------------------------------------------->

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

Fluxo de processamento

![Fluxo de mensagens e execução](images/workflow.svg)

Figura: Como uma mensagem do usuário atravessa o sistema — passa pela `conscience`, é processada pela IA (Ollama) e pode disparar execução de comandos.

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

... (mantido o restante do conteúdo do INSTALL.md na raiz)
# INSTALL — Guia de instalação (docs)

Este documento é uma versão para a área `docs/` de `INSTALL.md`. Mantive os passos essenciais para preparar o ambiente Ubuntu.

Pré-requisitos

- Python 3.10+
- Node.js 16+ / npm
- git
- sudo (para instalar serviços do sistema)

Passos principais

1. Clonar o repositório

```bash
git clone <repo-url> jarvis
cd jarvis
```

2. Preparar ambiente Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Inicializar banco (dev)

```bash
# dentro do venv
PYTHONPATH=. python3 scripts/bootstrap_db.py --create-admin admin admin
```

4. Rodar backend e frontend (dev)

```bash
uvicorn main:asgi_app --host 0.0.0.0 --port 8000 --reload
cd web && npm install && npm run dev
```

Variáveis de ambiente importantes

```
JARVIS_JWT_SECRET=__REPLACE_ME__
DATABASE_URL=postgresql://jarvis:password@localhost:5432/jarvis
REDIS_URL=redis://localhost:6379/0
```

Verifique também o instalador: `bash scripts/installer.sh --components`.
