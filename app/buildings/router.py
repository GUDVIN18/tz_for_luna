from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db.database import SessionLocal
from .resources import service
from .resources.schemas import BuildingOut, BuildingCreate, SuccessResponse


router = APIRouter(prefix="/buildings", tags=["Buildings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
        "/", 
        name="Список всех зданий",
        response_model=list[BuildingOut]
    )
def list_buildings(db: Session = Depends(get_db)):
    return service.get_all_buildings(db)

@router.get(
        "/{building_id}", 
        name="Получить здание по ID",
        response_model=BuildingOut
    )
def get_building(
    building_id: int, 
    db: Session = Depends(get_db)
):
    building = service.get_building(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.post(
        "/", 
        name="Создать здание",
        response_model=BuildingOut
        )
def create_building(
    data: BuildingCreate, 
    db: Session = Depends(get_db)
):
    return service.create_building(db, data)

@router.delete(
        "/{building_id}",
         name="Удалить здание",
         response_model=SuccessResponse
    )
def delete_building(
    building_id: int, 
    db: Session = Depends(get_db)
):
    service.delete_building(db, building_id)
    return SuccessResponse