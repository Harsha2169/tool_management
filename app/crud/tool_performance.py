from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.tool_performance import ToolPerformance
from app.models.tool_master import ToolMaster
from app.schemas.tool_performance import ToolPerformanceCreate, ToolPerformanceUpdate


def get_performances(db: Session, tool_master_id: int):
    return db.query(ToolPerformance).filter(ToolPerformance.tool_master_id == tool_master_id).all()


def get_performance(db: Session, performance_id: int):
    return db.query(ToolPerformance).filter(ToolPerformance.id == performance_id).first()


def _update_tool_usage(db: Session, tool_master_id: int):
    """Recalculate current_usage from the latest cumulative performance value."""
    latest = (
        db.query(ToolPerformance)
        .filter(ToolPerformance.tool_master_id == tool_master_id)
        .order_by(ToolPerformance.start_date.desc(), ToolPerformance.id.desc())
        .first()
    )
    tool = db.query(ToolMaster).filter(ToolMaster.id == tool_master_id).first()
    if tool:
        tool.current_usage = int(latest.cumulative) if latest and latest.cumulative else 0
        db.commit()


def create_performance(db: Session, tool_master_id: int, data: ToolPerformanceCreate):
    db_obj = ToolPerformance(tool_master_id=tool_master_id, **data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    _update_tool_usage(db, tool_master_id)
    return db_obj


def update_performance(db: Session, performance_id: int, data: ToolPerformanceUpdate):
    db_obj = get_performance(db, performance_id)
    if not db_obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    _update_tool_usage(db, db_obj.tool_master_id)
    return db_obj


def delete_performance(db: Session, performance_id: int):
    db_obj = get_performance(db, performance_id)
    if not db_obj:
        return None
    tool_master_id = db_obj.tool_master_id
    db.delete(db_obj)
    db.commit()
    _update_tool_usage(db, tool_master_id)
    return True
