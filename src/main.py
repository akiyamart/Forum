import uvicorn
from fastapi import FastAPI, APIRouter
from src.api.main_handlers import user_router

app = FastAPI(
    title="Forum"
)

# Создание инстанса для всех роутеров (роутер, который собирает в себя остальные роутеры)
main_api_router = APIRouter()

# Создание тестового роутера (ПОТОМ УДАЛИТЬ)
test_router = APIRouter()

@test_router.get("/ping")
async def read_test():
    return "Pong"

# Подключение всех "младших роутеров" к основному роутеру
main_api_router.include_router(test_router)
main_api_router.include_router(
    user_router, 
    prefix="/user", 
    tags=["user"]
)
# Подключение основного роутера к приложению
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
