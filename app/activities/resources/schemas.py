import uuid
import datetime as dt
from pydantic import BaseModel, Field
from typing import Optional, List


class ActivityBase(BaseModel):
    name: str = Field(..., example="Молочная продукция")
    parent_id: Optional[int] = Field(None, example=1)
    parent_name: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityOut(ActivityBase):
    id: int
    uuid: uuid.UUID
    created_at: Optional[dt.datetime] = None
    updated_at: Optional[dt.datetime] = None

class SuccessResponse(BaseModel):
    status: int = 200
    message: str = "Запрос выполнен успешно"