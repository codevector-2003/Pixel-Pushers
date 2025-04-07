from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from schemas.diet import DietRecord, DietRecordCreate 
from config import diet_collection, baby_collection , allergy_collection , food_collection
from security import get_current_active_user
from datetime import datetime  

router = APIRouter(tags=["diet"])
def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/{baby_id}/diet/")
async def create_diet_record(
    baby_id: str, 
    diet_record: DietRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    diet_dict = diet_record.dict()
    diet_dict["baby_id"] = baby_id

    diet_dict["date"] = datetime.combine(diet_dict["date"], datetime.min.time())
    diet_dict["baby_id"] = baby_id
    
    result = diet_collection.insert_one(diet_dict)
    created_diet = diet_collection.find_one({"_id": result.inserted_id})
    created_diet["_id"] = str(created_diet["_id"])
    return  created_diet

@router.get("/babies/{baby_id}/diet/", response_model=List[DietRecord])
async def read_diet_records(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    diet_records = list(diet_collection.find(
        {"baby_id": baby_id},
        skip=skip,
        limit=limit
    ))
    return diet_records

@router.get("/babies/{baby_id}/diet/{diet_id}", response_model=DietRecord)
async def read_diet_record(
    baby_id: str, 
    diet_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    diet_record = diet_collection.find_one({
        "_id": ObjectId(diet_id),
        "baby_id": baby_id
    })
    if diet_record is None:
        raise HTTPException(status_code=404, detail="Diet record not found")
    return diet_record

@router.put("/babies/{baby_id}/diet/{diet_id}", response_model=DietRecord)
async def update_diet_record(
    baby_id: str, 
    diet_id: str, 
    diet_update: DietRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    update_data = diet_update.dict(exclude_unset=True)
    if "date" in update_data:
        update_data["date"] = datetime.combine(update_data["date"], datetime.min.time())

    diet_collection.update_one(
        {"_id": ObjectId(diet_id), "baby_id": baby_id},
        {"$set": update_data}
    )
    updated_diet = diet_collection.find_one({"_id": ObjectId(diet_id)})
    updated_diet["_id"] = str(updated_diet["_id"])
    return updated_diet

@router.delete("/babies/{baby_id}/diet/{diet_id}")
async def delete_diet_record(
    baby_id: str, 
    diet_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = diet_collection.delete_one({
        "_id": ObjectId(diet_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Diet record not found")
    return {"message": "Diet record deleted successfully"}

