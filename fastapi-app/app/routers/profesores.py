from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.profesor import Profesor
from app.schemas.profesor import ProfesorCreate

router = APIRouter(prefix="/profesores", tags=["profesores"])


def _get_or_404(db: Session, id_val: str) -> Profesor:
    try:
        id_int = int(id_val)
    except ValueError:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    profesor = db.get(Profesor, id_int)
    if not profesor:
        raise HTTPException(status_code=404, detail=f"Profesor con id {id_int} no encontrado")
    return profesor


@router.get("", status_code=200)
def get_profesores(db: Session = Depends(get_db)):
    return [p.to_dict() for p in db.query(Profesor).all()]


@router.get("/{id}", status_code=200)
def get_profesor(id: str, db: Session = Depends(get_db)):
    return _get_or_404(db, id).to_dict()


@router.post("", status_code=201)
def create_profesor(data: ProfesorCreate, db: Session = Depends(get_db)):
    profesor = Profesor(
        numeroEmpleado=data.numeroEmpleado,
        nombres=data.nombres,
        apellidos=data.apellidos,
        horasClase=data.horasClase,
    )
    if data.id is not None:
        profesor.id = data.id
    db.add(profesor)
    db.commit()
    db.refresh(profesor)
    return profesor.to_dict()


@router.put("/{id}", status_code=200)
def update_profesor(id: str, data: ProfesorCreate, db: Session = Depends(get_db)):
    profesor = _get_or_404(db, id)
    profesor.numeroEmpleado = data.numeroEmpleado
    profesor.nombres = data.nombres
    profesor.apellidos = data.apellidos
    profesor.horasClase = data.horasClase
    db.commit()
    db.refresh(profesor)
    return profesor.to_dict()


@router.delete("/{id}", status_code=200)
def delete_profesor(id: str, db: Session = Depends(get_db)):
    profesor = _get_or_404(db, id)
    data = profesor.to_dict()
    db.delete(profesor)
    db.commit()
    return data
