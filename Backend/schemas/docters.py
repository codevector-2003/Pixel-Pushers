from typing import List, Optional, Any, Dict
from datetime import datetime
from bson import ObjectId
from pydantic import Field, ConfigDict, BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str) and ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId")

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

class ChatMessageBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

class ChatMessage(ChatMessageBase):
    text: str

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Why my milk is red?"
            }
        }

class ChatMessageResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    user_id: str
    sender: str
    text: str
    timestamp: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )