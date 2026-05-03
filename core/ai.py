"""Integração com Ollama local via HTTP.

Implementa `JarvisAI` que consulta o endpoint local do Ollama (porta 11434).
O método `respond` recebe o histórico (lista de Conversation ORM objects)
e retorna um dicionário com keys: `reply`, optional `execute` (bool) e `command` (str).
"""
import httpx
import os
import json
from typing import List, Dict, Any


SYSTEM_PROMPT = (
    "You are Jarvis, a loyal, technical, and efficient assistant for a Linux system administrator. "
    "When asked, you may suggest shell commands to accomplish tasks. "
    "If you decide a command must be executed, respond in JSON with keys: reply, execute (true/false), command (string). "
    "Example JSON: {\"reply\": \"I will list files\", \"execute\": true, \"command\": \"ls -la /tmp\"}. "
    "If no command is needed, return {\"reply\": \"...\", \"execute\": false}."
)


class JarvisAI:
    def __init__(self, host: str = None, model: str = None):
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.model = model or os.environ.get("OLLAMA_MODEL", "llama3")

    async def call_ollama(self, prompt: str) -> str:
        url = f"{self.host}/api/generate"
        payload = {"model": self.model, "prompt": prompt}
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                # Ollama response shape may vary; attempt to extract text
                if isinstance(data, dict) and "text" in data:
                    return data["text"]
                if isinstance(data, dict) and "output" in data:
                    return data["output"]
                return json.dumps(data)
            except Exception as e:
                return f"{{\"reply\": \"Ollama error: {str(e)}\", \"execute\": false}}"

    def build_prompt(self, history: List[Any]) -> str:
        parts = ["System: " + SYSTEM_PROMPT]
        for h in history:
            role = h.role
            content = h.content
            parts.append(f"{role.capitalize()}: {content}")
        parts.append("Assistant:")
        return "\n".join(parts)

    async def respond(self, history: List[Any]) -> Dict[str, Any]:
        prompt = self.build_prompt(history)
        raw = await self.call_ollama(prompt)
        # try parse JSON
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict) and "reply" in parsed:
                return parsed
        except Exception:
            # fallback: try to extract JSON substring
            try:
                start = raw.find('{')
                if start != -1:
                    parsed = json.loads(raw[start:])
                    if isinstance(parsed, dict) and "reply" in parsed:
                        return parsed
            except Exception:
                pass

        # default fallback: return as plain reply
        return {"reply": str(raw), "execute": False}


def is_ollama_available() -> bool:
    try:
        import socket
        host = os.environ.get("OLLAMA_HOST", "localhost")
        # quick TCP check
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((host, 11434))
        s.close()
        return True
    except Exception:
        return False

