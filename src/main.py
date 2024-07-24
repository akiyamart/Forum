import uvicorn
from fastapi import FastAPI, APIRouter
from src.api.services.users.endpoints import user_router

app = FastAPI(
    title="Forum"
)

main_router = APIRouter()

main_router.include_router(
    user_router, 
    prefix="/user", 
    tags=["User"]
)   

app.include_router(main_router)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
