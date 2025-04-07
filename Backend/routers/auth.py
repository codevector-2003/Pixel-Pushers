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

    created_user["token"] = access_token

    return created_user

@router.post("/token")
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
    - **baby_id**: ID of associated baby (if exists)
    """
    # First authenticate the user
    auth_user = authenticate_user(form_data.username, form_data.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Then get the full user document from database
    user = user_collection.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = str(user["_id"])
    
    # Check for associated baby
    baby = baby_collection.find_one({"parent_id": user_id})
    baby_id = str(baby["_id"]) if baby else None

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    
    # Prepare response data
    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
    }
    
    # Add baby_id if exists
    if baby_id:
        response_data["baby_id"] = baby_id
    
    return response_data



@router.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_active_user)):
    return {"message": "This is a protected route", "user": current_user["username"]}