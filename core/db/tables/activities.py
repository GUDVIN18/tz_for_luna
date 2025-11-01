from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from .meta import metadata
import uuid


activities_tabel = Table(
    'activities',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4),

    Column('name', String, nullable=False), # Еда и тд
    Column('parent_id', Integer, ForeignKey('activities.id'), nullable=True),  # для вложенности

    Column('created_at', DateTime, nullable=False, server_default=func.now()),
    Column('updated_at', DateTime, onupdate=func.now())
)


organization_activities = Table(
    'organization_activities',
    metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id', ondelete="CASCADE")),
    Column('activity_id', Integer, ForeignKey('activities.id', ondelete="CASCADE"))
)