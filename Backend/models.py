from pydantic import BaseModel, validator
import re

class SignupRequest(BaseModel):
    name: str
    username: str
    password: str
    confirm_password: str

    @validator("username")
    def validate_username(cls, value):
        if len(value) < 8:
            raise ValueError("Username must be at least 8 characters long")
        return value

    @validator("password")
    def validate_password(cls, value):
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value

    @validator("confirm_password")
    def passwords_match(cls, value, values):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match")
        return value

class LoginRequest(BaseModel):
    username: str
    password: str

class MilestoneData(BaseModel):
    username: str

