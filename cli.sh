#!/bin/bash

set -euo pipefail

# CLI avançado para Jarvis
# Uso: ./cli.sh [command] [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JARVIS_DIR="${JARVIS_DIR:-$SCRIPT_DIR}"
RUNTIME_DIR="${RUNTIME_DIR:-$JARVIS_DIR/.runtime}"
LOG_FILE="$RUNTIME_DIR/jarvis.log"
PID_FILE="$RUNTIME_DIR/jarvis.pid"
FX_PID_FILE="$RUNTIME_DIR/jarvis-fx.pid"
PYTHON_BIN="${PYTHON_BIN:-$JARVIS_DIR/.venv/bin/python}"

# Cores
CYAN='\033[0;36m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'

show_menu() {
    clear
    echo -e "${CYAN}=== JARVIS SYSTEM CONTROL ===${RESET}"
    echo "1) start       - Iniciar serviços"
    echo "2) stop        - Parar serviços"
    echo "3) restart     - Reiniciar serviços"
    echo "4) mic-toggle  - Ativar/Desativar microfone"
    echo "5) config      - Editar configurações"
    echo "6) installer   - Executar instalador detectando hardware"
    echo "7) install     - Instalar componente específico"
    echo "8) logs        - Ver logs em tempo real"
    echo "9) status      - Ver status dos processos"
    echo "10) voice-on   - Ativar módulo de voz (placeholder)"
    echo "11) voice-off  - Desativar módulo de voz (placeholder)"
    echo "12) fx-on      - Ativar efeito visual desktop"
    echo "13) fx-off     - Desativar efeito visual desktop"
    echo "q) sair"
    echo -n "Escolha uma opção: "
}

start() {
    echo -e "${GREEN}Iniciando Jarvis...${RESET}"
    mkdir -p "$RUNTIME_DIR"
    cd "$JARVIS_DIR" || return 1
    if [ -f "$PID_FILE" ] && ps -p "$(cat "$PID_FILE")" > /dev/null 2>&1; then
        echo "Jarvis já está rodando (PID $(cat "$PID_FILE"))."
        return 0
    fi
    if [ ! -x "$PYTHON_BIN" ]; then
        PYTHON_BIN="$(command -v python3)"
    fi
    nohup "$PYTHON_BIN" main.py > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "Jarvis iniciado com PID $(cat "$PID_FILE"). Logs em $LOG_FILE"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo -e "${RED}Parando Jarvis (PID $PID)...${RESET}"
        kill "$PID" 2>/dev/null || true
        rm -f "$PID_FILE"
    else
        echo "Jarvis não parece estar rodando."
    fi
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "Jarvis rodando (PID $PID)"
        else
            echo "PID file existe, mas processo não encontrado."
        fi
    else
        echo "Jarvis não está rodando."
    fi
}

mic_toggle() {
    # tenta alternar captura via amixer (PulseAudio/ALSA)
    if command -v amixer >/dev/null 2>&1; then
        amixer set Capture toggle && echo "Microfone alternado."
    else
        echo "amixer não encontrado; verifique PulseAudio/ALSA."
    fi
}

show_logs() {
    mkdir -p "$RUNTIME_DIR"
    touch "$LOG_FILE"
    tail -f "$LOG_FILE"
}

install_component() {
    comp="$1"
    echo -e "${YELLOW}Instalando componente: $comp${RESET}"
    "$SCRIPT_DIR/scripts/installer.sh" --install "$comp"
}

voice_on() {
    echo "Ativando módulo de voz (placeholder)..."
    # Placeholder: iniciar processo TTS/STT
}

voice_off() {
    echo "Desativando módulo de voz (placeholder)..."
}

fx_on() {
    mkdir -p "$RUNTIME_DIR"
    if [ -f "$FX_PID_FILE" ] && ps -p "$(cat "$FX_PID_FILE")" > /dev/null 2>&1; then
        echo "Jarvis FX já está ativo (PID $(cat "$FX_PID_FILE"))."
        return 0
    fi
    if [ ! -x "$PYTHON_BIN" ]; then
        PYTHON_BIN="$(command -v python3)"
    fi
    nohup "$PYTHON_BIN" "$SCRIPT_DIR/scripts/jarvis_fx.py" > "$RUNTIME_DIR/jarvis-fx.log" 2>&1 &
    echo $! > "$FX_PID_FILE"
    echo "Jarvis FX iniciado com PID $(cat "$FX_PID_FILE")."
}

fx_off() {
    if [ -f "$FX_PID_FILE" ]; then
        PID=$(cat "$FX_PID_FILE")
        echo -e "${RED}Parando Jarvis FX (PID $PID)...${RESET}"
        kill "$PID" 2>/dev/null || true
        rm -f "$FX_PID_FILE"
    else
        echo "Jarvis FX não parece estar rodando."
    fi
}

print_help() {
    echo "Usage: $0 <command> [args]"
    echo "Commands: start stop restart mic-toggle config installer install logs status voice-on voice-off fx-on fx-off help"
}

case "$1" in
    start) start ;; 
    stop) stop ;; 
    restart) stop; start ;; 
    mic-toggle) mic_toggle ;; 
    config) mkdir -p "$RUNTIME_DIR"; touch "$RUNTIME_DIR/config.json"; ${EDITOR:-nano} "$RUNTIME_DIR/config.json" ;; 
    installer) "$SCRIPT_DIR/scripts/installer.sh" "${@:2}" ;; 
    install) shift; install_component "$*" ;; 
    logs) show_logs ;; 
    status) status ;; 
    voice-on) voice_on ;; 
    voice-off) voice_off ;; 
    fx-on) fx_on ;;
    fx-off) fx_off ;;
    "" ) show_menu; read opt; case $opt in
            1) $0 start ;;
            2) $0 stop ;;
            3) $0 restart ;;
            4) $0 mic-toggle ;;
            5) $0 config ;;
            6) $0 installer ;;
            7) echo "Use: $0 install <component>" ;;
            8) $0 logs ;;
            9) $0 status ;;
            10) $0 voice-on ;;
            11) $0 voice-off ;;
            12) $0 fx-on ;;
            13) $0 fx-off ;;
            q) exit ;;
        esac ;; 
    help|-h|--help) print_help ;; 
    *) echo "Comando desconhecido: $1"; print_help ;;
esac
