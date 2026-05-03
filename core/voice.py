"""Módulo placeholder para funcionalidades de voz (STT/TTS).

Implementação futura:
- Integração com Vosk/Coqui/STT local
- Pipeline: capture audio -> transcribe -> emit socket event
- TTS: gerar áudio localmente e reproduzir
"""
from typing import Optional

class VoiceEngine:
    def __init__(self, model: Optional[str] = None):
        self.model = model
        self.running = False

    def start(self):
        self.running = True
        # placeholder: iniciar captura de microfone e STT

    def stop(self):
        self.running = False

    def synthesize(self, text: str) -> bytes:
        # placeholder: retornar bytes de áudio sintetizado
        return text.encode("utf-8")
