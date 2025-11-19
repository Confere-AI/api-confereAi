from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logging.error("DATABASE_URL is not set. Configure .env or environment variables.")

engine_pg = create_async_engine(DATABASE_URL, isolation_level="REPEATABLE READ")
# com isolation_level REPEATABLE READ, o PostgreSQL garante que todas as leituras feitas dentro de uma transação vejam um snapshot consistente dos dados, mesmo que outras transações estejam modificando os dados ao mesmo tempo.

async def teste():
    async with engine_pg.connect() as connection:
        result = await connection.execute(text("SELECT 1;"))
        logging.info("DB test query result: %s", result.all())


if __name__ == "__main__":
    asyncio.run(teste())

# Adicione aqui outras configurações do banco de dados conforme necessário. exemplo: pool_size, max_overflow, pool_timeout, etc.