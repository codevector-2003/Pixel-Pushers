from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import user_collection
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from routers import auth , milestones , baby , growth

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],                       
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(milestones.router)
app.include_router(baby.router)
app.include_router(growth.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8078)



""""

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/login")
async def login(request: LoginRequest):
    # Check if user exists
    user = user_collection.find_one({"username": request.username})
    if not user:
        return JSONResponse(status_code=400, content={"message": "User does not exist"})

    # Check if password is correct
    if not pwd_context.verify(request.password, user["password"]):
        return JSONResponse(status_code=400, content={"message": "Incorrect password"})
    
    return {"message": "Login successful"}


@app.post("/signup")
async def signup(request: SignupRequest):
    # Check if user already exists
    if user_collection.find_one({"username": request.username}):
        return JSONResponse(status_code=400, content={"message": "User already exists"})

    # Hash password
    hashed_password = pwd_context.hash(request.password)

    # Insert user details into the database
    user_collection.insert_one({"username": request.username, "password": hashed_password})

    return {"message": "User registered successfully"}


@app.get("/users")
def get_all_users():
    users = list(user_collection.find())

    for user in users:
        user["_id"] = str(user["_id"])

    return users  


"""
