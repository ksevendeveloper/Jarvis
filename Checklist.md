# Checklist do Jarvis — Recursos e Status

Este documento lista as funcionalidades esperadas de um assistente "Jarvis" completo, o que já implementamos neste repositório e o que ainda falta para chegarmos a um Jarvis operacional.

Sumário rápido
- O que temos (implementado / parcial): backend FastAPI + Socket.IO, endpoint `/api/execute`, instalador inteligente (`scripts/installer.sh`), CLI (`cli.sh`), scaffold web Next.js com login JWT, placeholders em `core/` (voz/conscience), scripts utilitários e documentação básica (`README.md`, `INSTALL.md`).
- O que falta (principais itens): integração IA local (Ollama), STT/TTS funcional, persistência (PostgreSQL/Redis fully integrated), validação JWT no Socket.IO, segurança/HTTPS, deploy (systemd/Docker), testes, auditoria e controles avançados de hardware.

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
  - Status: Implementado parcialmente — `POST /api/execute` executa comandos via subprocess e emite eventos Socket.IO; `scripts/run_command.sh` e `cli.sh` fornecem utilitários básicos.
  - Falta: autorização/escopo por comando, sandboxing/limitação, verificação de segurança antes de execução (usar `conscience`), logs/auditoria por usuário, drivers de hardware específicos.

4) Comunicação em tempo real
- Objetivo: eventos em tempo real entre backend e frontend (Socket.IO), notificação de estados (`listening`, `thinking`, `executing`, `success`, `error`).
  - Status: Implementado — `socketio.AsyncServer` e emissões (`executing`, `success`, `error`, `status`); cliente de teste em `scripts/test_socketio_client.py` e frontend conecta com `socket.io-client`.
  - Falta: validar token JWT no `connect`, escopos por socket, reconexão e políticas de CORS/segurança.

5) Web UI
- Objetivo: painel moderno (React/Next.js) que mostra eventos, aceita comandos por UI, autenticação, perfil de usuário e configurações.
  - Status: Scaffold inicial em `web/` com `login` (salva JWT) e dashboard básico recebendo eventos.
  - Falta: páginas de configuração, tela de execução de comandos, proteção de rotas (SSR), gerenciamento de usuários, UX polish e assets/ícones.

6) Persistência e Cache
- Objetivo: PostgreSQL para usuários, históricos, configurações; Redis para cache, filas e pub/sub.
  - Status: Dependências mencionadas em `requirements.txt` e `scripts/installer.sh` suporta instalação; não integrado ao código.
  - Falta: implementar camada de banco (`sqlalchemy`/`alembic`), migrations, integração Redis para pub/sub/locks.

7) Autenticação e Segurança
- Objetivo: login, roles, refresh tokens, proteção de endpoints, TLS/HTTPS, firewall.
  - Status: Endpoint básico `POST /api/auth/login` com JWT; in-memory user store (`admin:admin`), passlib para hashing.
  - Falta: validação de JWT no Socket.IO, refresh tokens, armazenamento seguro de secrets, força de senhas, HTTPS, políticas CORS restritivas, rate limiting.

8) Conscience / Segurança da Ação
- Objetivo: avaliar e bloquear ações perigosas, políticas de consentimento e limites por usuário.
  - Status: Placeholder `core/conscience.py` com checagem simples por padrões proibidos.
  - Falta: regras compreensivas, integração antes de executar comandos, logging e alertas.

9) Instalador & CLI
- Objetivo: instalação automática baseada em hardware; CLI de controle do serviço.
  - Status: Implementado — `scripts/installer.sh` (auto/advanced/dry-run) e `cli.sh` (start/stop/install/logs/status etc.).
  - Falta: testes de instalação em múltiplas distros, integração com systemd/Docker, opções de rollback.

10) Integrações externas
- Objetivo: integração com calendar, e-mail, home automation (MQTT), sensores, APIs externas.
  - Status: Não implementado (arquitetura pronta para adicionar adaptadores).
  - Falta: adaptadores e autenticações para cada serviço.

11) Observabilidade e Testes
- Objetivo: logs estruturados, métricas (Prometheus), tracing, testes unitários/integrados e CI.
  - Status: Logs básicos via `nohup` e arquivos; não há métricas ou testes.
  - Falta: adicionar logging estruturado, métricas, testes automatizados e pipeline CI.

12) Deploy e Operação
- Objetivo: deployment robusto (Docker, systemd, orquestração), backups e recuperação.
  - Status: Não implementado.
  - Falta: `Dockerfile`, imagens, systemd unit files, documentação de deploy seguro.

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
- [x] Integração Ollama / Llama3 local (cliente HTTP implementado; ajuste conforme endpoint)
- [ ] STT/TTS funcional (Vosk/Coqui/Whisper/Coqui TTS)
- [ ] Persistência completa (PostgreSQL + migrations) — SQLAlchemy models implemented; fallback SQLite + bootstrap script added
- [ ] Integração Redis (pub/sub, filas)
- [ ] Segurança: HTTPS, CORS, rate limiting, secrets management
- [ ] Role-based access, refresh tokens, user management
- [ ] Sandboxing e policies antes de executar comandos (conscience)
- [ ] Tests unitários/integrados e CI
- [ ] Dockerfile / systemd / deployment scripts
- [ ] Observability: metrics, tracing, structured logs
- [ ] Integrations: calendar, home automation, email, external APIs

Como proceder
- Prioridade inicial sugerida:
  1. Migrar store para PostgreSQL e adicionar migrations (Alembic).
  2. Reforçar segurança (refresh tokens, HTTPS, rate limiting).
  3. Implementar STT/TTS e integrar em `core/voice.py`.
  4. Expandir `conscience` para regras e auditoria antes da execução.
  5. Criar Dockerfile / systemd unit para deploy.

O arquivo `Checklist.md` foi atualizado com o estado atual. Quer que eu comece pela prioridade 1 (Alembic + Postgres) ou outra tarefa?
