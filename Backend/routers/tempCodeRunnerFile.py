@router.post("/babies/{baby_id}/illness/", response_model=IllnessRecord)
async def create_illness_record(
    baby_id: str, 
    illness: IllnessRecordCreate, 
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    illness_data = illness.model_dump()
    illness_data["baby_id"] = baby_id
    

    
    result = illness_collection.insert_one(illness_data)
    created_illness = illness_collection.find_one({"_id": result.inserted_id})
    created_illness["_id"] = str(created_illness["_id"])
    return IllnessRecord(**created_illness)