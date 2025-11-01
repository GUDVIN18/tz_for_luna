from sqlalchemy.orm import Session
from .crud import OrganizationsCRUD
from .schemas import OrganizationCreate


def get_organization(db: Session, org_id: int):
    return OrganizationsCRUD(db).get_by_id(org_id)

def create_organization(db: Session, data: OrganizationCreate):
    return OrganizationsCRUD(db).create(data)

def delete_organization(db: Session, org_id: int):
    return OrganizationsCRUD(db).delete_by_id(org_id)

def get_by_building(db: Session, building_id):
    return OrganizationsCRUD(db).get_by_building(building_id)

def get_by_activity_name(db, name: str):
    return OrganizationsCRUD(db).get_by_activity_name(name)

def get_by_rectangle(db, lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    return OrganizationsCRUD(db).get_by_rectangle(lat_min, lat_max, lon_min, lon_max)

def search_by_name(db, name: str):
    return OrganizationsCRUD(db).search_by_name(name)

def get_organizations_by_activity(db, activity_name: str):
    return OrganizationsCRUD(db).get_organizations_by_activity(activity_name)