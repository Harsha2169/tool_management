from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tool_type_lookup import ToolTypeLookup

router = APIRouter(prefix="/api/v1/lookups", tags=["Lookups"])


@router.get("/tool-types")
def get_tool_types(db: Session = Depends(get_db)):
    types = db.query(ToolTypeLookup).filter(ToolTypeLookup.is_active == True).all()  # noqa: E712
    return [{"id": t.id, "name": t.type_name} for t in types]


@router.get("/control-units")
def get_control_units():
    return [{"value": "Shots"}, {"value": "Microns"}]


@router.get("/asset-owners")
def get_asset_owners():
    return [{"value": "Client"}, {"value": "Inhouse"}, {"value": "3rd Party"}]


@router.get("/life-statuses")
def get_life_statuses():
    return [{"value": "Active"}, {"value": "Inactive"}]
