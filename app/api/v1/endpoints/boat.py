from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from schemas.boat import Boat, BoatRead, BoatUpdate
from db.database import get_session


BOAT_ID = 1

router = APIRouter(prefix='/boat')


@router.get('')
async def get_boat(
    session: Session = Depends(get_session)
) -> BoatRead:
    return session.get(Boat, BOAT_ID)


@router.patch('')
async def update_boat(
    boat_update: BoatUpdate,
    session: Session = Depends(get_session)
) -> BoatRead:
    boat = session.get(Boat, BOAT_ID)
    if not boat:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 'Лодка не найдена')
    dump = boat_update.model_dump(exclude_unset=True)
    boat.sqlmodel_update(dump)
    session.add(boat)
    session.commit()
    session.refresh(boat)
    return boat
