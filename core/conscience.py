"""Policy de segurança para filtrar comandos shell arriscados."""

from typing import Tuple


class Conscience:
    def __init__(self):
        self.enabled = True
        self.forbidden_patterns = [
            "rm -rf /",
            "dd if=",
            "mkfs",
            ":(){ :|:& };:",
            "shutdown",
            "reboot",
            "poweroff",
            "userdel",
            "chmod -R 777 /",
            "> /dev/sd",
        ]

    def evaluate_action(self, action: str) -> Tuple[bool, str]:
        """Retorna (permitido, motivo)."""
        cmd = (action or "").strip().lower()
        if not cmd:
            return False, "Command is empty."

        for pattern in self.forbidden_patterns:
            if pattern in cmd:
                return False, f"Command blocked by safety policy: '{pattern}'."

        return True, "Command allowed."

    def check_action(self, action: str) -> bool:
        allowed, _ = self.evaluate_action(action)
        return allowed
