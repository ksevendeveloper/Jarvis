from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db
from api.auth import get_current_user, verify_token
from api.models import Conversation, User
from core.conscience import Conscience
from core.ai import JarvisAI
from typing import Optional
import main as main_app

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(req: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # security check
    conscience = Conscience()
    if not conscience.check_action(req.message):
        raise HTTPException(status_code=403, detail="Action forbidden by conscience")

    # save user message
    conv = Conversation(user_id=current_user.id, role="user", content=req.message)
    db.add(conv)
    db.commit()

    # load history
    history = db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.timestamp.asc()).all()

    ai = JarvisAI()
    result = await ai.respond(history)

    # result expected: dict with 'reply', optional 'execute' and 'command'
    reply = result.get("reply") if isinstance(result, dict) else str(result)
    execute = result.get("execute") if isinstance(result, dict) else False
    command = result.get("command") if isinstance(result, dict) else None

    # save assistant reply
    conv2 = Conversation(user_id=current_user.id, role="assistant", content=reply)
    db.add(conv2)
    db.commit()

    # if need to execute a command
    if execute and command:
        room = f"user:{current_user.username}"
        await main_app.sio.emit("executing", {"command": command}, to=room)
        # run command in background
        await main_app.run_and_emit(command, room=room)

    # emit final status
    room = f"user:{current_user.username}"
    await main_app.sio.emit("status", {"event": "reply", "reply": reply}, to=room)

    return {"reply": reply, "execute": bool(execute), "command": command}
