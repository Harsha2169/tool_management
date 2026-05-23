from sqlalchemy.orm import Session
from app.models.tool_production import ToolProduction
from app.schemas.tool_production import ToolProductionCreate, ToolProductionUpdate


def get_productions(db: Session, tool_master_id: int):
    return db.query(ToolProduction).filter(ToolProduction.tool_master_id == tool_master_id).all()


def get_production(db: Session, production_id: int):
    return db.query(ToolProduction).filter(ToolProduction.id == production_id).first()


def create_production(db: Session, tool_master_id: int, data: ToolProductionCreate):
    db_obj = ToolProduction(tool_master_id=tool_master_id, **data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_production(db: Session, production_id: int, data: ToolProductionUpdate):
    db_obj = get_production(db, production_id)
    if not db_obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_production(db: Session, production_id: int):
    db_obj = get_production(db, production_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return True
