from sqlalchemy import (
    Column, BigInteger, String, Date, Text, Numeric, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ToolMaintenance(Base):
    __tablename__ = "tool_maintenance"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tool_master_id = Column(BigInteger, ForeignKey("tool_master.id"), nullable=False)
    maintenance_date = Column(Date, nullable=False)
    maintenance_type = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    performed_by = Column(String(100), nullable=True)
    next_due_date = Column(Date, nullable=True)
    cost = Column(Numeric(12, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    tool_master = relationship("ToolMaster", back_populates="maintenances")
