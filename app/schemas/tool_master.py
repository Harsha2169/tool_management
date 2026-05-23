from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ToolMasterBase(BaseModel):
    tool_id: str
    tool_description: str
    tool_type_id: int
    life_status: str = "Active"
    make: Optional[str] = None
    model: Optional[str] = None
    asset_owner: str
    acquired_date: Optional[date] = None
    lifecycle_limit: int
    control_unit: str
    lifecycle_initial_value: int = 0
    current_usage: int = 0
    plant_id: Optional[str] = None


class ToolMasterCreate(ToolMasterBase):
    pass


class ToolMasterUpdate(BaseModel):
    tool_description: Optional[str] = None
    tool_type_id: Optional[int] = None
    life_status: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    asset_owner: Optional[str] = None
    acquired_date: Optional[date] = None
    lifecycle_limit: Optional[int] = None
    control_unit: Optional[str] = None
    lifecycle_initial_value: Optional[int] = None
    current_usage: Optional[int] = None
    plant_id: Optional[str] = None


class ToolMasterResponse(ToolMasterBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    tool_type_name: Optional[str] = None
    usage_percentage: Optional[float] = None

    class Config:
        from_attributes = True


class ToolMasterListResponse(BaseModel):
    total: int
    items: list[ToolMasterResponse]
