from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ToolProductionBase(BaseModel):
    tool_part_code: str
    cavities: int
    cavity_numbers: Optional[str] = None
    weight_all_parts_g: Optional[float] = None
    weight_runner_g: Optional[float] = None
    weight_shot_g: Optional[float] = None


class ToolProductionCreate(ToolProductionBase):
    pass


class ToolProductionUpdate(BaseModel):
    tool_part_code: Optional[str] = None
    cavities: Optional[int] = None
    cavity_numbers: Optional[str] = None
    weight_all_parts_g: Optional[float] = None
    weight_runner_g: Optional[float] = None
    weight_shot_g: Optional[float] = None


class ToolProductionResponse(ToolProductionBase):
    id: int
    tool_master_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
