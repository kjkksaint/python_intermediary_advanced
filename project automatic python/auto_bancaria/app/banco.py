import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import logging

logger = logging.getLogger(__name__)

db = declarative_base()
engine = None
session = None

def init_db(app):
    global engine, session
    db_url = app.config['DATABASE_URL'] or 'sqlite:///config/database.db'
    engine = create_engine(db_url, pool_pre_ping=True, future=True)
    session = scoped_session(sessionmaker(bind=engine))
    # Import models to register metadata
    from . import models
    db.metadata.create_all(engine)
    logger.info("Banco inicializado: %s", db_url)
