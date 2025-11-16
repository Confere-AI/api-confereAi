from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.config.config_db import engine_pg

# Create a sessionmaker bound to the existing engine
async_session = async_sessionmaker(engine_pg, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
