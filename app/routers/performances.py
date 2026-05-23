from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import tool_master as tool_crud
from app.crud import tool_performance as crud
from app.schemas.tool_performance import (
    ToolPerformanceCreate, ToolPerformanceUpdate, ToolPerformanceResponse
)

router = APIRouter(prefix="/api/v1/tools/{tool_id}/performances", tags=["Performances"])


def _get_tool_pk(tool_id: str, db: Session):
    tool = tool_crud.get_tool_by_id(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool.id


@router.get("", response_model=list[ToolPerformanceResponse])
def list_performances(tool_id: str, db: Session = Depends(get_db)):
    pk = _get_tool_pk(tool_id, db)
    return crud.get_performances(db, pk)


@router.post("", response_model=ToolPerformanceResponse, status_code=201)
def create_performance(tool_id: str, data: ToolPerformanceCreate, db: Session = Depends(get_db)):
    pk = _get_tool_pk(tool_id, db)
    return crud.create_performance(db, pk, data)


@router.put("/{performance_id}", response_model=ToolPerformanceResponse)
def update_performance(tool_id: str, performance_id: int, data: ToolPerformanceUpdate, db: Session = Depends(get_db)):
    _get_tool_pk(tool_id, db)
    result = crud.update_performance(db, performance_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Performance record not found")
    return result


@router.delete("/{performance_id}")
def delete_performance(tool_id: str, performance_id: int, db: Session = Depends(get_db)):
    _get_tool_pk(tool_id, db)
    result = crud.delete_performance(db, performance_id)
    if not result:
        raise HTTPException(status_code=404, detail="Performance record not found")
    return {"message": "Deleted successfully"}
