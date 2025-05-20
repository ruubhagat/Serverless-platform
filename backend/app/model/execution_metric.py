from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base  # Adjust import if needed

class ExecutionMetric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    function_id = Column(Integer)
    runtime = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float)
    exit_code = Column(Integer)
    error_message = Column(String, nullable=True)
    stdout = Column(String)
    stderr = Column(String)
