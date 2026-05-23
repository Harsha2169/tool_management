from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ToolPerformanceBase(BaseModel):
    start_date: date
    end_date: Optional[date] = None
    performance_value: Optional[float] = None
    cumulative: Optional[float] = None
    uom: str


class ToolPerformanceCreate(ToolPerformanceBase):
    pass


class ToolPerformanceUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    performance_value: Optional[float] = None
    cumulative: Optional[float] = None
    uom: Optional[str] = None


class ToolPerformanceResponse(ToolPerformanceBase):
    id: int
    tool_master_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
