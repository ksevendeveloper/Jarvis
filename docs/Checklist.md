# Checklist do Jarvis — Recursos e Status (docs)

Versão resumida do `Checklist.md` para a documentação do projeto.

Principais pontos
- Backend: `FastAPI` + `Socket.IO` com validação JWT no `connect`.
- Execução: `POST /api/execute` protegido por JWT e `conscience` + allowlist.
- Frontend: scaffold Next.js com login JWT e painel básico.

O que falta
- Integração Ollama completa e STT/TTS.
- Persistência avançada com migrations (Alembic) e Redis.
- Segurança de produção (HTTPS, rate limiting, refresh tokens).

Checklist rápido

- [x] Backend básico e endpoints principais
- [x] Instalador inteligente e CLI
- [x] Efeito visual local (`fx-on` / `fx-off`)
- [ ] Migrations/Alembic aplicadas
- [ ] Dockerfile e CI

Consulte o `Checklist.md` raiz para detalhamento técnico.
