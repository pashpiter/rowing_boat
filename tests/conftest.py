from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from db.database import get_session
from main import app
from schemas.boat import Boat
from schemas.passengers import Passenger

from .testdata import DEFAULT_BOAT, PASSENGER_ONE, PASSENGER_TWO


@pytest.fixture(name='session')
def session_fixture():
    '''Фикстура для сессии'''
    engine = create_engine(
        'sqlite:///tests/test_database.db',
        connect_args={'check_same_thread': False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name='client')
def client_fixture(session: Session):
    '''Клиентская фикстура'''
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name='boat')
def default_boat(session: Session):
    '''Лодка с двумя пассажирами и дефолтными значениями'''
    boat = Boat(name=DEFAULT_BOAT['name'])
    passenger_1 = Passenger(name=PASSENGER_ONE['name'], boat_id=boat.id)
    passenger_2 = Passenger(name=PASSENGER_TWO['name'], boat_id=boat.id)
    session.add_all([boat, passenger_1, passenger_2])
    session.commit()


@pytest.fixture(name='empty_boat')
def empty_boat(session: Session):
    '''Лодка без пассажиров и дефолтными значениями'''
    boat = Boat(name=DEFAULT_BOAT['name'])
    session.add(boat)
    session.commit()


@pytest.fixture(name='boat_with_passenger_one_created_at')
def boat_with_passenger_one_and_created_at(session: Session):
    '''Лодка с PASSENGER_ONE и датой создания 01.01.2000'''
    boat = Boat(name=DEFAULT_BOAT['name'], created_at=date(2000, 1, 1))
    passenger_1 = Passenger(name=PASSENGER_ONE['name'], boat_id=boat.id)
    session.add_all([boat, passenger_1])
    session.commit()
