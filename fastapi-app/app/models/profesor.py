from sqlalchemy import Column, Integer, String

from app.database import Base


class Profesor(Base):
    __tablename__ = "profesores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numeroEmpleado = Column(Integer, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    horasClase = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "numeroEmpleado": self.numeroEmpleado,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "horasClase": self.horasClase,
        }
