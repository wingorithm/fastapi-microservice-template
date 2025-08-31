import fastapi

from app.api.routes.ServiceRoutes import router as service_router

router = fastapi.APIRouter()

router.include_router(service_router)
# add other router if needed