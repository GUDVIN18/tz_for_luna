from sqlalchemy import select, insert, delete, func
from sqlalchemy.orm import Session
from core.db.tables import organizations, buildings_tabel, activities_tabel, organization_activities
from .schemas import *


class OrganizationsCRUD:
    def __init__(self, db):
        self.db: Session = db

    def get_by_id(self, org_id: int):
        query = (
            select(
                organizations.c.id,
                organizations.c.uuid,
                organizations.c.name,
                organizations.c.phones,
                organizations.c.building_id,
                buildings_tabel.c.address.label("building_address"),
                buildings_tabel.c.latitude,
                buildings_tabel.c.longitude,
                organizations.c.created_at,
                organizations.c.updated_at,
            )
            .join(buildings_tabel, organizations.c.building_id == buildings_tabel.c.id)
            .where(organizations.c.id == org_id)
        )

        row = self.db.execute(query).mappings().first()
        if not row:
            return None

        data = dict(row)

        data["phones"] = (
            [p.strip() for p in data["phones"].replace(";", ",").split(",")]
            if data["phones"] else []
        )

        acts = self.db.execute(
            select(organization_activities.c.activity_id)
            .where(organization_activities.c.organization_id == data["id"])
        ).fetchall()
        data["activity_ids"] = [r[0] for r in acts]
        return data

    def create(self, data):
        phones_value = ", ".join(data.phones) if isinstance(data.phones, list) else data.phones

        new_org = {
            "uuid": uuid.uuid4(),
            "name": data.name,
            "phones": phones_value,
            "building_id": data.building_id,
        }

        result = self.db.execute(organizations.insert().values(**new_org))
        org_id = result.lastrowid
        if data.activity_ids:
            for act_id in data.activity_ids:
                self.db.execute(
                    organization_activities.insert().values(
                        organization_id=org_id,
                        activity_id=act_id
                    )
                )

        self.db.commit()
        query = (
            select(
                organizations.c.id,
                organizations.c.uuid,
                organizations.c.name,
                organizations.c.phones,
                organizations.c.building_id,
                buildings_tabel.c.address.label("building_address"),
                organizations.c.created_at,
                organizations.c.updated_at
            )
            .join(buildings_tabel, buildings_tabel.c.id == organizations.c.building_id)
            .where(organizations.c.id == org_id)
        )

        row = self.db.execute(query).mappings().first()
        if not row:
            return None
        
        org_data = dict(row)
        org_data["phones"] = (
            [p.strip() for p in org_data["phones"].replace(";", ",").split(",")]
            if org_data["phones"] else []
        )
        acts = self.db.execute(
            select(organization_activities.c.activity_id)
            .where(organization_activities.c.organization_id == org_data["id"])
        ).fetchall()
        org_data["activity_ids"] = [r[0] for r in acts]
        return org_data
    

    def get_by_building(self, building_id: int):
        query = (
            select(
                organizations.c.id,
                organizations.c.uuid,
                organizations.c.name,
                organizations.c.phones,
                organizations.c.building_id,
                buildings_tabel.c.address.label("building_address"),
                organizations.c.created_at,
                organizations.c.updated_at
            )
            .join(buildings_tabel, organizations.c.building_id == buildings_tabel.c.id)
            .where(organizations.c.building_id == building_id)
        )
        rows = self.db.execute(query).mappings().all()
        result = []
        for r in rows:
            data = dict(r)
            data["phones"] = [p.strip() for p in data["phones"].replace(";", ",").split(",")] if data["phones"] else []
            activities_rows = self.db.execute(
                select(organization_activities.c.activity_id)
                .where(organization_activities.c.organization_id == data["id"])
            ).fetchall()
            data["activity_ids"] = [row[0] for row in activities_rows]
            result.append(data)
        return result


    def get_by_activity(self, activity_id: int):
        query = (
            select(
                organizations.c.id,
                organizations.c.uuid,
                organizations.c.name,
                organizations.c.phones,
                organizations.c.building_id,
                buildings_tabel.c.address.label("building_address"),
                activities_tabel.c.name.label("activity_name"),
                organizations.c.created_at,
                organizations.c.updated_at
            )
            .join(organization_activities, organizations.c.id == organization_activities.c.organization_id)
            .join(activities_tabel, activities_tabel.c.id == organization_activities.c.activity_id)
            .join(buildings_tabel, organizations.c.building_id == buildings_tabel.c.id)
            .where(activities_tabel.c.id == activity_id)
        )

        rows = self.db.execute(query).mappings().all()

        result = []
        for row in rows:
            data = dict(row)
            if data["phones"]:
                data["phones"] = [p.strip() for p in data["phones"].replace(";", ",").split(",")]
            else:
                data["phones"] = []
            result.append(data)

        return result

    def get_by_activity_name(self, activity_name: str):
        activity = self.db.execute(
            select(activities_tabel.c.id).where(activities_tabel.c.name == activity_name)
        ).first()

        if not activity:
            return []

        activity_id = activity[0]

        query = (
            select(
                organizations.c.id,
                organizations.c.uuid,
                organizations.c.name,
                organizations.c.phones,
                organizations.c.building_id,
                buildings_tabel.c.address.label("building_address"),
                organizations.c.created_at,
                organizations.c.updated_at,
            )
            .join(organization_activities, organizations.c.id == organization_activities.c.organization_id)
            .join(activities_tabel, organization_activities.c.activity_id == activities_tabel.c.id)
            .join(buildings_tabel, organizations.c.building_id == buildings_tabel.c.id)
            .where(activities_tabel.c.id == activity_id)
        )

        rows = self.db.execute(query).mappings().all()
        result = []
        for row in rows:
            data = dict(row)
            data["phones"] = (
                [p.strip() for p in data["phones"].replace(";", ",").split(",")]
                if data["phones"] else []
            )
            acts = self.db.execute(
                select(organization_activities.c.activity_id)
                .where(organization_activities.c.organization_id == data["id"])
            ).fetchall()
            data["activity_ids"] = [r[0] for r in acts]
            result.append(data)
        return result


    def get_by_rectangle(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float):
        query = (
            select(
                organizations.c.id,
                organizations.c.uuid,
                organizations.c.name,
                organizations.c.phones,
                organizations.c.building_id,
                buildings_tabel.c.address.label("building_address"),
                buildings_tabel.c.latitude,
                buildings_tabel.c.longitude,
                organizations.c.created_at,
                organizations.c.updated_at,
            )
            .join(buildings_tabel, organizations.c.building_id == buildings_tabel.c.id)
            .where(
                buildings_tabel.c.latitude.between(lat_min, lat_max),
                buildings_tabel.c.longitude.between(lon_min, lon_max)
            )
        )

        rows = self.db.execute(query).mappings().all()
        result = []
        for row in rows:
            data = dict(row)
            data["phones"] = [p.strip() for p in data["phones"].replace(";", ",").split(",")] if data["phones"] else []
            result.append(data)
        return result


    def search_by_name(self, name: str):
        print(name)
        query = (
            select(
                organizations.c.id,
                organizations.c.uuid,
                organizations.c.name,
                organizations.c.phones,
                organizations.c.building_id,
                buildings_tabel.c.address.label("building_address"),
                buildings_tabel.c.latitude,
                buildings_tabel.c.longitude,
                organizations.c.created_at,
                organizations.c.updated_at,
            )
            .join(buildings_tabel, organizations.c.building_id == buildings_tabel.c.id)
            .where(organizations.c.name == name)
        )

        rows = self.db.execute(query).mappings().all()

        result = []
        for row in rows:
            data = dict(row)
            data["phones"] = (
                [p.strip() for p in data["phones"].replace(";", ",").split(",")]
                if data["phones"] else []
            )

            acts = self.db.execute(
                select(organization_activities.c.activity_id)
                .where(organization_activities.c.organization_id == data["id"])
            ).fetchall()
            data["activity_ids"] = [r[0] for r in acts]
            result.append(data)

        return result


    def get_organizations_by_activity(self, activity_name: str):
        parent_id = self.db.execute(
            select(activities_tabel.c.id).where(activities_tabel.c.name == activity_name)
        ).scalar_one_or_none()

        if not parent_id:
            return []

        child_ids = self.db.execute(
            select(activities_tabel.c.id).where(activities_tabel.c.parent_id == parent_id)
        ).scalars().all()

        all_ids = [parent_id] + child_ids
        query = (
            select(
                organizations.c.id,
                organizations.c.uuid,
                organizations.c.name,
                organizations.c.phones,
                organizations.c.building_id,
                buildings_tabel.c.address.label("building_address"),
                organizations.c.created_at,
                organizations.c.updated_at
            )
            .join(organization_activities, organization_activities.c.organization_id == organizations.c.id)
            .join(activities_tabel, activities_tabel.c.id == organization_activities.c.activity_id)
            .join(buildings_tabel, buildings_tabel.c.id == organizations.c.building_id)
            .where(organization_activities.c.activity_id.in_(all_ids))
            .distinct()
        )

        rows = self.db.execute(query).mappings().all()
        result = []

        for row in rows:
            data = dict(row)
            data["phones"] = (
                [p.strip() for p in data["phones"].replace(";", ",").split(",")]
                if data["phones"] else []
            )
            acts = self.db.execute(
                select(organization_activities.c.activity_id)
                .where(organization_activities.c.organization_id == data["id"])
            ).fetchall()
            data["activity_ids"] = [r[0] for r in acts]
            result.append(data)

        return result


    def delete_by_id(self, org_id: int):
        stmt = delete(organizations).where(
            organizations.c.id == org_id
        )
        self.db.execute(stmt)
        self.db.commit()