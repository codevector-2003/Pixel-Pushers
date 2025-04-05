from pydantic import BaseModel, Field , GetJsonSchemaHandler , GetCoreSchemaHandler
from typing import Optional , Any, Dict
from datetime import date
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
class DietRecordBase(BaseModel):
    date: date
    food_name: str
    amount: float
    calories: float
    nutrients: str
    notes: Optional[str] = None

class DietRecordCreate(DietRecordBase):
    pass

class DietRecord(DietRecordBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    baby_id: str
    
    class Config:
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "date": "2023-04-10",
                "food_name": "Banana puree",
                "amount": 50.0,
                "calories": 45.0,
                "nutrients": "Potassium, Vitamin C",
                "notes": "Baby liked it very much",
                "baby_id": "507f1f77bcf86cd799439011"
            }
        }