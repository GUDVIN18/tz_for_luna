from sqlalchemy import select, insert, delete
from sqlalchemy.orm import Session
from core.db.tables import activities_tabel as activities
from .schemas import ActivityCreate
from sqlalchemy.exc import IntegrityError


class ActivitiesCRUD:
    def __init__(self, db):
        self.db: Session = db

    def get_all(self):
        stmt = select(activities)
        return self.db.execute(stmt).mappings().all()

    def get_by_id(self, activity_id: int):
        stmt = select(activities).where(activities.c.id == activity_id)
        return self.db.execute(stmt).mappings().first()

    def _get_depth(self, activity_id: int, depth: int = 1) -> int:
        query = select(activities.c.parent_id).where(activities.c.id == activity_id)
        parent = self.db.execute(query).fetchone()
        if parent and parent.parent_id:
            return self._get_depth(parent.parent_id, depth + 1)
        return depth

    def create(self, data: ActivityCreate):
        parent_id = data.parent_id
        if data.parent_name and not parent_id:
            query = select(activities.c.id).where(activities.c.name == data.parent_name)
            parent = self.db.execute(query).fetchone()
            if not parent:
                raise ValueError(f"Родительская категория '{data.parent_name}' не найдена")
            parent_id = parent.id

        # проверим на уровень
        if parent_id:
            depth = self._get_depth(parent_id)
            if depth >= 3:
                raise ValueError("Нельзя создавать уровень глубже 3")

        insert_stmt = activities.insert().values(
            name=data.name,
            parent_id=parent_id,
        ).returning(activities)
        result = self.db.execute(insert_stmt)
        row = result.mappings().first()
        self.db.commit()
        return row

    def delete_by_id(self, activity_id: int):
        stmt = delete(activities).where(activities.c.id == activity_id)
        self.db.execute(stmt)
        self.db.commit()