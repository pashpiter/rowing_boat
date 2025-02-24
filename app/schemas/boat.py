from datetime import date
from enum import Enum
from typing import List

from pydantic import computed_field, model_validator
from sqlmodel import Field, Relationship, SQLModel

from schemas.passengers import Passenger, PassengerRead


class BoatDirection(str, Enum):
    '''Направления движения лодки'''
    FORWARD = 'Вперед'
    BACK = 'Назад'


class BoatBase(SQLModel):
    name: str = Field(index=True, max_length=20, min_length=1)
    seats: int | None = Field(default=2, le=6, ge=1)
    speed: float | None = Field(default=0, le=4, ge=0)
    direction: BoatDirection = Field(default=BoatDirection.FORWARD)


class Boat(BoatBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    passengers: List['Passenger'] = Relationship(
        sa_relationship_kwargs={'lazy': 'joined'}
    )
    created_at: date = date.today()

    @model_validator(mode='before')
    def num_of_pass_less_than_seats(cls, data):
        if len(data.passengers) > data.seats:
            raise ValueError(
                'Num of passangers can not be greater than num of seats'
            )


class BoatRead(BoatBase):
    passengers: List[PassengerRead] | None = []
    created_at: date = Field(exclude=True)

    @computed_field
    @property
    def age(self) -> int:
        return (date.today() - self.created_at).days
