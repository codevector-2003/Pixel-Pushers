from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId

from schemas.growth import GrowthRecord, GrowthRecordCreate
from config import growth_collection, baby_collection
from security import get_current_active_user

router = APIRouter(tags=["growth"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/{baby_id}/growth/", response_model=GrowthRecord)
async def create_growth_record(
    baby_id: str, 
    growth: GrowthRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    growth_dict = growth.dict()
    growth_dict["baby_id"] = baby_id
    
    result = growth_collection.insert_one(growth_dict)
    created_growth = growth_collection.find_one({"_id": result.inserted_id})
    return created_growth

@router.get("/babies/{baby_id}/growth/", response_model=List[GrowthRecord])
async def read_growth_records(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    growth_records = list(growth_collection.find(
        {"baby_id": baby_id},
        skip=skip,
        limit=limit
    ))
    return growth_records

@router.get("/babies/{baby_id}/growth/{growth_id}", response_model=GrowthRecord)
async def read_growth_record(
    baby_id: str, 
    growth_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    growth = growth_collection.find_one({
        "_id": ObjectId(growth_id),
        "baby_id": baby_id
    })
    if growth is None:
        raise HTTPException(status_code=404, detail="Growth record not found")
    return growth

@router.put("/babies/{baby_id}/growth/{growth_id}", response_model=GrowthRecord)
async def update_growth_record(
    baby_id: str, 
    growth_id: str, 
    growth_update: GrowthRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    update_data = growth_update.dict(exclude_unset=True)
    growth_collection.update_one(
        {"_id": ObjectId(growth_id), "baby_id": baby_id},
        {"$set": update_data}
    )
    updated_growth = growth_collection.find_one({"_id": ObjectId(growth_id)})
    return updated_growth

@router.delete("/babies/{baby_id}/growth/{growth_id}")
async def delete_growth_record(
    baby_id: str, 
    growth_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = growth_collection.delete_one({
        "_id": ObjectId(growth_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Growth record not found")
    return {"message": "Growth record deleted successfully"}

