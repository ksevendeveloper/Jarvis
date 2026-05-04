# Checklist do Jarvis — Recursos e Status

Este documento lista as funcionalidades esperadas de um assistente "Jarvis" completo, o que já implementamos neste repositório e o que ainda falta para chegarmos a um Jarvis operacional.

Diagramas rápidos

![Arquitetura do Jarvis](docs/images/architecture.svg)

![Fluxo de mensagens e execução](docs/images/workflow.svg)

UI (mockup):

![Mockup UI Jarvis](docs/images/ui-mockup.svg)

Sumário rápido
- O que temos (implementado / parcial): backend FastAPI + Socket.IO com JWT no `connect`, endpoint `/api/execute` com JWT obrigatório + policy/allowlist, instalador inteligente (`scripts/installer.sh`), CLI (`cli.sh`) incluindo `fx-on/fx-off`, scaffold web Next.js com login JWT e efeito visual de atividade, testes automatizados básicos (`pytest`), unit file `systemd`, scripts utilitários e documentação (`README.md`, `INSTALL.md`).
- O que falta (principais itens): integração IA local completa (Ollama), STT/TTS funcional, persistência avançada (migrations/Alembic + Redis real), segurança de produção (HTTPS/rate limit/refresh token), auditoria aprofundada e controles avançados de hardware.

Detalhamento por área

1) Core IA
- Objetivo: integrar modelo local (Ollama / Llama3), gerenciar contexto, memória de conversação, ferramentas e prompt-engineering.
  - Status: Parcial (placeholder `core/ai.py` existe, mas sem integração com Ollama).
  - Falta: integração com Ollama, gerenciamento de sessões/contexts, pipelines de prompts, caching de respostas.

2) Voz (STT/TTS)
- Objetivo: capturar microfone, transcrever (STT), interpretar comandos, responder por voz (TTS) e sincronizar com UI (animações de fala/escuta).
  - Status: Placeholder (`core/voice.py`) — não funcional.
  - Falta: integrar Vosk/Coqui/Whisper local para STT, Coqui/VITS/etc para TTS, gerenciamento de dispositivos de áudio, permissões e testes.

3) Controle do Sistema
- Objetivo: executar comandos seguros, gerenciar serviços, acesso a hardware (microfone, câmera, GPIO), agendamento e automações.
  - Status: Implementado parcialmente — `POST /api/execute` exige JWT, valida comando por `conscience` + allowlist (`JARVIS_ALLOWED_COMMANDS`), executa via subprocess e emite eventos Socket.IO; `scripts/run_command.sh` e `cli.sh` fornecem utilitários.
  - Falta: sandboxing mais forte, políticas por role, auditoria detalhada por usuário e drivers de hardware específicos.

4) Comunicação em tempo real
- Objetivo: eventos em tempo real entre backend e frontend (Socket.IO), notificação de estados (`listening`, `thinking`, `executing`, `success`, `error`).
  - Status: Implementado — `socketio.AsyncServer` e emissões (`executing`, `success`, `error`, `status`); cliente de teste em `scripts/test_socketio_client.py` e frontend conecta com `socket.io-client`.
  - Falta: eventos avançados (`listening`/`thinking`), reconexão com métricas e políticas CORS de produção.

5) Web UI
- Objetivo: painel moderno (React/Next.js) que mostra eventos, aceita comandos por UI, autenticação, perfil de usuário e configurações.
  - Status: Scaffold funcional em `web/` com `login` (salva JWT), dashboard de eventos e efeito visual de estado em tempo real.
  - Falta: páginas de configuração, tela de execução de comandos, proteção de rotas (SSR), gerenciamento de usuários, UX polish e assets/ícones.

6) Persistência e Cache
- Objetivo: PostgreSQL para usuários, históricos, configurações; Redis para cache, filas e pub/sub.
  - Status: Dependências mencionadas em `requirements.txt` e `scripts/installer.sh` suporta instalação; não integrado ao código.
  - Falta: implementar camada de banco (`sqlalchemy`/`alembic`), migrations, integração Redis para pub/sub/locks.

7) Autenticação e Segurança
- Objetivo: login, roles, refresh tokens, proteção de endpoints, TLS/HTTPS, firewall.
  - Status: `POST /api/auth/login` com JWT e usuários via SQLAlchemy (SQLite fallback/Postgres via `DATABASE_URL`), JWT validado no Socket.IO `connect`, `/api/execute` protegido por JWT.
  - Falta: refresh tokens, força de senha/política, HTTPS, CORS restritivo por ambiente, rate limiting e rotação automatizada de segredos.

8) Conscience / Segurança da Ação
- Objetivo: avaliar e bloquear ações perigosas, políticas de consentimento e limites por usuário.
  - Status: Integrado ao `/api/execute` com bloqueio de padrões perigosos e retorno de motivo.
  - Falta: regras mais abrangentes, policy por perfil, logging estruturado e alertas.

9) Instalador & CLI
- Objetivo: instalação automática baseada em hardware; CLI de controle do serviço.
  - Status: Implementado — `scripts/installer.sh` (auto/advanced/dry-run), `cli.sh` (start/stop/install/logs/status/fx-on/fx-off) e efeito visual desktop (`scripts/jarvis_fx.py`).
  - Falta: testes de instalação em múltiplas distros e opções de rollback.

10) Integrações externas
- Objetivo: integração com calendar, e-mail, home automation (MQTT), sensores, APIs externas.
  - Status: Não implementado (arquitetura pronta para adicionar adaptadores).
  - Falta: adaptadores e autenticações para cada serviço.

11) Observabilidade e Testes
- Objetivo: logs estruturados, métricas (Prometheus), tracing, testes unitários/integrados e CI.
  - Status: Logs básicos via `nohup`/arquivos e testes automatizados iniciais com `pytest` (health/login/execute).
  - Falta: logging estruturado, métricas, tracing, ampliar cobertura e pipeline CI.

12) Deploy e Operação
- Objetivo: deployment robusto (Docker, systemd, orquestração), backups e recuperação.
  - Status: Parcial — unit file `deploy/systemd/jarvis.service` + instruções em `INSTALL.md`.
  - Falta: Dockerfile/imagens, NGINX+TLS, backup/restore e hardening operacional.

Checklist resumida (checkboxes)

- [x] Backend FastAPI + Socket.IO básico (`main.py`)
- [x] Endpoint `/api/execute` que emite eventos Socket.IO
- [x] `scripts/installer.sh` — instalador inteligente (auto/advanced/dry-run)
- [x] `cli.sh` — CLI refatorado (start/stop/install/logs/status)
- [x] Scaffold web Next.js com login JWT e dashboard básico
- [x] Auth endpoint `POST /api/auth/login` (JWT) — DB-backed via SQLAlchemy
- [x] Placeholders `core/voice.py` e `core/conscience.py`
- [x] `scripts/test_socketio_client.py` — cliente de teste
- [x] `README.md` e `INSTALL.md`
- [x] Validação JWT no Socket.IO `connect` (token verificado, room `user:<username>`)
- [x] `/api/execute` protegido por JWT + allowlist + policy (`conscience`)
- [x] Efeito visual local de atividade (`./cli.sh fx-on` / `./cli.sh fx-off`)
- [x] Testes automatizados iniciais com `pytest`
- [x] Unidade `systemd` para backend (`deploy/systemd/jarvis.service`)
- [x] Integração Ollama / Llama3 local (cliente HTTP implementado; ajuste conforme endpoint)
- [ ] STT/TTS funcional (Vosk/Coqui/Whisper/Coqui TTS)
- [ ] Persistência completa (PostgreSQL + migrations) — SQLAlchemy models implemented; fallback SQLite + bootstrap script added
- [ ] Integração Redis (pub/sub, filas)
- [ ] Segurança: HTTPS, CORS, rate limiting, secrets management
- [ ] Role-based access, refresh tokens, user management
- [ ] Sandboxing avançado e policies por role antes de executar comandos
- [ ] Tests unitários/integrados e CI
- [ ] Dockerfile / deployment scripts adicionais
- [ ] Observability: metrics, tracing, structured logs
- [ ] Integrations: calendar, home automation, email, external APIs

Como proceder
- Prioridade inicial sugerida:
  1. Migrar store para PostgreSQL e adicionar migrations (Alembic).
  2. Reforçar segurança (refresh tokens, HTTPS, rate limiting).
  3. Implementar STT/TTS e integrar em `core/voice.py`.
  4. Expandir `conscience` para regras e auditoria antes da execução.
  5. Criar Dockerfile e pipeline CI para deploy contínuo.

Implementação status: adicionei scaffold Alembic (`alembic/`), primeira migration inicial (`alembic/versions/0001_initial.py`), modelos para `RefreshToken` e endpoints básicos de refresh em `api/auth.py`, e um rate-limiter simples em `api/ratelimit.py`. Também adicionei `VERSION`/`AUTHORS` e `scripts/generate_docs_metadata.py` e `docs/metadata.json` para a página de documentação dinâmica.

O arquivo `Checklist.md` foi atualizado com o estado atual. Quer que eu comece pela prioridade 1 (Alembic + Postgres) ou outra tarefa?
