import os
import sys
from logging.config import fileConfig
import asyncio
from dotenv import load_dotenv

# adiciona a raiz do projeto ao PYTHONPATH para o Alembic rodando dentro do container
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models.base import Base
import app.models 

load_dotenv()


config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
# from myapp import mymodel

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_server_default=True)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an async engine."""
    database_url = os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
    connectable = create_async_engine(database_url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
