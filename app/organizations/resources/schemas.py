from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import datetime as dt


class OrganizationBase(BaseModel):
    name: str
    phones: Optional[List[str]] = None
    building_id: int
    activity_ids: Optional[List[int]] = Field(default=None, example=[1, 2])

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationOut(OrganizationBase):
    id: int
    uuid: uuid.UUID
    phones: List[str]
    building_address: Optional[str] = None
    created_at: Optional[dt.datetime]
    updated_at: Optional[dt.datetime]


class SuccessResponse(BaseModel):
    status: int = 200
    message: str = "Запрос выполнен успешно"