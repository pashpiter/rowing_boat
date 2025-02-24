from fastapi import APIRouter

from api.v1.endpoints.boat import router as boat_router


router = APIRouter(prefix='/api/v1')

router.include_router(boat_router, tags=['Лодка'])
