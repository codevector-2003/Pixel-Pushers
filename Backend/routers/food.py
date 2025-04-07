from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from schemas.diet import foodRecord, foodCreate
from config import food_collection, baby_collection
from security import get_current_active_user

router = APIRouter(tags=["food"])

def verify_baby_ownership(baby_id: str, user_id: str):
    baby = baby_collection.find_one({
        "_id": ObjectId(baby_id),
        "parent_id": user_id
    })
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.post("/babies/{baby_id}/foods/", response_model=foodRecord)
async def create_food(
    baby_id: str, 
    food: foodCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    food_data = food.model_dump()
    food_data["baby_id"] = baby_id
    
    result = food_collection.insert_one(food_data)
    created_food = food_collection.find_one({"_id": result.inserted_id})
    created_food["_id"] = str(created_food["_id"])
    return foodRecord(**created_food)

@router.get("/babies/{baby_id}/foods/", response_model=List[foodRecord])
async def read_foods(
    baby_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    foods = list(food_collection.find(
        {"baby_id": baby_id},
        skip=skip,
        limit=limit
    ))
    return [foodRecord(**f) for f in foods]

@router.delete("/babies/{baby_id}/foods/{food_id}")
async def delete_food(
    baby_id: str, 
    food_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    result = food_collection.delete_one({
        "_id": ObjectId(food_id),
        "baby_id": baby_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Food not found")
    return {"message": "Food deleted successfully"}