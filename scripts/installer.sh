#!/usr/bin/env bash
set -euo pipefail

# Instalador inteligente para Jarvis
# Detecta CPU, RAM, disco e GPU e recomenda um plano de instalação.
# Aceita flags: --auto, --advanced, --components, --install <name>, --dry-run

DRY_RUN=0
AUTO=0
ADVANCED=0

usage() {
  cat <<EOF
Usage: $0 [--auto] [--advanced] [--components] [--install <name>] [--dry-run]

Options:
  --auto         : Instala automaticamente os componentes recomendados (usa sudo quando necessário)
  --advanced     : Modo interativo avançado para escolher componentes manualmente
  --components   : Lista componentes detectados e recomendações
  --install NAME : Instala componente específico (postgres|redis|ollama|speech|backend)
  --dry-run      : Não executa ações, apenas mostra o que faria
EOF
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --auto) AUTO=1; shift ;;
    --advanced) ADVANCED=1; shift ;;
    --components) SHOW_COMPONENTS=1; shift ;;
    --install) INSTALL_NAME="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option $1"; usage; exit 1 ;;
  esac
done

info() { echo -e "[installer] $*"; }
dry() { if [ "$DRY_RUN" -eq 1 ]; then echo "[dry-run] $*"; else eval "$*"; fi }

detect_os() {
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "$NAME $VERSION_ID"
  else
    uname -srv
  fi
}

detect_cpu() { nproc --all || echo "1"; }
detect_mem_gb() { awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo || echo 0; }
detect_disk_gb() { df --output=avail -BG / | tail -1 | tr -d '\n' | sed 's/G//g' || echo 0; }
detect_gpu() {
  if command -v nvidia-smi >/dev/null 2>&1; then
    echo "nvidia"
  elif lspci | grep -i 'vga\|3d\|nvidia' >/dev/null 2>&1; then
    echo "possible"
  else
    echo "none"
  fi
}

OS=$(detect_os)
CPU=$(detect_cpu)
MEM_GB=$(detect_mem_gb)
DISK_GB=$(detect_disk_gb)
GPU=$(detect_gpu)

info "Detected OS: $OS"
info "CPU cores: $CPU"
info "Memory (MB): ${MEM_GB}MB"
info "Disk available (GB): ${DISK_GB}GB"
info "GPU: $GPU"

recommend() {
  # Base recommendations
  echo "Recommended components based on detected resources:"
  if [ "$MEM_GB" -lt 2000 ]; then
    echo " - Minimal: backend (FastAPI), redis (optional)"
  elif [ "$MEM_GB" -lt 8000 ]; then
    echo " - Standard: backend, postgresql, redis"
  else
    echo " - Full: backend, postgresql, redis, speech (STT/TTS)"
    if [ "$GPU" = "nvidia" ] || [ "$GPU" = "possible" ]; then
      echo " - Ollama / Llama3 recommended if disk and GPU available"
    fi
  fi
}

if [ "${SHOW_COMPONENTS:-0}" = 1 ]; then
  recommend
  exit 0
fi

do_install_postgres() {
  info "Installing PostgreSQL (apt)"
  dry "sudo apt update && sudo apt install -y postgresql postgresql-contrib"
}

do_install_redis() {
  info "Installing Redis (apt)"
  dry "sudo apt update && sudo apt install -y redis-server"
}

do_install_backend() {
  info "Installing backend dependencies (pip)"
  dry "python3 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt"
}

do_install_speech() {
  info "Installing speech dependencies (Vosk/Coqui placeholders)"
  dry "pip install vosk sounddevice numpy"
}

do_install_ollama() {
  info "Ollama installation is environment-specific. Printing instructions."
  echo "Please follow Ollama docs: https://ollama.ai/docs/"
}

if [ -n "${INSTALL_NAME:-}" ]; then
  case "$INSTALL_NAME" in
    postgres|postgresql) do_install_postgres ;;
    redis) do_install_redis ;;
    backend) do_install_backend ;;
    speech) do_install_speech ;;
    ollama) do_install_ollama ;;
    *) echo "Unknown component: $INSTALL_NAME"; exit 2 ;;
  esac
  exit 0
fi

if [ "$AUTO" -eq 1 ]; then
  info "Auto-install mode enabled. Will install recommended set."
  if [ "$MEM_GB" -lt 2000 ]; then
    info "Minimal install"
    do_install_backend
  elif [ "$MEM_GB" -lt 8000 ]; then
    do_install_backend
    do_install_postgres
    do_install_redis
  else
    do_install_backend
    do_install_postgres
    do_install_redis
    do_install_speech
    if [ "$GPU" != "none" ]; then
      info "GPU detected; recommending Ollama installation"
      do_install_ollama
    fi
  fi
  exit 0
fi

if [ "$ADVANCED" -eq 1 ]; then
  echo "Advanced interactive installer"
  echo "Detected resources: CPU=$CPU, MEM=${MEM_GB}MB, DISK=${DISK_GB}GB, GPU=$GPU"
  echo "Choose components to install (y/n):"
  read -rp "Install backend (FastAPI + deps)? [Y/n] " REPLY
  REPLY=${REPLY:-Y}
  if [[ "$REPLY" =~ ^[Yy]$ ]]; then do_install_backend; fi

  read -rp "Install PostgreSQL? [Y/n] " REPLY
  REPLY=${REPLY:-Y}
  if [[ "$REPLY" =~ ^[Yy]$ ]]; then do_install_postgres; fi

  read -rp "Install Redis? [Y/n] " REPLY
  REPLY=${REPLY:-Y}
  if [[ "$REPLY" =~ ^[Yy]$ ]]; then do_install_redis; fi

  read -rp "Install speech stack (Vosk/Coqui)? [y/N] " REPLY
  if [[ "$REPLY" =~ ^[Yy]$ ]]; then do_install_speech; fi

  if [ "$GPU" != "none" ]; then
    read -rp "Install Ollama (instructions)? [y/N] " REPLY
    if [[ "$REPLY" =~ ^[Yy]$ ]]; then do_install_ollama; fi
  fi
  exit 0
fi

echo "Run with --components to see recommended components, --auto to auto-install, or --advanced for manual selection."
