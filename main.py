from contextlib import asynccontextmanager
import time
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse

from infra.database import close_db_connection, connect_to_db, db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the lifespan context manager
    await connect_to_db(app)

    yield

    # End the lifespan context manager
    await close_db_connection(app)


app = FastAPI(lifespan=lifespan)
METRICS: List[float] = []


def get_conn():
    yield db.db_pool


@app.get("/clientes/{cliente_id}")
async def ler_cliente(cliente_id: int, conn=Depends(get_conn)):
    
    start_time = time.perf_counter()
    row = await conn.fetchrow(
        "SELECT id, nome, email FROM clientes WHERE id = $1", cliente_id
    )
    end_time = time.perf_counter()
    
    global METRICS
    METRICS.append(end_time - start_time)

    if not row:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    row = dict(row)
    return JSONResponse(row)


@app.get("/metrics")
async def metrics():
    global METRICS
    return JSONResponse({"status": "ok", "message": METRICS})


@app.put("/clean-metrics")
async def clean_metrics():

    global METRICS
    METRICS.clear()
    return JSONResponse({"status": "ok", "message": "Metrics cleaned."})
