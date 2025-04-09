from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routers import (
    auth_router,
    baby_router,
    diet_router,
    doctor_router,
    milestone_router,
    settings_router,
    vaccine_router,
    illness_router,
    allergy_router,
    food_router,
    recommendation_router,   
    weight_router,
    height_router,
)

app = FastAPI(title="Smart Baby LK", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],                       
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(baby_router)
app.include_router(diet_router)
app.include_router(doctor_router)
app.include_router(milestone_router)
app.include_router(settings_router)
app.include_router(vaccine_router)
app.include_router(illness_router)
app.include_router(weight_router)
app.include_router(height_router)
app.include_router(allergy_router)
app.include_router(food_router)
app.include_router(recommendation_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Smart Baby LK",
        version="1.0.0",
        description="API for Smart Baby LK application",
        routes=app.routes,
    )
    
    # Add security definitions
    openapi_schema["components"] = {
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "tokenUrl": "token",
                        "scopes": {}
                    }
                }
            }
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

