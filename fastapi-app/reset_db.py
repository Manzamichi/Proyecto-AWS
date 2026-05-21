"""Resetea la base de datos relacional antes de las pruebas."""
from app.database import Base, engine, init_db

Base.metadata.drop_all(bind=engine)
init_db()
print("Base de datos formateada y lista para pruebas.")
