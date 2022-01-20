from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, TIMESTAMP, MetaData
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy.pool import Pool
from sqlalchemy.event import listens_for, listen

from .config import get_settings
settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    # connect_args={"check_same_thread": False},
    echo=settings.echo_db,
    future=True,
)

print(f"engine {engine}")

AsyncSessionLocal = sessionmaker(bind=engine,
                                 expire_on_commit=False,
                                 autocommit=False,
                                 autoflush=False,
                                 class_=AsyncSession)
current_session = scoped_session(session_factory=AsyncSessionLocal)

convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
metadata.tables.keys()

Base = declarative_base(metadata=metadata)


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())


def get_db():
    return current_session()
