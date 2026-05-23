from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import tool_master as tool_crud
from app.crud import tool_production as crud
from app.schemas.tool_production import (
    ToolProductionCreate, ToolProductionUpdate, ToolProductionResponse
)

router = APIRouter(prefix="/api/v1/tools/{tool_id}/productions", tags=["Productions"])


def _get_tool_pk(tool_id: str, db: Session):
    tool = tool_crud.get_tool_by_id(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool.id


@router.get("", response_model=list[ToolProductionResponse])
def list_productions(tool_id: str, db: Session = Depends(get_db)):
    pk = _get_tool_pk(tool_id, db)
    return crud.get_productions(db, pk)


@router.post("", response_model=ToolProductionResponse, status_code=201)
def create_production(tool_id: str, data: ToolProductionCreate, db: Session = Depends(get_db)):
    pk = _get_tool_pk(tool_id, db)
    return crud.create_production(db, pk, data)


@router.put("/{production_id}", response_model=ToolProductionResponse)
def update_production(tool_id: str, production_id: int, data: ToolProductionUpdate, db: Session = Depends(get_db)):
    _get_tool_pk(tool_id, db)
    result = crud.update_production(db, production_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Production entry not found")
    return result


@router.delete("/{production_id}")
def delete_production(tool_id: str, production_id: int, db: Session = Depends(get_db)):
    _get_tool_pk(tool_id, db)
    result = crud.delete_production(db, production_id)
    if not result:
        raise HTTPException(status_code=404, detail="Production entry not found")
    return {"message": "Deleted successfully"}
