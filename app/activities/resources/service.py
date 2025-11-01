from sqlalchemy.orm import Session
from .crud import ActivitiesCRUD
from .schemas import ActivityCreate


def get_all_activities(db: Session):
    return ActivitiesCRUD(db).get_all()

def get_activity(db: Session, activity_id: int):
    return ActivitiesCRUD(db).get_by_id(activity_id)

def create_activity(db: Session, data: ActivityCreate):
    return ActivitiesCRUD(db).create(data)

def delete_activity(db: Session, activity_id: int):
    return ActivitiesCRUD(db).delete_by_id(activity_id)