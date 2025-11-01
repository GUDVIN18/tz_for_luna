from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db.database import SessionLocal
from .resources import service
from .resources.schemas import (
    OrganizationOut, 
    OrganizationCreate, 
    SuccessResponse,
)
from typing import List

router = APIRouter(prefix="/organizations", tags=["Organizations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
        "/", 
        name="Создать конкретную организацию",
        response_model=OrganizationOut)
def create_organization(
    data: OrganizationCreate, 
    db: Session = Depends(get_db)
):
    return service.create_organization(db, data)


@router.delete(
        "/{org_id}",
        name="Удалить конкретную организацию",
        response_model=SuccessResponse
    )
def delete_organization(
    org_id: int, 
    db: Session = Depends(get_db)
):
    service.delete_organization(db, org_id)
    return SuccessResponse


@router.get(
        "/building/{building_id}", 
        response_model=List[OrganizationOut], 
        name="список всех организаций находящихся в конкретном здании"
    )
def get_organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    result = service.get_by_building(db, building_id)
    if not result:
        raise HTTPException(status_code=404, detail="Организации в этом здании не найдены")
    return result

@router.get(
        "/activity/by-name/{activity_name}", 
        name="список всех организаций, которые относятся к указанному виду деятельности",
        response_model=List[OrganizationOut]
    )
def get_organizations_by_activity_name(activity_name: str, db: Session = Depends(get_db)):
    return service.get_by_activity_name(db, activity_name)


@router.get(
        "/nearby/rectangle", 
        name="список организаций, которые находятся в заданном прямоугольной области относительно указанной точки на карте",
        response_model=List[OrganizationOut]
    )
def get_organizations_in_rectangle(
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    db: Session = Depends(get_db)
):
    return service.get_by_rectangle(db, lat_min, lat_max, lon_min, lon_max)

@router.get(
        "/{org_id}", 
        name="вывод информации об организации по её идентификатору",
        response_model=OrganizationOut
    )
def get_organization(
    org_id: int, 
    db: Session = Depends(get_db)
):
    org = service.get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get(
        "/search/by-name", 
        name="поиск организации по названию",
    )
def search_organizations_by_name(name: str, db: Session = Depends(get_db)):
    result = service.search_by_name(db, name)
    if not result:
        raise HTTPException(status_code=404, detail="Организации не найдены")
    return result


@router.get(
        "/by-activity/{activity_name}", 
        name="искать организации по виду деятельности. ",
        response_model=list[OrganizationOut]
    )
def get_organizations_by_activity(activity_name: str, db: Session = Depends(get_db)):
    return service.get_organizations_by_activity(db, activity_name)