from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ToolMaintenanceBase(BaseModel):
    maintenance_date: date
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    performed_by: Optional[str] = None
    next_due_date: Optional[date] = None
    cost: Optional[float] = None


class ToolMaintenanceCreate(ToolMaintenanceBase):
    pass


class ToolMaintenanceUpdate(BaseModel):
    maintenance_date: Optional[date] = None
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    performed_by: Optional[str] = None
    next_due_date: Optional[date] = None
    cost: Optional[float] = None


class ToolMaintenanceResponse(ToolMaintenanceBase):
    id: int
    tool_master_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
