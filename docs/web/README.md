<!-- Copy of web/README.md for docs viewer -->

# Web (frontend)

Pequeno scaffold Next.js com autenticação JWT (login) e cliente Socket.IO.

Como testar:

```bash
cd web
npm install
npm run dev
```

Abra http://localhost:3000/login para entrar (usuário inicial: `admin` / senha `admin` se criado via bootstrap).

Notas:
- O frontend salva o JWT em `localStorage` como `jarvis_token` e envia o token ao conectar ao Socket.IO usando `auth: { token }`.
- Para desenvolvimento crie o usuário admin com:

```bash
# dentro do .venv
PYTHONPATH=. python3 scripts/bootstrap_db.py --create-admin admin admin
```

Visualização rápida (UI mockup):

![Mockup UI Jarvis](../images/ui-mockup.svg)
