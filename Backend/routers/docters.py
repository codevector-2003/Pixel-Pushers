# app/routers/doctor.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from bson import ObjectId

from config import doctor_chat_collection
from security import get_current_active_user
from utils.genai_chat import setup_genai, get_doctor_reply

router = APIRouter(tags=["doctor"])

@router.post("/doctor/chat/", response_model=dict)
async def create_chat_message(
    message: dict, 
    current_user: dict = Depends(get_current_active_user)
):
    user_id = str(current_user["_id"])
    user_msg = message.get("text", "")

    if not user_msg:
        raise HTTPException(status_code=400, detail="Message text is required.")

    # Save user message
    user_entry = {
        "user_id": user_id,
        "sender": "user",
        "text": user_msg,
        "timestamp": datetime.utcnow()
    }
    doctor_chat_collection.insert_one(user_entry)

    # Generate doctor reply
    model = setup_genai()
    reply_text = get_doctor_reply(model, user_msg)

    # Save bot reply
    bot_entry = {
        "user_id": user_id,
        "sender": "doctor",
        "text": reply_text,
        "timestamp": datetime.utcnow()
    }
    doctor_chat_collection.insert_one(bot_entry)

    return {"user_message": user_msg, "doctor_reply": reply_text}

@router.get("/doctor/chat/", response_model=List[dict])
async def read_chat_messages(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_active_user)
):
    user_id = str(current_user["_id"])
    
    messages = list(doctor_chat_collection.find(
        {"user_id": user_id},
    ).sort("timestamp", 1).skip(skip).limit(limit))  # Sort ASCENDING

    return messages
