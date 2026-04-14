# /// main
# requires-python = ">=X.XX" TODO: Update this to the minimum Python version you want to support
# dependencies = [
#   TODO: Add any dependencies your script requires
# ]
# ///

# TODO: Update the main function to your needs or remove it.


from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, Field
from typing import List, Optional
import math

app = FastAPI(title="AWS Cloud Foundations API")

# ─── Modelos ────────────────────────────────────────────────────────────────

class AlumnoCreate(BaseModel):
    nombres: str
    apellidos: str
    matricula: str
    promedio: float

    @field_validator("nombres", "apellidos", "matricula")
    @classmethod
    def no_vacio(cls, v, info):
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} no puede estar vacío")
        return v.strip()

    @field_validator("promedio")
    @classmethod
    def promedio_valido(cls, v):
        if math.isnan(v) or math.isinf(v):
            raise ValueError("promedio debe ser un número válido")
        if v < 0 or v > 10:
            raise ValueError("promedio debe estar entre 0 y 10")
        return v


class Alumno(AlumnoCreate):
    id: int


class ProfesorCreate(BaseModel):
    model_config = {"populate_by_name": True}

    numeroEmpleado: str = Field(alias="numero_empleado")
    nombres: str
    apellidos: str
    horasClase: int = Field(alias="horas_clase")

    @field_validator("numeroEmpleado", "nombres", "apellidos")
    @classmethod
    def no_vacio(cls, v, info):
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} no puede estar vacío")
        return v.strip()

    @field_validator("horasClase")
    @classmethod
    def horas_validas(cls, v):
        if v < 0:
            raise ValueError("horasClase debe ser un número positivo")
        return v


class Profesor(ProfesorCreate):
    id: int


# ─── Almacenamiento en memoria ───────────────────────────────────────────────

alumnos: List[dict] = []
profesores: List[dict] = []
alumno_counter = 1
profesor_counter = 1

# ─── Helpers ────────────────────────────────────────────────────────────────

def validation_error_response(exc):
    errors = [{"campo": e["loc"][-1], "error": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": errors})


# ─── Endpoints Alumnos ──────────────────────────────────────────────────────

@app.get("/alumnos", status_code=200)
def get_alumnos():
    return alumnos


@app.get("/alumnos/{id}", status_code=200)
def get_alumno(id: int):
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if not alumno:
        raise HTTPException(status_code=404, detail=f"Alumno con id {id} no encontrado")
    return alumno


@app.post("/alumnos", status_code=201)
def create_alumno(data: AlumnoCreate):
    global alumno_counter
    alumno = {"id": alumno_counter, **data.model_dump()}
    alumno_counter += 1
    alumnos.append(alumno)
    return alumno


@app.put("/alumnos/{id}", status_code=200)
def update_alumno(id: int, data: AlumnoCreate):
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if not alumno:
        raise HTTPException(status_code=404, detail=f"Alumno con id {id} no encontrado")
    alumno.update(data.model_dump())
    return alumno


@app.delete("/alumnos/{id}", status_code=200)
def delete_alumno(id: int):
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if not alumno:
        raise HTTPException(status_code=404, detail=f"Alumno con id {id} no encontrado")
    alumnos.remove(alumno)
    return alumno


# ─── Endpoints Profesores ────────────────────────────────────────────────────

@app.get("/profesores", status_code=200)
def get_profesores():
    return profesores


@app.get("/profesores/{id}", status_code=200)
def get_profesor(id: int):
    profesor = next((p for p in profesores if p["id"] == id), None)
    if not profesor:
        raise HTTPException(status_code=404, detail=f"Profesor con id {id} no encontrado")
    return profesor


@app.post("/profesores", status_code=201)
def create_profesor(data: ProfesorCreate):
    global profesor_counter
    profesor = {"id": profesor_counter, **data.model_dump()}
    profesor_counter += 1
    profesores.append(profesor)
    return profesor


@app.put("/profesores/{id}", status_code=200)
def update_profesor(id: int, data: ProfesorCreate):
    profesor = next((p for p in profesores if p["id"] == id), None)
    if not profesor:
        raise HTTPException(status_code=404, detail=f"Profesor con id {id} no encontrado")
    profesor.update(data.model_dump())
    return profesor


@app.delete("/profesores/{id}", status_code=200)
def delete_profesor(id: int):
    profesor = next((p for p in profesores if p["id"] == id), None)
    if not profesor:
        raise HTTPException(status_code=404, detail=f"Profesor con id {id} no encontrado")
    profesores.remove(profesor)
    return profesor


# ─── Manejo global de errores ────────────────────────────────────────────────

from fastapi.exceptions import RequestValidationError
from fastapi import Request

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return validation_error_response(exc)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})
