from fastapi import APIRouter

from .setup.setup import create_application

from .routers import (
    user_api,
    auth_api,
    geojson_api
)

router = APIRouter(prefix="/api")

router.include_router(user_api.router)
router.include_router(auth_api.router)
router.include_router(geojson_api.router)

app = create_application(router=router)