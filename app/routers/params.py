from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import tool_master as tool_crud
from app.crud import tool_params as crud
from app.schemas.tool_params import (
    ToolParamsCreate, ToolParamsUpdate, ToolParamsResponse
)

router = APIRouter(prefix="/api/v1/tools/{tool_id}/params", tags=["Params"])


def _get_tool_pk(tool_id: str, db: Session):
    tool = tool_crud.get_tool_by_id(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool.id


@router.get("", response_model=list[ToolParamsResponse])
def list_params(tool_id: str, db: Session = Depends(get_db)):
    pk = _get_tool_pk(tool_id, db)
    return crud.get_params(db, pk)


@router.post("", response_model=ToolParamsResponse, status_code=201)
def create_param(tool_id: str, data: ToolParamsCreate, db: Session = Depends(get_db)):
    pk = _get_tool_pk(tool_id, db)
    return crud.create_param(db, pk, data)


@router.put("/{param_id}", response_model=ToolParamsResponse)
def update_param(tool_id: str, param_id: int, data: ToolParamsUpdate, db: Session = Depends(get_db)):
    _get_tool_pk(tool_id, db)
    result = crud.update_param(db, param_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return result


@router.delete("/{param_id}")
def delete_param(tool_id: str, param_id: int, db: Session = Depends(get_db)):
    _get_tool_pk(tool_id, db)
    result = crud.delete_param(db, param_id)
    if not result:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return {"message": "Deleted successfully"}
