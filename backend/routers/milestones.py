from fastapi import APIRouter, Depends, HTTPException  
from typing import List
from bson import ObjectId

from schemas.milestones import Milestone, MilestoneCreate
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

@router.post("/babies/{baby_id}/milestones/", response_model=Milestone)
async def create_milestone(
    baby_id: str, 
    milestone: MilestoneCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    milestone_dict = milestone.dict()
    milestone_dict["baby_id"] = baby_id
    
    result = milestone_collection.insert_one(milestone_dict)
    created_milestone = milestone_collection.find_one({"_id": result.inserted_id})
    return created_milestone

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
    return milestones

@router.get("/babies/{baby_id}/milestones/{milestone_id}", response_model=Milestone)
async def read_milestone(
    baby_id: str, 
    milestone_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    milestone = milestone_collection.find_one({
        "_id": ObjectId(milestone_id),
        "baby_id": baby_id
    })
    if milestone is None:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return milestone

@router.put("/babies/{baby_id}/milestones/{milestone_id}", response_model=Milestone)
async def update_milestone(
    baby_id: str, 
    milestone_id: str, 
    milestone_update: MilestoneCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    update_data = milestone_update.dict(exclude_unset=True)
    milestone_collection.update_one(
        {"_id": ObjectId(milestone_id), "baby_id": baby_id},
        {"$set": update_data}
    )
    updated_milestone = milestone_collection.find_one({"_id": ObjectId(milestone_id)})
    return updated_milestone

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