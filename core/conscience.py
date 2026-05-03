"""Módulo placeholder para a "conscience" do assistente.

Responsabilidades (futuras):
- Política de segurança e verificação de ações perigosas
- Regras de privacidade e consentimento
- Monitoramento de comportamento e limites
"""

class Conscience:
    def __init__(self):
        self.enabled = True

    def check_action(self, action: str) -> bool:
        """Avalia se uma ação é permitida. Retorna True se permitida."""
        # placeholder: regras simples
        forbidden = ["rm -rf /", "dd if="]
        for f in forbidden:
            if f in action:
                return False
        return True
