#!/bin/bash

# Configurações
JARVIS_DIR="$HOME/jarvis-system"
VENV_PATH="$JARVIS_DIR/venv/bin/activate"
LOG_FILE="$JARVIS_DIR/jarvis.log"

# Cores para o terminal
CYAN='\033[0;36m'
RED='\033[0;31m'
GREEN='\033[0;32m'
RESET='\033[0m'

show_menu() {
    clear
    echo -e "${CYAN}=== JARVIS SYSTEM CONTROL ===${RESET}"
    echo "1) Ligar (Start)"
    echo "2) Desligar (Stop)"
    echo "3) Reiniciar (Restart)"
    echo "4) Ativar/Desativar Microfone"
    echo "5) Editar Configurações"
    echo "6) Ativar Inicialização Automática (Boot)"
    echo "7) Desativar Inicialização Automática"
    echo "8) Ver Logs em tempo real"
    echo "q) Sair"
    echo -n "Escolha uma opção: "
}

case $1 in
    start)
        echo -e "${GREEN}Iniciando Jarvis...${RESET}"
        # Comando para iniciar backend e frontend (exemplo com pm2 ou nohup)
        cd $JARVIS_DIR && nohup python3 main.py > $LOG_FILE 2>&1 &
        echo $! > $JARVIS_DIR/jarvis.pid
        ;;
    stop)
        echo -e "${RED}Desligando Jarvis...${RESET}"
        kill $(cat $JARVIS_DIR/jarvis.pid) && rm $JARVIS_DIR/jarvis.pid
        ;;
    mic-toggle)
        # Comando específico para Ubuntu/PulseAudio
        amixer set Capture toggle
        echo "Status do microfone alterado."
        ;;
    *)
        show_menu
        read opt
        case $opt in
            1) $0 start ;;
            2) $0 stop ;;
            4) $0 mic-toggle ;;
            5) nano $JARVIS_DIR/config.json ;;
            8) tail -f $LOG_FILE ;;
            q) exit ;;
        esac
        ;;
esac