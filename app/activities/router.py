from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db.database import SessionLocal
from .resources import service
from .resources.schemas import ActivityOut, ActivityCreate, SuccessResponse

router = APIRouter(prefix="/activities", tags=["Activities"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    name="Получить все виды деятельности",
    response_model=list[ActivityOut]
)
def list_activities(db: Session = Depends(get_db)):
    return service.get_all_activities(db)


@router.get(
    "/{activity_id}",
    name="Получить вид деятельности по ID",
    response_model=ActivityOut
)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = service.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post(
    "/",
    name="Создать новый вид деятельности",
    response_model=ActivityOut
)
def create_activity(
    data: ActivityCreate, 
    db: Session = Depends(get_db)
):
    return service.create_activity(db, data)


@router.delete(
    "/{activity_id}",
    name="Удалить вид деятельности по ID",
    response_model=SuccessResponse
)
def delete_activity(
    activity_id: int, 
    db: Session = Depends(get_db)
):
    service.delete_activity(db, activity_id)
    return SuccessResponse