from sqlalchemy import (
    Column, BigInteger, String, Date, Numeric, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ToolPerformance(Base):
    __tablename__ = "tool_performance"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tool_master_id = Column(BigInteger, ForeignKey("tool_master.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    performance_value = Column(Numeric(12, 2), nullable=True)
    cumulative = Column(Numeric(12, 2), nullable=True)
    uom = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    tool_master = relationship("ToolMaster", back_populates="performances")
