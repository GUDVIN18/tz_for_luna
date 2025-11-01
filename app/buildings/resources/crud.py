from sqlalchemy import select, insert, delete
from sqlalchemy.orm import Session
from core.db.tables import buildings_tabel as buildings
from .schemas import BuildingCreate


class BuildCRUD:
    def __init__(self, db):
        self.db: Session = db
    
    def get_all(self):
        stmt = select(buildings)
        return self.db.execute(stmt).mappings().all()

    def get_by_id(self, building_id: int):
        stmt = select(buildings).where(buildings.c.id == building_id)
        return self.db.execute(stmt).mappings().first()

    def create(self, data: BuildingCreate):
        stmt = insert(buildings).values(
            address=data.address,
            latitude=data.latitude,
            longitude=data.longitude
        ).returning(buildings)
        result = self.db.execute(stmt)
        row = result.mappings().first()
        self.db.commit()
        return row

    def delete_by_id(self, building_id: int):
        stmt = delete(buildings).where(buildings.c.id == building_id)
        self.db.execute(stmt)
        self.db.commit()