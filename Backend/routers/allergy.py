from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from schemas.diet import allergyRecord, allergyCreate
from config import allergy_collection, baby_collection
from security import get_current_active_user

router = APIRouter(tags=["allergy"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/{baby_id}/allergies/", response_model=allergyRecord)
async def create_allergy(
    baby_id: str, 
    allergy: allergyCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    allergy_dict = allergy.dict()
    allergy_dict["baby_id"] = baby_id
    
    result = allergy_collection.insert_one(allergy_dict)
    created_allergy = allergy_collection.find_one({"_id": result.inserted_id})
    return allergyRecord(**created_allergy)

@router.get("/babies/{baby_id}/allergies/", response_model=List[allergyRecord])
async def read_allergies(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    allergies = list(allergy_collection.find(
        {"baby_id": baby_id},
        skip=skip,
        limit=limit
    ))
    return [allergyRecord(**a) for a in allergies]

@router.delete("/babies/{baby_id}/allergies/{allergy_id}")
async def delete_allergy(
    baby_id: str, 
    allergy_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = allergy_collection.delete_one({
        "_id": ObjectId(allergy_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return {"message": "Allergy deleted successfully"}