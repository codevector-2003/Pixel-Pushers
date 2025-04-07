from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime

from schemas.illness import IllnessRecord, IllnessRecordCreate
from config import illness_collection, baby_collection
from security import get_current_active_user

router = APIRouter(tags=["illness"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/{baby_id}/illness/", response_model=IllnessRecord)
async def create_illness_record(
    baby_id: str, 
    illness: IllnessRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    illness_data = illness.model_dump()
    illness_data["baby_id"] = baby_id
    illness_data["date"] = datetime.combine(illness_data["date"], datetime.min.time())
    
    result = illness_collection.insert_one(illness_data)
    created_illness = illness_collection.find_one({"_id": result.inserted_id})
    created_illness["_id"] = str(created_illness["_id"])
    return IllnessRecord(**created_illness)

@router.get("/babies/{baby_id}/illness/", response_model=List[IllnessRecord])
async def read_illness_records(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    illnesses = list(illness_collection.find(
        {"baby_id": baby_id},
        skip=skip,
        limit=limit
    ))
    return illnesses

@router.get("/babies/{baby_id}/illness/{illness_id}", response_model=IllnessRecord)
async def read_illness_record(
    baby_id: str, 
    illness_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    illness = illness_collection.find_one({
        "_id": ObjectId(illness_id),
        "baby_id": baby_id
    })
    if illness is None:
        raise HTTPException(status_code=404, detail="Illness record not found")
    return illness

@router.put("/babies/{baby_id}/illness/{illness_id}", response_model=IllnessRecord)
async def update_illness_record(
    baby_id: str, 
    illness_id: str, 
    illness_update: IllnessRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    update_data = illness_update.model_dump()
    update_data["date"] = datetime.combine(update_data["date"], datetime.min.time())
    result = illness_collection.update_one(
        {"_id": ObjectId(illness_id), "baby_id": baby_id},
        {"$set": update_data}
    )
    
    updated_illness = illness_collection.find_one({"_id": ObjectId(illness_id)})
    updated_illness["_id"] = str(updated_illness["_id"])
    return IllnessRecord(**updated_illness)

@router.delete("/babies/{baby_id}/illness/{illness_id}")
async def delete_illness_record(
    baby_id: str, 
    illness_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = illness_collection.delete_one({
        "_id": ObjectId(illness_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Illness record not found")
    return {"message": "Illness record deleted successfully"}