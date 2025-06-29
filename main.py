from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException

from infra.database import close_db_connection, connect_to_db, db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the lifespan context manager
    await connect_to_db(app)

    yield

    # End the lifespan context manager
    await close_db_connection(app)


app = FastAPI(lifespan=lifespan)


def get_conn():
    yield db.db_pool


@app.get("/clientes/{cliente_id}")
async def ler_cliente(cliente_id: int, conn=Depends(get_conn)):
    
    row = await conn.fetchrow(
        "SELECT id, nome, email FROM clientes WHERE id = $1", cliente_id
    )
    if not row:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    row = dict(row)
    return JSONResponse(row)
