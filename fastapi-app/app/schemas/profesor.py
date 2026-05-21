from pydantic import BaseModel, StrictStr, field_validator


class ProfesorCreate(BaseModel):
    id: int | None = None
    numeroEmpleado: int
    nombres: StrictStr
    apellidos: StrictStr
    horasClase: int

    @field_validator("nombres", "apellidos")
    @classmethod
    def no_vacio(cls, v, info):
        if not v or not str(v).strip():
            raise ValueError(f"{info.field_name} no puede estar vacío")
        return str(v).strip()

    @field_validator("numeroEmpleado")
    @classmethod
    def empleado_valido(cls, v):
        if v < 0:
            raise ValueError("numeroEmpleado debe ser positivo")
        return v

    @field_validator("horasClase")
    @classmethod
    def horas_validas(cls, v):
        if v < 0:
            raise ValueError("horasClase debe ser un número positivo")
        return v


class ProfesorResponse(BaseModel):
    id: int
    numeroEmpleado: int
    nombres: str
    apellidos: str
    horasClase: int
