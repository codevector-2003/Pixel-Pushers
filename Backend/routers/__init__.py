# app/routers/__init__.py
"""
API Routes and Endpoints

This package contains all FastAPI routers that define the application's endpoints.
Each router handles a specific domain of functionality.
"""

from .auth import router as auth_router
from .baby import router as baby_router
from .milestones import router as milestone_router
from .diet import router as diet_router
from .vaccine import router as vaccine_router
from .illness import router as illness_router
from .docters import router as doctor_router
from .settings import router as settings_router
from .allergy import router as allergy_router
from .food import router as food_router
from .recommendation import router as recommendation_router
from .weight import router as weight_router
from .height import router as height_router

__all__ = [
    "auth_router",
    "baby_router",
    "milestone_router",
    "diet_router",
    "vaccine_router",
    "illness_router",
    "growth_router",
    "doctor_router",
    "settings_router",
    "allergy_router",
    "food_router",
    "recommendation_router"
]