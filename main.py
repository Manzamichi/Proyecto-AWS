from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
from typing import List, Any
import math

app = FastAPI(title="AWS Cloud Foundations API")


class AlumnoCreate(BaseModel):
    nombres: str
    apellidos: str
    matricula: str
    promedio: float

    @field_validator("nombres", "apellidos", "matricula")
    @classmethod
    def no_vacio(cls, v, info):
        if not v or not str(v).strip():
            raise ValueError(f"{info.field_name} no puede estar vacío")
        return str(v).strip()

    @field_validator("promedio")
    @classmethod
    def promedio_valido(cls, v):
        if math.isnan(v) or math.isinf(v):
            raise ValueError("promedio debe ser un número válido")
        if v < 0 or v > 10:
            raise ValueError("promedio debe estar entre 0 y 10")
        return v


class ProfesorCreate(BaseModel):
    numeroEmpleado: Any
    nombres: str
    apellidos: str
    horasClase: int

    @field_validator("numeroEmpleado")
    @classmethod
    def empleado_to_str(cls, v):
        if v is None or str(v).strip() == "":
            raise ValueError("numeroEmpleado no puede estar vacío")
        return str(v).strip()

    @field_validator("nombres", "apellidos")
    @classmethod
    def no_vacio(cls, v, info):
        if not v or not str(v).strip():
            raise ValueError(f"{info.field_name} no puede estar vacío")
        return str(v).strip()

    @field_validator("horasClase")
    @classmethod
    def horas_validas(cls, v):
        if v < 0:
            raise ValueError("horasClase debe ser un número positivo")
        return v


alumnos: List[dict] = []
profesores: List[dict] = []
alumno_counter = 1
profesor_counter = 1


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
async def create_alumno(request: Request, data: AlumnoCreate):
    global alumno_counter
    body = await request.json()
    client_id = body.get("id")
    alumno = {"id": client_id if client_id else alumno_counter, **data.model_dump()}
    if not client_id:
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
async def create_profesor(request: Request, data: ProfesorCreate):
    global profesor_counter
    body = await request.json()
    client_id = body.get("id")
    profesor = {"id": client_id if client_id else profesor_counter, **data.model_dump()}
    if not client_id:
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": "Bad request"})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})