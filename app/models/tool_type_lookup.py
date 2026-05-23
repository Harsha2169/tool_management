from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class ToolTypeLookup(Base):
    __tablename__ = "tool_type_lookup"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type_name = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship
    tools = relationship("ToolMaster", back_populates="tool_type_rel")
