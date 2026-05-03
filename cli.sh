#!/bin/bash

# CLI avançado para Jarvis
# Uso: ./cli.sh [command] [options]

JARVIS_DIR="$HOME/jarvis-system"
LOG_FILE="$JARVIS_DIR/jarvis.log"
PID_FILE="$JARVIS_DIR/jarvis.pid"

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
    echo "q) sair"
    echo -n "Escolha uma opção: "
}

start() {
    echo -e "${GREEN}Iniciando Jarvis...${RESET}"
    mkdir -p "$JARVIS_DIR"
    cd "$JARVIS_DIR" || return 1
    nohup python3 main.py > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "PID $(cat $PID_FILE)" > "$LOG_FILE"
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
    tail -f "$LOG_FILE"
}

install_component() {
    comp="$1"
    echo -e "${YELLOW}Instalando componente: $comp${RESET}"
    scripts/installer.sh --install "$comp"
}

voice_on() {
    echo "Ativando módulo de voz (placeholder)..."
    # Placeholder: iniciar processo TTS/STT
}

voice_off() {
    echo "Desativando módulo de voz (placeholder)..."
}

print_help() {
    echo "Usage: $0 <command> [args]"
    echo "Commands: start stop restart mic-toggle config installer install logs status voice-on voice-off help"
}

case "$1" in
    start) start ;; 
    stop) stop ;; 
    restart) stop; start ;; 
    mic-toggle|mic-toggle) mic_toggle ;; 
    config) ${EDITOR:-nano} "$JARVIS_DIR/config.json" ;; 
    installer) scripts/installer.sh ${@:2} ;; 
    install) shift; install_component "$*" ;; 
    logs) show_logs ;; 
    status) status ;; 
    voice-on) voice_on ;; 
    voice-off) voice_off ;; 
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
            q) exit ;;
        esac ;; 
    help|-h|--help) print_help ;; 
    *) echo "Comando desconhecido: $1"; print_help ;;
esac
