# app/schemas/__init__.py
"""
Data Schemas and Validation Models

This package contains all Pydantic models used for:
- Request validation
- Response serialization
- Data transfer objects
"""

from .user import User, UserCreate, UserInDB, Token, TokenData
from .baby import Baby, BabyBase, BabyCreate
from .milestones import Milestone, MilestoneBase, MilestoneCreate
from .diet import DietRecord, DietRecordBase, DietRecordCreate
from .vaccine import VaccineRecord, VaccineRecordBase, VaccineRecordCreate
from .illness import IllnessRecord, IllnessRecordBase, IllnessRecordCreate
from .growth import GrowthRecord, GrowthRecordBase, GrowthRecordCreate

__all__ = [
    "User", "UserCreate", "UserInDB", "Token", "TokenData",
    "Baby", "BabyBase", "BabyCreate",
    "Milestone", "MilestoneBase", "MilestoneCreate",
    "DietRecord", "DietRecordBase", "DietRecordCreate",
    "VaccineRecord", "VaccineRecordBase", "VaccineRecordCreate",
    "IllnessRecord", "IllnessRecordBase", "IllnessRecordCreate",
    "GrowthRecord", "GrowthRecordBase", "GrowthRecordCreate"
]