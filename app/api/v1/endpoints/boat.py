from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from schemas.boat import Boat, BoatRead
from db.database import get_session


router = APIRouter(prefix='/boat')


@router.get('')
async def get_boat(
    session: Session = Depends(get_session)
) -> BoatRead:
    return session.get(Boat, 1)


@router.patch('')
async def update_boat(
    session: Session = Depends(get_session)
) -> BoatRead:
    pass
