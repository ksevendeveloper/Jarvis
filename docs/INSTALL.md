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
