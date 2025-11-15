from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

engine_pg = create_async_engine(os.getenv("DATABASE_URL"), isolation_level="REPEATABLE READ")
# com isolation_level REPEATABLE READ, o PostgreSQL garante que todas as leituras feitas dentro de uma transação vejam um snapshot consistente dos dados, mesmo que outras transações estejam modificando os dados ao mesmo tempo.

async def teste():
    async with engine_pg.connect() as connection:
        result = await connection.execute(text("SELECT 1;"))
        print(result.all())


if __name__ == "__main__":
    asyncio.run(teste())

# Adicione aqui outras configurações do banco de dados conforme necessário. exemplo: pool_size, max_overflow, pool_timeout, etc.