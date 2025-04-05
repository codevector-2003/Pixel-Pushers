from pydantic import BaseModel, validator
import re

class SignupRequest(BaseModel):
    name: str
    username: str
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class MilestoneData(BaseModel):
    username: str

