from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional

from app.models.tool_master import ToolMaster
from app.models.tool_type_lookup import ToolTypeLookup
from app.schemas.tool_master import ToolMasterCreate, ToolMasterUpdate


def get_tools(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    tool_type: Optional[str] = None,
    life_status: Optional[str] = None,
    search: Optional[str] = None,
):
    query = db.query(ToolMaster).filter(ToolMaster.is_deleted == False)  # noqa: E712

    if tool_type:
        query = query.join(ToolTypeLookup).filter(ToolTypeLookup.type_name == tool_type)
    if life_status:
        query = query.filter(ToolMaster.life_status == life_status)
    if search:
        query = query.filter(
            ToolMaster.tool_id.ilike(f"%{search}%")
            | ToolMaster.tool_description.ilike(f"%{search}%")
        )

    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return total, items


def get_tool_by_id(db: Session, tool_id: str):
    return db.query(ToolMaster).filter(
        and_(ToolMaster.tool_id == tool_id, ToolMaster.is_deleted == False)  # noqa: E712
    ).first()


def get_tool_by_pk(db: Session, pk: int):
    return db.query(ToolMaster).filter(
        and_(ToolMaster.id == pk, ToolMaster.is_deleted == False)  # noqa: E712
    ).first()


def create_tool(db: Session, tool: ToolMasterCreate):
    db_tool = ToolMaster(**tool.model_dump())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool


def update_tool(db: Session, tool_id: str, tool_update: ToolMasterUpdate):
    db_tool = get_tool_by_id(db, tool_id)
    if not db_tool:
        return None
    update_data = tool_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tool, field, value)
    db.commit()
    db.refresh(db_tool)
    return db_tool


def delete_tool(db: Session, tool_id: str):
    db_tool = get_tool_by_id(db, tool_id)
    if not db_tool:
        return None
    db_tool.is_deleted = True
    db.commit()
    return db_tool
