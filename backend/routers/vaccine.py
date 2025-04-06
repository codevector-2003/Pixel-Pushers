from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from schemas.vaccine import Vaccine
from datetime import date
from typing import Optional
from config import vaccine_collection, baby_collection
from security import get_current_active_user
from utils.baby_vaccination_db import STANDARD_VACCINES

router = APIRouter(tags=["vaccines"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.put("/babies/{baby_id}/vaccines/{vaccine_id}/mark", response_model=Vaccine)
async def mark_vaccine_as_given(
    baby_id: str,
    vaccine_id: str,
    given_date: date,
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    update_data = {
        "given": True,
        "given_date": given_date
    }
    
    vaccine_collection.update_one(
        {"_id": ObjectId(vaccine_id), "baby_id": baby_id},
        {"$set": update_data}
    )
    updated_vaccine = vaccine_collection.find_one({"_id": ObjectId(vaccine_id)})
    return updated_vaccine

@router.get("/babies/{baby_id}/vaccines/", response_model=List[Vaccine])
async def read_vaccines(
    baby_id: str,
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    vaccines = list(vaccine_collection.find({"baby_id": baby_id} , skip=skip, limit=limit))
    return vaccines

