"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
import math
from scipy.stats import norm
from schemas.growth import GrowthRecord, GrowthRecordCreate
from utils.growth_calculations import get_growth_assessment
from config import growth_collection, baby_collection
from security import get_current_active_user
from datetime import datetime

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
    
    growth_data = growth.model_dump()
    growth_data["baby_id"] = baby_id
    
    result = growth_collection.insert_one(growth_data)
    created_growth = growth_collection.find_one({"_id": result.inserted_id})
    created_growth["_id"] = str(created_growth["_id"])
    created_growth["baby_id"] = baby_id 
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

@router.get("/babies/{baby_id}/growth/graph-data", response_model=List[dict])
async def get_growth_graph_data(
    baby_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """"""""
    Returns growth data formatted specifically for frontend graphing
    Format: [
        {date: "2023-01-01", weight: 3.5, height: 52.0},
        {date: "2023-02-01", weight: 4.2, height: 55.0},
        ...
    ]
    """
"""
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    growth_records = list(growth_collection.find(
        {"baby_id": baby_id},
        {"_id": 0, "date": 1, "weight": 1, "height": 1 , "notes" : 0 } 
    ).sort("date", 1))  # Sort by date ascending
    
    # Convert dates to strings and handle None values
    for record in growth_records:
        record["date"] = record["date"].isoformat()
        
    return growth_records


@router.get("/babies/{baby_id}/growth/percentiles", response_model=List[dict])
async def get_growth_percentiles(
    baby_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))

    baby = baby_collection.find_one({"_id": ObjectId(baby_id)})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    
    growth_records = list(growth_collection.find(
        {"baby_id": baby_id},
        {"_id": 0, "date": 1, "weight": 1, "height": 1}
    ).sort("date", 1))

    last_nonzero_weight = None
    last_nonzero_height = None

    # Find the last non-zero weight and height
    for record in reversed(growth_records):
        if record["weight"] > 0 and last_nonzero_weight is None:
            last_nonzero_weight = record["weight"]
        
        if record["height"] > 0 and last_nonzero_height is None:
            last_nonzero_height = record["height"]

        if last_nonzero_weight is not None and last_nonzero_height is not None:
            break
    
    # If no valid weight or height was found, raise an error
    if last_nonzero_weight is None or last_nonzero_height is None:
        raise HTTPException(status_code=404, detail="Valid growth data not found")
    
    result = {
        "last_nonzero_weight": last_nonzero_weight,
        "last_nonzero_height": last_nonzero_height
    }

    return [result]

@router.get("/babies/{baby_id}/growth/assessment", response_model=dict)
async def get_latest_growth_assessment(
    baby_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
 
    baby = baby_collection.find_one({"_id": ObjectId(baby_id)})
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")

    latest_record = growth_collection.find_one(
        {"baby_id": baby_id},
        sort=[("date", -1)]  # Get most recent
    )
    if not latest_record:
        raise HTTPException(status_code=404, detail="No growth records found")
    
    # Calculate growth assessment
    assessment = get_growth_assessment(
        gender=baby["gender"],
        birth_date=baby["birth_date"],
        measurement_date=datetime.now().date(),
        weight_kg=latest_record["weight"],
        height_cm=latest_record["height"]
    )
    return assessment

"""