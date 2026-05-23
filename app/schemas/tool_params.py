from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ToolParamsBase(BaseModel):
    parameter_name: str
    parameter_value: str
    uom: Optional[str] = None


class ToolParamsCreate(ToolParamsBase):
    pass


class ToolParamsUpdate(BaseModel):
    parameter_name: Optional[str] = None
    parameter_value: Optional[str] = None
    uom: Optional[str] = None


class ToolParamsResponse(ToolParamsBase):
    id: int
    tool_master_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
