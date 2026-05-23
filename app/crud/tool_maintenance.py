from sqlalchemy.orm import Session
from app.models.tool_maintenance import ToolMaintenance
from app.schemas.tool_maintenance import ToolMaintenanceCreate, ToolMaintenanceUpdate


def get_maintenances(db: Session, tool_master_id: int):
    return db.query(ToolMaintenance).filter(ToolMaintenance.tool_master_id == tool_master_id).all()


def get_maintenance(db: Session, maintenance_id: int):
    return db.query(ToolMaintenance).filter(ToolMaintenance.id == maintenance_id).first()


def create_maintenance(db: Session, tool_master_id: int, data: ToolMaintenanceCreate):
    db_obj = ToolMaintenance(tool_master_id=tool_master_id, **data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_maintenance(db: Session, maintenance_id: int, data: ToolMaintenanceUpdate):
    db_obj = get_maintenance(db, maintenance_id)
    if not db_obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_maintenance(db: Session, maintenance_id: int):
    db_obj = get_maintenance(db, maintenance_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return True
