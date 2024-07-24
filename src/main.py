import uvicorn
from fastapi import FastAPI, APIRouter
from src.api.handlers.users import user_router
from src.api.handlers.roles import role_router
from src.api.handlers.auth import login_router

app = FastAPI(
    title="Forum"
)

main_router = APIRouter()

main_router.include_router(
    user_router, 
    prefix="/user", 
    tags=["User"]
)   

main_router.include_router(
    role_router,
    prefix="/roles",
    tags=["Roles"]
)
main_router.include_router(
    login_router,
    prefix="/auth",
    tags=["Auth"]
)


app.include_router(main_router)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
