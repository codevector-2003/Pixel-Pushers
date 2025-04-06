from pydantic import BaseModel, Field , GetJsonSchemaHandler , GetCoreSchemaHandler
from typing import Optional , Any, Dict
from datetime import date
from bson import ObjectId
from pydantic_core import core_schema 
from pydantic import ConfigDict

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

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,  
    )


class allergy(BaseModel):
    name: str

class allergyCreate(allergy):
    pass   

class allergyRecord(allergy):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    baby_id: str

    model_config = ConfigDict(
    json_encoders={ObjectId: str},
    populate_by_name=True,
    json_schema_extra={
        "example": {
            "name": "Peanuts",
            "baby_id": "507f1f77bcf86cd799439011"
        }
    }
)

class food(BaseModel):
    name: str

class foodCreate(food):
    pass   

class foodRecord(food):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    baby_id: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "food": "Peanuts",
                "baby_id": "507f1f77bcf86cd799439011"
            }
        }
    )