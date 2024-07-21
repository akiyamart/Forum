from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE_URL

# Для создания фабрики сессий 
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Сама фабрика сессий подключения с бд 
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def connect_to_db(): 
    try: 
        session: AsyncSession = async_session()
        yield session
    finally: 
        await session.close()