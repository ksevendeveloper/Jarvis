#!/usr/bin/env python3
"""Desktop visual effect daemon for Jarvis events."""

import argparse
import asyncio
import math
import os
import threading
import tkinter as tk

import httpx
import socketio

STATE_COLORS = {
    "offline": "#5f6b7a",
    "idle": "#4bb5ff",
    "online": "#36d7b7",
    "executing": "#ffcc4d",
    "success": "#35dd7d",
    "error": "#ff5d73",
}

STATE_SPEED = {
    "offline": 0.02,
    "idle": 0.09,
    "online": 0.08,
    "executing": 0.16,
    "success": 0.12,
    "error": 0.2,
}


class JarvisOrb:
    def __init__(self):
        self.state = "offline"
        self.running = True
        self.phase = 0.0

        self.root = tk.Tk()
        self.root.title("Jarvis FX")
        self.root.geometry("170x170+40+40")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.configure(bg="#07121f")

        self.canvas = tk.Canvas(self.root, width=170, height=170, bg="#07121f", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.ring_outer = self.canvas.create_oval(20, 20, 150, 150, outline="#4bb5ff", width=3)
        self.ring_inner = self.canvas.create_oval(40, 40, 130, 130, outline="#4bb5ff", width=2)
        self.core = self.canvas.create_oval(55, 55, 115, 115, fill="#4bb5ff", outline="")
        self.label = self.canvas.create_text(85, 150, text="offline", fill="#c5def0", font=("Helvetica", 10, "bold"))

        self.root.protocol("WM_DELETE_WINDOW", self.stop)

    def set_state(self, state: str):
        if state in STATE_COLORS:
            self.state = state

    def animate(self):
        if not self.running:
            return

        color = STATE_COLORS[self.state]
        speed = STATE_SPEED[self.state]
        self.phase += speed

        pulse = 4 + (3 * (1 + math.sin(self.phase)))
        outer = 20 - pulse
        inner = 40 - (pulse / 2)

        self.canvas.coords(self.ring_outer, outer, outer, 170 - outer, 170 - outer)
        self.canvas.coords(self.ring_inner, inner, inner, 170 - inner, 170 - inner)
        self.canvas.itemconfig(self.ring_outer, outline=color)
        self.canvas.itemconfig(self.ring_inner, outline=color)
        self.canvas.itemconfig(self.core, fill=color)
        self.canvas.itemconfig(self.label, text=self.state, fill="#d8ecfb")

        self.root.after(33, self.animate)

    def stop(self):
        self.running = False
        self.root.quit()


async def fetch_token(server: str, username: str, password: str) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(f"{server}/api/auth/login", json={"username": username, "password": password})
        resp.raise_for_status()
        return resp.json()["access_token"]


async def socket_worker(server: str, token: str, orb: JarvisOrb):
    sio = socketio.AsyncClient(reconnection=True, reconnection_attempts=0)

    @sio.event
    async def connect():
        orb.set_state("online")

    @sio.event
    async def disconnect():
        orb.set_state("offline")

    @sio.on("status")
    async def on_status(_):
        orb.set_state("online")

    @sio.on("executing")
    async def on_executing(_):
        orb.set_state("executing")

    @sio.on("success")
    async def on_success(_):
        orb.set_state("success")

    @sio.on("error")
    async def on_error(_):
        orb.set_state("error")

    try:
        await sio.connect(server, auth={"token": token})
        while orb.running:
            await asyncio.sleep(0.2)
    finally:
        if sio.connected:
            await sio.disconnect()


def run_async_loop(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default=os.environ.get("JARVIS_SERVER_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--token", default=os.environ.get("JARVIS_FX_TOKEN"))
    parser.add_argument("--username", default=os.environ.get("JARVIS_FX_USER", "admin"))
    parser.add_argument("--password", default=os.environ.get("JARVIS_FX_PASSWORD", "admin"))
    args = parser.parse_args()

    orb = JarvisOrb()

    token = args.token
    if not token:
        token = asyncio.run(fetch_token(args.server, args.username, args.password))

    thread = threading.Thread(target=run_async_loop, args=(socket_worker(args.server, token, orb),), daemon=True)
    thread.start()

    orb.animate()
    orb.root.mainloop()


if __name__ == "__main__":
    main()
