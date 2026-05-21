from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Alumno(Base):
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    matricula = Column(String(50), nullable=False, unique=True)
    promedio = Column(Float, nullable=False)
    password = Column(String(255), nullable=True)
    fotoPerfilUrl = Column(String(500), nullable=True)

    def to_dict(self):
        # password NUNCA se expone.
        return {
            "id": self.id,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "matricula": self.matricula,
            "promedio": self.promedio,
            "fotoPerfilUrl": self.fotoPerfilUrl,
        }
