# app/__init__.py
"""
smartBaby Application Package

This package contains all the core functionality of the smartBaby backend:
- API routes
- Database models and connections
- Schemas and data validation
- Utility functions
"""

from .main import app
from .routers import (
    auth_router,
    baby_router,
    diet_router,
    doctor_router,
    milestone_router,
    settings_router,
    vaccine_router,
    illness_router,
    growth_router,
)
from security import (get_current_active_user, 
                      get_current_user, 
                      authenticate_user, 
                      verify_password, 
                      get_password_hash, 
                      create_access_token,
                      SECRET_KEY,
                      ALGORITHM,
                      ACCESS_TOKEN_EXPIRE_MINUTES)

from .schemas import (
    User,
    UserCreate,
    UserInDB,
    Token,
    TokenData,
    Baby,
    BabyBase,
    BabyCreate,
    Milestone,
    MilestoneBase,
    MilestoneCreate,
    DietRecord,
    DietRecordBase,
    DietRecordCreate,
    VaccineRecord,
    VaccineRecordBase,
    VaccineRecordCreate,
    IllnessRecord,
    IllnessRecordBase,
    IllnessRecordCreate,
    GrowthRecord,
    GrowthRecordBase,
    GrowthRecordCreate
)
