from sqlalchemy import (
    Column, BigInteger, String, Date, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ToolMaster(Base):
    __tablename__ = "tool_master"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tool_id = Column(String(50), unique=True, nullable=False, index=True)
    tool_description = Column(String(255), nullable=False)
    tool_type_id = Column(BigInteger, ForeignKey("tool_type_lookup.id"), nullable=False)
    life_status = Column(String(20), nullable=False, default="Active")
    make = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    asset_owner = Column(String(50), nullable=False)
    acquired_date = Column(Date, nullable=True)
    lifecycle_limit = Column(BigInteger, nullable=False)
    control_unit = Column(String(50), nullable=False)
    lifecycle_initial_value = Column(BigInteger, default=0)
    current_usage = Column(BigInteger, default=0)
    plant_id = Column(String(50), nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    tool_type_rel = relationship("ToolTypeLookup", back_populates="tools")
    productions = relationship("ToolProduction", back_populates="tool_master", cascade="all, delete-orphan")
    performances = relationship("ToolPerformance", back_populates="tool_master", cascade="all, delete-orphan")
    params = relationship("ToolParams", back_populates="tool_master", cascade="all, delete-orphan")
    maintenances = relationship("ToolMaintenance", back_populates="tool_master", cascade="all, delete-orphan")
