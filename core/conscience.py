"""Policy de segurança para filtrar comandos shell arriscados."""

from typing import Tuple
import os
import datetime


class Conscience:
    """Policy de segurança para filtrar comandos shell arriscados.

    Além de avaliar padrões proibidos, registra tentativas em `logs/audit.log`.
    """

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
        os.makedirs('logs', exist_ok=True)
        self.audit_path = os.path.join('logs', 'audit.log')

    def _audit(self, user: str, action: str, allowed: bool, reason: str):
        ts = datetime.datetime.utcnow().isoformat()
        line = f"{ts} | user={user or 'unknown'} | allowed={allowed} | reason={reason} | action={action}\n"
        try:
            with open(self.audit_path, 'a', encoding='utf-8') as f:
                f.write(line)
        except Exception:
            pass

    def evaluate_action(self, action: str, user: str = None) -> Tuple[bool, str]:
        """Retorna (permitido, motivo)."""
        cmd = (action or "").strip().lower()
        if not cmd:
            reason = "Command is empty."
            self._audit(user, action, False, reason)
            return False, reason

        for pattern in self.forbidden_patterns:
            if pattern in cmd:
                reason = f"Command blocked by safety policy: '{pattern}'."
                self._audit(user, action, False, reason)
                return False, reason

        reason = "Command allowed."
        self._audit(user, action, True, reason)
        return True, reason

    def check_action(self, action: str) -> bool:
        allowed, _ = self.evaluate_action(action)
        return allowed
