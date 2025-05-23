from pydantic import BaseModel, Field, GetJsonSchemaHandler , GetCoreSchemaHandler, root_validator
from pydantic.json_schema import JsonSchemaValue
from typing import  Any, Dict, Optional, Union
from bson import ObjectId
from pydantic_core import core_schema
from enum import Enum
from datetime import date


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

    
class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"

class BabyBase(BaseModel):
    Gurdian_name: str
    birth_date: date
    gender: Optional[GenderEnum] = None
    blood_Type: str
    preterm: Optional[bool] = None


class BabyCreate(BabyBase):
    pass


class Baby(BabyBase):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    parent_id: str

    @root_validator(pre=True)
    def convert_objectid_to_string(cls, values):
        if "_id" in values and isinstance(values["_id"], ObjectId):
            values["_id"] = str(values["_id"])  # Convert ObjectId to string
        return values

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "name": "Emma Smith",
                "birth_date": "2023-01-15",
                "gender": "female",
                "birth_weight": 3.2,
                "birth_height": 50.5,
                "parent_id": "507f1f77bcf86cd799439011"
            }
        }
