from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends
from schemas.boat import Boat
from schemas.passengers import Passenger


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def create_boat():
    session: Session = next(get_session())
    boat = session.get(Boat, 1)
    if not boat:
        boat = Boat(name='Титаник')
        passenger_1 = Passenger(name='Никита', boat_id=1)
        passenger_2 = Passenger(name='Андрей', boat_id=1)
        session.add_all([boat, passenger_1, passenger_2])
        session.commit()


def create_table_and_boat():
    SQLModel.metadata.create_all(engine)
    create_boat()
