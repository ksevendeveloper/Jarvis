#!/usr/bin/env python3
"""Cliente de teste que conecta via Socket.IO, envia um POST para /api/execute e imprime eventos."""
import asyncio
import json
import sys

import httpx
import socketio


SERVER = "http://localhost:8000"


async def main(cmd: str = "echo hello && sleep 1 && echo done"):
    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        print("[client] connected to server")

    @sio.event
    async def disconnect():
        print("[client] disconnected")

    @sio.on("status")
    async def on_status(data):
        print("[event:status]", data)

    @sio.on("executing")
    async def on_executing(data):
        print("[event:executing]", data)

    @sio.on("success")
    async def on_success(data):
        print("[event:success]", data)
        await sio.disconnect()

    @sio.on("error")
    async def on_error(data):
        print("[event:error]", data)
        await sio.disconnect()

    await sio.connect(SERVER)

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{SERVER}/api/execute", json={"command": cmd}, timeout=10.0)
        print("POST /api/execute ->", resp.status_code, resp.text)

    # aguardar eventos até desconexão
    await sio.wait()


if __name__ == "__main__":
    cmd = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "echo hello && sleep 1 && echo done"
    asyncio.run(main(cmd))
