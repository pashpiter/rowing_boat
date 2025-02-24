from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.engine import Result
from sqlmodel import Session, select

from db.database import get_session
from schemas.boat import Boat, BoatDirection, BoatRead
from schemas.passengers import Passenger


BOAT_ID: int = 1

router = APIRouter(prefix='/boat')


@router.get('')
async def get_boat(
    session: Session = Depends(get_session)
) -> BoatRead:
    '''Возвращает лодку с параметрами'''
    return session.get(Boat, BOAT_ID)


@router.patch('')
async def update_boat(
    session: Session = Depends(get_session),
    name: Annotated[str, Query(max_length=20, min_length=1)] = None,
    seats: Annotated[int, Query(le=6, ge=1)] = None,
    speed: Annotated[float, Query(le=4, ge=0)] = None,
    direction: BoatDirection = None
) -> BoatRead:
    '''Изменение полей лодки'''
    boat = session.get(Boat, BOAT_ID)
    if not boat:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 'Лодка не найдена')
    result = {}
    if name:
        result['name'] = name
    if seats:
        if seats < len(boat.passengers):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Уберите пассажиров перед тем как уменьшить количество мест'
            )
        result['seats'] = seats
    if speed:
        result['speed'] = speed
    if direction:
        result['direction'] = direction
    boat.sqlmodel_update(result)
    session.add(boat)
    session.commit()
    session.refresh(boat)
    return boat


@router.patch('/add_passenger')
async def add_passenger(
    name: str,
    session: Session = Depends(get_session)
) -> BoatRead:
    '''Добавление пассажиров в лодку'''
    boat = session.get(Boat, BOAT_ID)
    stmt = select(Passenger).where(Passenger.name == name)
    result: Result = session.exec(stmt)
    passenger = result.all()
    if name in [passenger.name for passenger in boat.passengers]:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, f'{name} уже на лодке')
    if len(boat.passengers) >= boat.seats:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 'Больше нет мест на лодке')
    if not passenger:
        passenger = Passenger(name=name, boat_id=BOAT_ID)
        session.add(passenger)
        session.commit()
    session.refresh(boat)
    return boat


@router.patch('/delete_passenger')
async def delete_passenger(
    name: str,
    session: Session = Depends(get_session)
) -> BoatRead:
    '''Удаление пассажиров с лодки'''
    stmt = select(Passenger).where(
        Passenger.name == name, Passenger.boat_id == BOAT_ID
    )
    passenger = session.exec(stmt).one_or_none()
    if not passenger:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f'Пассажира {name} нет на лодке'
        )
    passenger.sqlmodel_update({'boat_id': None})
    session.add(passenger)
    session.commit()
    boat = session.get(Boat, BOAT_ID)
    return boat
