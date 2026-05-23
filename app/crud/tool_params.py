from sqlalchemy.orm import Session
from app.models.tool_params import ToolParams
from app.schemas.tool_params import ToolParamsCreate, ToolParamsUpdate


def get_params(db: Session, tool_master_id: int):
    return db.query(ToolParams).filter(ToolParams.tool_master_id == tool_master_id).all()


def get_param(db: Session, param_id: int):
    return db.query(ToolParams).filter(ToolParams.id == param_id).first()


def create_param(db: Session, tool_master_id: int, data: ToolParamsCreate):
    db_obj = ToolParams(tool_master_id=tool_master_id, **data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_param(db: Session, param_id: int, data: ToolParamsUpdate):
    db_obj = get_param(db, param_id)
    if not db_obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_param(db: Session, param_id: int):
    db_obj = get_param(db, param_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return True
