from sqlalchemy import (
    Column, BigInteger, String, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ToolParams(Base):
    __tablename__ = "tool_params"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tool_master_id = Column(BigInteger, ForeignKey("tool_master.id"), nullable=False)
    parameter_name = Column(String(100), nullable=False)
    parameter_value = Column(String(100), nullable=False)
    uom = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    tool_master = relationship("ToolMaster", back_populates="params")
