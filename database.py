from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

PG_DSN = 'postgresql://postgres:2146@localhost:5432/postgres'

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    owner = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now())


Base.metadata.create_all(engine)
