import asyncio
import os
from typing import Dict

import socketio
from fastapi import FastAPI, BackgroundTasks
from api.routes import router as api_router
from api import auth as auth_module
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Socket.IO server (ASGI)
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# FastAPI app
app = FastAPI(title="Jarvis - Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include example API routes
app.include_router(api_router, prefix="/api")
app.include_router(auth_module.router, prefix="/api")


class ExecuteRequest(BaseModel):
    command: str


@sio.event
async def connect(sid, environ):
    await sio.emit("status", {"event": "connected", "sid": sid}, to=sid)


@sio.event
async def disconnect(sid):
    print("Client disconnected", sid)


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "jarvis-backend"}


@app.post("/api/execute")
async def execute(req: ExecuteRequest, background_tasks: BackgroundTasks):
    """Agenda a execução de um comando no sistema e emite eventos Socket.IO.

    Retorna imediatamente um ack e executa o comando em background.
    """
    cmd = req.command
    background_tasks.add_task(run_and_emit, cmd)
    return {"status": "scheduled", "command": cmd}


async def run_and_emit(cmd: str):
    await sio.emit("executing", {"command": cmd})
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            executable="/bin/bash",
        )
        stdout, stderr = await proc.communicate()
        returncode = proc.returncode
        out = stdout.decode().strip()
        err = stderr.decode().strip()
        if returncode == 0:
            await sio.emit("success", {"command": cmd, "output": out})
        else:
            await sio.emit(
                "error",
                {"command": cmd, "returncode": returncode, "stderr": err},
            )
    except Exception as e:
        await sio.emit("error", {"command": cmd, "exception": str(e)})


# Mount Socket.IO ASGI app together with FastAPI app
asgi_app = socketio.ASGIApp(sio, other_asgi_app=app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:asgi_app", host="0.0.0.0", port=8000, log_level="info")
