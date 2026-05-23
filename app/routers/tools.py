from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.crud import tool_master as crud
from app.schemas.tool_master import (
    ToolMasterCreate, ToolMasterUpdate, ToolMasterResponse, ToolMasterListResponse
)

router = APIRouter(prefix="/api/v1/tools", tags=["Tools"])


@router.get("", response_model=ToolMasterListResponse)
def list_tools(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    tool_type: Optional[str] = None,
    life_status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    total, items = crud.get_tools(db, skip, limit, tool_type, life_status, search)
    response_items = []
    for tool in items:
        tool_dict = ToolMasterResponse.model_validate(tool)
        tool_dict.tool_type_name = tool.tool_type_rel.type_name if tool.tool_type_rel else None
        tool_dict.usage_percentage = (
            round((tool.current_usage / tool.lifecycle_limit) * 100, 2)
            if tool.lifecycle_limit > 0 else 0
        )
        response_items.append(tool_dict)
    return ToolMasterListResponse(total=total, items=response_items)


@router.get("/{tool_id}", response_model=ToolMasterResponse)
def get_tool(tool_id: str, db: Session = Depends(get_db)):
    tool = crud.get_tool_by_id(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    resp = ToolMasterResponse.model_validate(tool)
    resp.tool_type_name = tool.tool_type_rel.type_name if tool.tool_type_rel else None
    resp.usage_percentage = (
        round((tool.current_usage / tool.lifecycle_limit) * 100, 2)
        if tool.lifecycle_limit > 0 else 0
    )
    return resp


@router.post("", response_model=ToolMasterResponse, status_code=201)
def create_tool(tool: ToolMasterCreate, db: Session = Depends(get_db)):
    existing = crud.get_tool_by_id(db, tool.tool_id)
    if existing:
        raise HTTPException(status_code=400, detail="Tool ID already exists")
    return crud.create_tool(db, tool)


@router.put("/{tool_id}", response_model=ToolMasterResponse)
def update_tool(tool_id: str, tool_update: ToolMasterUpdate, db: Session = Depends(get_db)):
    tool = crud.update_tool(db, tool_id, tool_update)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


@router.delete("/{tool_id}")
def delete_tool(tool_id: str, db: Session = Depends(get_db)):
    tool = crud.delete_tool(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"message": "Tool deleted successfully"}
