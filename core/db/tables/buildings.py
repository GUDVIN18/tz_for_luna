from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from .meta import metadata
import uuid


buildings_tabel = Table(
    'buildings',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4),

    Column('address', String, nullable=False),
    Column('latitude', Float, nullable=False), # широта
    Column('longitude', Float, nullable=False), # долгота

    Column('created_at', DateTime, nullable=False, server_default=func.now()),
    Column('updated_at', DateTime, onupdate=func.now())
)