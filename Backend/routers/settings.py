from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime

from schemas.user import User
from config import doctor_chat_collection
from security import get_current_active_user

router = APIRouter(tags=["doctor"])

@router.post("/doctor/chat/", response_model=dict)
async def create_chat_message(
    message: dict, 
    current_user: dict = Depends(get_current_active_user)
):
    message_dict = message
    message_dict["user_id"] = str(current_user["_id"])
    message_dict["timestamp"] = datetime.utcnow()
    
    result = doctor_chat_collection.insert_one(message_dict)
    created_message = doctor_chat_collection.find_one({"_id": result.inserted_id})
    return created_message

@router.get("/doctor/chat/", response_model=List[dict])
async def read_chat_messages(
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    messages = list(doctor_chat_collection.find(
        {"user_id": str(current_user["_id"])},
        skip=skip,
        limit=limit
    ).sort("timestamp", -1))  # Sort by timestamp descending
    return messages