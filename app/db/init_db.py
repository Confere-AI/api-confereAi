import asyncio
from app.config.config_db import engine_pg
from app.models.base import Base


async def init_db() -> None:
    """Cria todas as tabelas do metadata declarativo (async).

    Use com `docker compose exec web python -c "import asyncio; from app.db.init_db import init_db; asyncio.run(init_db())"`
    """

    async with engine_pg.begin() as conn:
        # run_sync permite executar o create_all no loop sync
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
