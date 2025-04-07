from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

from schemas.user import User, UserCreate, Token
from config import user_collection , baby_collection
from security import (
    get_password_hash,
    create_access_token,
    authenticate_user,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


router = APIRouter(tags=["authentication"])

@router.post("/signup")
async def signup(user: UserCreate):
    # Check if user exists
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    user_dict["is_active"] = True
    del user_dict["password"]
    
    result = user_collection.insert_one(user_dict)
    created_user = user_collection.find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": created_user["username"]},
        expires_delta=access_token_expires
    )

    baby_id = baby_collection.find_one({"parent_id": str(created_user["_id"])})

    if baby_id:
        created_user["baby_id"] = str(baby_id["_id"])

    created_user["token"] = access_token

    return created_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    OAuth2 compatible token login, get an access token for future requests
    
    - **username**: Your username
    - **password**: Your password
    
    Returns:
    - **access_token**: JWT token to be used in Authorization header
    - **token_type**: Will always be "bearer"
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create token with username as subject
    access_token = create_access_token(
        data={"sub": user["username"]},  # 'sub' is standard JWT field for subject
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",  # Must be "bearer" for OAuth2 compatibility
    }

@router.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_active_user)):
    return {"message": "This is a protected route", "user": current_user["username"]}