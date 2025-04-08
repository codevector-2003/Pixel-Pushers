from fastapi import APIRouter, Depends, HTTPException  
from typing import List
from bson import ObjectId
from datetime import datetime , date

from schemas.milestones import Milestone, MilestoneCreate , MilestoneCategory
from config import milestone_collection, baby_collection
from security import get_current_active_user

router = APIRouter(tags=["milestones"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True
0
@router.post("/babies/{baby_id}/milestones/", response_model=Milestone)
async def create_milestone(
    baby_id: str, 
    milestone: MilestoneCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    # Convert 'date' to datetime if it's not already
    milestone_dict = milestone.dict()
    milestone_dict["baby_id"] = baby_id
    
    # Ensure the date is a datetime object
    if isinstance(milestone_dict.get("date"), date):
        milestone_dict["date"] = datetime.combine(milestone_dict["date"], datetime.min.time())
    
    result = milestone_collection.insert_one(milestone_dict)
    created_milestone = milestone_collection.find_one({"_id": result.inserted_id})
    created_milestone["_id"] = str(created_milestone["_id"])
    return Milestone(**created_milestone)


@router.get("/babies/{baby_id}/milestones/", response_model=List[Milestone])
async def read_milestones(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    milestones = list(milestone_collection.find(
        {"baby_id": baby_id},
        skip=skip,
        limit=limit
    ))

    for milestone in milestones:
        milestone["_id"] = str(milestone["_id"])
    return milestones

@router.put("/babies/{baby_id}/milestones/{milestone_id}")
async def update_milestone(
    baby_id: str, 
    milestone_id: str, 
    milestone_update: MilestoneCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    update_data = milestone_update.model_dump()
    if "date" in update_data:
        update_data["date"] = datetime.combine(update_data["date"], datetime.min.time())
        
    update_data["baby_id"] = baby_id

    milestone_collection.update_one(
        {"_id": ObjectId(milestone_id), "baby_id": baby_id},
        {"$set": update_data}
    )
    updated_milestone = milestone_collection.find_one({"_id": ObjectId(milestone_id)})
    updated_milestone["_id"] = str(updated_milestone["_id"])
    return Milestone(**updated_milestone)

@router.delete("/babies/{baby_id}/milestones/{milestone_id}")
async def delete_milestone(
    baby_id: str, 
    milestone_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = milestone_collection.delete_one({
        "_id": ObjectId(milestone_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return {"message": "Milestone deleted successfully"}

