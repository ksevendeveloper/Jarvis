"""Placeholder para `Assistant` que orquestra módulos de IA e sistema."""

class Assistant:
    def __init__(self, name: str = "Jarvis"):
        self.name = name

    async def think(self, prompt: str) -> str:
        # placeholder: integrar com Ollama / Llama3 local
        return f"(simulado) respondiendo a: {prompt}"
