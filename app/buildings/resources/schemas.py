import uuid
from pydantic import BaseModel, Field
from typing import Optional
import datetime as dt


class BuildingBase(BaseModel):
    address: str = Field(..., example="г. Москва, ул. Ленина 1, офис 3")
    latitude: float = Field(..., example=55.7558)
    longitude: float = Field(..., example=37.6173)

class BuildingCreate(BuildingBase):
    pass

class BuildingOut(BuildingBase):
    id: int
    uuid: uuid.UUID
    created_at: Optional[dt.datetime] = None
    updated_at: Optional[dt.datetime] = None

class SuccessResponse(BaseModel):
    status: int = 200
    message: str = "Запрос выполнен успешно"