from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from Avenger import FDB_URL, LOGGER as log

if FDB_URL and FDB_URL.startswith("postgres://"):
    FDB_URL = FDB_URL.replace("postgres://", "postgresql://", 1)

def start() -> scoped_session:
    engine = create_engine(FDB_URL, client_encoding="utf8")
    log.info("[PostgreSQL] Connecting to database......")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
try:
    SESSION = start()
except Exception as e:
    log.exception(f'[PostgreSQL] Failed to connect due to {e}')
    exit()
   
log.info("[PostgreSQL] Connection successful, session started.")
