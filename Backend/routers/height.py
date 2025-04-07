from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
import math
from scipy.stats import norm
from schemas.height import HeightRecord , HeightRecordCreate
from utils.growth_calculations import get_growth_assessment
from config import height_collection, baby_collection
from security import get_current_active_user
from datetime import datetime , date

router = APIRouter(tags=["height"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/{baby_id}/height/", response_model=HeightRecord)
async def create_height_record(
    baby_id: str, 
    height: HeightRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    height_data = height.model_dump()
    if (isinstance(height_data.get("date"), date) and 
        not isinstance(height_data.get("date"), datetime)):
        height_data["date"] = datetime.combine(height_data["date"], datetime.min.time())
        height_data["baby_id"] = baby_id

    result = height_collection.insert_one(height_data)
    created_height = height_collection.find_one({"_id": result.inserted_id})
    created_height["_id"] = str(created_height["_id"])
 
    return created_height

@router.get("/babies/{baby_id}/height/", response_model=List[HeightRecord])
async def read_height_records(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    height_records = list(height_collection.find(
        {"baby_id": baby_id}
    ).skip(skip).limit(limit))

    for record in height_records:
        record["_id"] = str(record["_id"])
    return height_records


@router.delete("/babies/{baby_id}/height/{height_id}")
async def delete_height_record(
    baby_id: str, 
    height_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = height_collection.delete_one({
        "_id": ObjectId(height_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Height record not found")
    return {"message": "Height record deleted successfully"}