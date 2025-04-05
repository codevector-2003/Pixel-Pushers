from pydantic import BaseModel, Field
from typing import Optional 
from datetime import date
from bson import ObjectId

class PyObject(ObjectId):
    @classmethod
    def _get_validators_(cls):
        yield cls.__validate

    @classmethod
    def validate(cls,v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectId")
        return ObjectId(v)
    
    @classmethod
    def _modify_schema_(cls, field_schema):
        field_schema.update(type="string")


class MilestoneBase(BaseModel):
    name: str
    date: date
    category: str #Emotional, Cognitive, Movement, Language
    notes:Optional[str] =None

class MilestoneCreate(MilestoneBase):
    pass

class Milestone(MilestoneBase):
    id: str= Field(default_factory=PyObject,alias="_id")
    baby_id:str

    class Config:
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "First smile",
                "date": "2023-03-15",
                "category": "Emotional",
                "notes": "Baby smiled for the first time!",
                "baby_id": "507f1f77bcf86cd799439011"
            }
        }