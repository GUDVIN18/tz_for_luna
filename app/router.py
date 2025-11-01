from fastapi import APIRouter
from .organizations.router import router as org_router
from .buildings.router import router as building_router
from .activities.router import router as activites_router

router = APIRouter()


router.include_router(org_router)
router.include_router(building_router)
router.include_router(activites_router)