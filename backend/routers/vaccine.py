from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId

from schemas.vaccine import VaccineRecord, VaccineRecordCreate
from config import vaccine_collection, baby_collection
from security import get_current_active_user

router = APIRouter(tags=["vaccines"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/{baby_id}/vaccines/", response_model=VaccineRecord)
async def create_vaccine_record(
    baby_id: str, 
    vaccine: VaccineRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    vaccine_dict = vaccine.dict()
    vaccine_dict["baby_id"] = baby_id
    
    result = vaccine_collection.insert_one(vaccine_dict)
    created_vaccine = vaccine_collection.find_one({"_id": result.inserted_id})
    return created_vaccine

@router.get("/babies/{baby_id}/vaccines/", response_model=List[VaccineRecord])
async def read_vaccine_records(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    vaccines = list(vaccine_collection.find(
        {"baby_id": baby_id},
        skip=skip,
        limit=limit
    ))
    return vaccines

@router.get("/babies/{baby_id}/vaccines/{vaccine_id}", response_model=VaccineRecord)
async def read_vaccine_record(
    baby_id: str, 
    vaccine_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    vaccine = vaccine_collection.find_one({
        "_id": ObjectId(vaccine_id),
        "baby_id": baby_id
    })
    if vaccine is None:
        raise HTTPException(status_code=404, detail="Vaccine record not found")
    return vaccine

@router.put("/babies/{baby_id}/vaccines/{vaccine_id}", response_model=VaccineRecord)
async def update_vaccine_record(
    baby_id: str, 
    vaccine_id: str, 
    vaccine_update: VaccineRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    update_data = vaccine_update.dict(exclude_unset=True)
    vaccine_collection.update_one(
        {"_id": ObjectId(vaccine_id), "baby_id": baby_id},
        {"$set": update_data}
    )
    updated_vaccine = vaccine_collection.find_one({"_id": ObjectId(vaccine_id)})
    return updated_vaccine

@router.delete("/babies/{baby_id}/vaccines/{vaccine_id}")
async def delete_vaccine_record(
    baby_id: str, 
    vaccine_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = vaccine_collection.delete_one({
        "_id": ObjectId(vaccine_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vaccine record not found")
    return {"message": "Vaccine record deleted successfully"}