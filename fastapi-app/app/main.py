from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database import init_db
from app.routers import alumnos, profesores


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas relacionales al arrancar.
    init_db()
    yield


app = FastAPI(title="AWS Cloud Foundations API", lifespan=lifespan)

app.include_router(alumnos.router)
app.include_router(profesores.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": "Bad request"})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})
