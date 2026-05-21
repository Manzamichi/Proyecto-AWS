import math

from pydantic import BaseModel, StrictStr, field_validator


class AlumnoCreate(BaseModel):
    id: int | None = None
    nombres: StrictStr
    apellidos: StrictStr
    matricula: StrictStr
    promedio: float
    password: str | None = None

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
        if v < 0:
            raise ValueError("promedio debe ser positivo")
        return v


class AlumnoResponse(BaseModel):
    id: int
    nombres: str
    apellidos: str
    matricula: str
    promedio: float
    fotoPerfilUrl: str | None = None


class LoginRequest(BaseModel):
    password: str


class SessionRequest(BaseModel):
    sessionString: str
