from sqlalchemy import (
    Column, BigInteger, Integer, String, Numeric, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ToolProduction(Base):
    __tablename__ = "tool_production"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tool_master_id = Column(BigInteger, ForeignKey("tool_master.id"), nullable=False)
    tool_part_code = Column(String(50), nullable=False)
    cavities = Column(Integer, nullable=False)
    cavity_numbers = Column(String(50), nullable=True)
    weight_all_parts_g = Column(Numeric(10, 2), nullable=True)
    weight_runner_g = Column(Numeric(10, 2), nullable=True)
    weight_shot_g = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    tool_master = relationship("ToolMaster", back_populates="productions")
