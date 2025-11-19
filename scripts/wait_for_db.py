#!/usr/bin/env python3
"""Espera até que o banco de dados esteja aceitando conexões.

Uso: este script lê `DATABASE_URL` do ambiente e tenta conectar usando
SQLAlchemy (async engine). Retorna 0 ao conectar com sucesso, 1 se
`DATABASE_URL` não estiver configurada, ou 2 se exceder o timeout.
"""
import asyncio
import os
import sys
import time
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logging.error("DATABASE_URL is not set")
    sys.exit(1)

async def wait_for_db(url: str, timeout: int = 60, interval: int = 2) -> int:
    logging.basicConfig(level=logging.INFO)
    engine = create_async_engine(url)
    deadline = time.time() + timeout
    try:
        while time.time() < deadline:
            try:
                async with engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                    await engine.dispose()
                    logging.info("Database is available")
                    return 0
            except Exception as exc:  # pragma: no cover - retry logic
                logging.warning("Database unavailable, retrying in %ss... (%s)", interval, exc)
                await asyncio.sleep(interval)
        await engine.dispose()
        logging.error("Timed out after %ss waiting for database", timeout)
        return 2
    finally:
        try:
            await engine.dispose()
        except Exception:
            pass


if __name__ == "__main__":
    timeout = int(os.getenv("WAIT_TIMEOUT", "60"))
    interval = int(os.getenv("WAIT_INTERVAL", "2"))
    rc = asyncio.run(wait_for_db(DATABASE_URL, timeout=timeout, interval=interval))
    sys.exit(rc)
