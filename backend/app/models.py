# backend/app/models.py

from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    route = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=False)
    timeout = Column(Float, default=5.0)
