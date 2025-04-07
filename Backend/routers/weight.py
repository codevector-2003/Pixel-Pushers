from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
import math
from scipy.stats import norm
from schemas.weight import WeightRecord, WeightRecordCreate
from utils.growth_calculations import get_growth_assessment
from config import weight_collection, baby_collection
from security import get_current_active_user
from datetime import datetime , date

router = APIRouter(tags=["weight"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/{baby_id}/weight/", response_model=WeightRecord)
async def create_weight_record(
    baby_id: str, 
    weight: WeightRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    weight_data = weight.model_dump()
    if (isinstance(weight_data.get("date"), date) and 
        not isinstance(weight_data.get("date"), datetime)):
        weight_data["date"] = datetime.combine(weight_data["date"], datetime.min.time())
        weight_data["baby_id"] = baby_id
    
    result = weight_collection.insert_one(weight_data)
    created_weight = weight_collection.find_one({"_id": result.inserted_id})
    created_weight["_id"] = str(created_weight["_id"])
 
    return created_weight

@router.get("/babies/{baby_id}/weight/", response_model=List[WeightRecord])
async def read_weight_records(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    weight_records = list(weight_collection.find(
        {"baby_id": baby_id},
        skip=skip,
        limit=limit
    ))
    for record in weight_records:
        record["_id"] = str(record["_id"])
    return weight_records

@router.delete("/babies/{baby_id}/weight/{weight_id}")
async def delete_weight_record(
    baby_id: str, 
    weight_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = weight_collection.delete_one({
        "_id": ObjectId(weight_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Weight record not found")
    return {"message": "Weight record deleted successfully"}