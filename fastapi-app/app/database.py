from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# pool_pre_ping evita errores por conexiones muertas a RDS.
# connect_args solo aplica a SQLite (tests).
connect_args = {"check_same_thread": False} if settings.sqlalchemy_uri.startswith("sqlite") else {}

engine = create_engine(
    settings.sqlalchemy_uri,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: abre una sesión por request y la cierra al final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Crea las tablas relacionales si no existen."""
    # Importa los modelos para registrarlos en el metadata antes de create_all.
    from app.models import alumno, profesor  # noqa: F401

    Base.metadata.create_all(bind=engine)
