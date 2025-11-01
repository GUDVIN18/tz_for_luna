from sqlalchemy.orm import Session
from .crud import BuildCRUD
from .schemas import BuildingCreate


def get_all_buildings(db: Session):
    return BuildCRUD(db).get_all()

def get_building(db: Session, building_id: int):
    return BuildCRUD(db).get_by_id(building_id)

def create_building(db: Session, data: BuildingCreate):
    return BuildCRUD(db).create(data)

def delete_building(db: Session, building_id: int):
    return BuildCRUD(db).delete_by_id(building_id)