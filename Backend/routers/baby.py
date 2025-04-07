from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime, date

from schemas.baby import Baby, BabyCreate
from config import baby_collection , vaccine_collection
from security import get_current_active_user
from utils.baby_vaccination_db import STANDARD_VACCINES
from schemas.vaccine import Vaccine

router = APIRouter(tags=["babies"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/", response_model=Baby)
async def create_baby(
    baby: BabyCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    baby_dict = baby.dict()
    if isinstance(baby_dict.get("birth_date"), date):
        baby_dict["birth_date"] = datetime.combine(baby_dict["birth_date"], datetime.min.time())

    baby_dict["parent_id"] = str(current_user["_id"])
    
    result = baby_collection.insert_one(baby_dict)
    created_baby = baby_collection.find_one({"_id": result.inserted_id})

    await initialize_standard_vaccines(str(result.inserted_id), current_user)
    return created_baby


@router.get("/babies/", response_model=List[Baby])
async def read_babies(
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    babies = list(baby_collection.find(
        {"parent_id": str(current_user["_id"])},
        skip=skip,
        limit=limit
    ))
    return [Baby(**baby) for baby in babies]

@router.get("/babies/{baby_id}", response_model=Baby)
async def read_baby(
    baby_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": str(current_user["_id"])
    })
    if baby is None:
        raise HTTPException(status_code=404, detail="Baby not found")
    return baby

@router.put("/babies/{baby_id}", response_model=Baby)
async def update_baby(
    baby_id: str, 
    baby_update: BabyCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    update_data = baby_update.dict(exclude_unset=True)

    if isinstance(update_data.get("birth_date"), date):
        update_data["birth_date"] = datetime.combine(update_data["birth_date"], datetime.min.time())
    
    baby_collection.update_one(
        {"_id": ObjectId(baby_id)},
        {"$set": update_data}
    )
    updated_baby = baby_collection.find_one({"_id": ObjectId(baby_id)})
    updated_baby["_id"] = str(updated_baby["_id"])
    return updated_baby

@router.delete("/babies/{baby_id}")
async def delete_baby(
    baby_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = baby_collection.delete_one({"_id": ObjectId(baby_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Baby not found")
    return {"message": "Baby deleted successfully"}

@router.post("/babies/{baby_id}/vaccines/initialize", response_model=List[Vaccine])
async def initialize_standard_vaccines(
    baby_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))

    # Delete existing vaccines for the baby
    vaccine_collection.delete_many({"baby_id": baby_id})

    # Insert standard vaccines with added fields
    vaccines = []
    for vaccine_data in STANDARD_VACCINES:
        vaccine_data_with_meta = {
            **vaccine_data,
            "baby_id": baby_id,
            "given": False
        }
        result = vaccine_collection.insert_one(vaccine_data_with_meta)
        inserted_vaccine = vaccine_collection.find_one({"_id": result.inserted_id})
        inserted_vaccine["_id"] = str(inserted_vaccine["_id"])
        vaccines.append(inserted_vaccine)

    return vaccines
