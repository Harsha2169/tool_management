from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import tool_master as tool_crud
from app.crud import tool_maintenance as crud
from app.schemas.tool_maintenance import (
    ToolMaintenanceCreate, ToolMaintenanceUpdate, ToolMaintenanceResponse
)

router = APIRouter(prefix="/api/v1/tools/{tool_id}/maintenances", tags=["Maintenances"])


def _get_tool_pk(tool_id: str, db: Session):
    tool = tool_crud.get_tool_by_id(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool.id


@router.get("", response_model=list[ToolMaintenanceResponse])
def list_maintenances(tool_id: str, db: Session = Depends(get_db)):
    pk = _get_tool_pk(tool_id, db)
    return crud.get_maintenances(db, pk)


@router.post("", response_model=ToolMaintenanceResponse, status_code=201)
def create_maintenance(tool_id: str, data: ToolMaintenanceCreate, db: Session = Depends(get_db)):
    pk = _get_tool_pk(tool_id, db)
    return crud.create_maintenance(db, pk, data)


@router.put("/{maintenance_id}", response_model=ToolMaintenanceResponse)
def update_maintenance(tool_id: str, maintenance_id: int, data: ToolMaintenanceUpdate, db: Session = Depends(get_db)):
    _get_tool_pk(tool_id, db)
    result = crud.update_maintenance(db, maintenance_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return result


@router.delete("/{maintenance_id}")
def delete_maintenance(tool_id: str, maintenance_id: int, db: Session = Depends(get_db)):
    _get_tool_pk(tool_id, db)
    result = crud.delete_maintenance(db, maintenance_id)
    if not result:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return {"message": "Deleted successfully"}
