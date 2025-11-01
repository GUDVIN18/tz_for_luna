from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from .meta import metadata
import uuid


organizations = Table(
    'organizations', 
    metadata,

    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4),

    Column('name', String, nullable=False),
    Column('phones', String, nullable=True),
    Column('building_id', Integer, ForeignKey('buildings.id', ondelete='CASCADE'), nullable=False),
    
    Column('created_at', DateTime, nullable=False, server_default=func.now()),
    Column('updated_at', DateTime, onupdate=func.now())
)