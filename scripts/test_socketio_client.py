#!/usr/bin/env python3
"""Cliente de teste com autenticação JWT para /api/execute e Socket.IO."""
import argparse
import asyncio

import httpx
import socketio


SERVER = "http://localhost:8000"


async def fetch_token(username: str, password: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SERVER}/api/auth/login",
            json={"username": username, "password": password},
            timeout=10.0,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]


async def main(cmd: str, username: str, password: str):
    token = await fetch_token(username, password)
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

    await sio.connect(SERVER, auth={"token": token})

    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SERVER}/api/execute",
            json={"command": cmd},
            headers=headers,
            timeout=10.0,
        )
        print("POST /api/execute ->", resp.status_code, resp.text)

    await sio.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="*", default=["echo hello && sleep 1 && echo done"])
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="admin")
    args = parser.parse_args()

    command = " ".join(args.command).strip()
    asyncio.run(main(command, args.username, args.password))
