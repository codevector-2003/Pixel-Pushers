from pydantic import BaseModel, Field, GetJsonSchemaHandler , GetCoreSchemaHandler, root_validator
from pydantic.json_schema import JsonSchemaValue
from typing import  Any, Dict, Optional, Union
from datetime import date, datetime
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> Dict[str, Any]:
        json_schema = handler(core_schema)
        json_schema.update(type="string", format="objectid")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )



class MilestoneBase(BaseModel):
    name: str
    date: date
    category: str #Emotional, Cognitive, Movement, Language
    notes:Optional[str] =None

class MilestoneCreate(MilestoneBase):
    pass

class Milestone(MilestoneBase):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    baby_id:str

    @root_validator(pre=True)
    def convert_date_to_datetime(cls, values):
        if 'date' in values and isinstance(values['date'], date):
            # Convert datetime.date to datetime.datetime
            values['date'] = datetime.combine(values['date'], datetime.min.time())
        return values

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name= True
        json_schema_extra = {
            "example": {
                "name": "First smile",
                "date": "2023-03-15",
                "category": "Emotional",
                "notes": "Baby smiled for the first time!",
                "baby_id": "507f1f77bcf86cd799439011"
            }
        }