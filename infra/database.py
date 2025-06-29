import os
from typing import Optional
import asyncpg

from asyncpg import Pool
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    db_pool: Optional[Pool]


db = DatabaseConnection()
db.db_pool = None


async def connect_to_db(app: FastAPI):
    # Como o app é um singleton,
    # é possível criar esse pool e adicionar no estado do app
    db.db_pool = await asyncpg.create_pool(
        min_size=5,
        max_size=20,
        dsn=os.getenv("DATABASE_URL"),
    )


async def close_db_connection(app: FastAPI):
    await db.db_pool.close()
    app.state.db_pool = None
