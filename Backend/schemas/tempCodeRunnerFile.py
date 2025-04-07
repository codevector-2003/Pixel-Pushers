from pydantic import BaseModel, EmailStr, Field, GetJsonSchemaHandler , GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from typing import  Any, Dict, Optional, Union
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


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    is_active: bool = True
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True 

class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
