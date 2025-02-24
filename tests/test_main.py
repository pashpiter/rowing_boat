from datetime import date

import pytest

from .testdata import (DEFAULT_BOAT, PASSENGER_ONE, PASSENGER_THREE,
                       PASSENGER_TWO)


@pytest.mark.positive
def test_get_default_boat(client, boat):
    '''Проверка полей у дефолтной лодки'''
    response = client.get('/api/v1/boat')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == DEFAULT_BOAT['name']
    assert data['seats'] == DEFAULT_BOAT['seats']
    assert data['speed'] == DEFAULT_BOAT['speed']
    assert data['direction'] == DEFAULT_BOAT['direction']
    assert PASSENGER_ONE['name'] in [
        passenger['name'] for passenger in data['passengers']
    ]
    assert PASSENGER_TWO['name'] in [
        passenger['name'] for passenger in data['passengers']
    ]
    assert data['age'] == 0


@pytest.mark.positive
def test_boat_age(client, boat_with_passenger_one_created_at):
    '''Проверка корректного возраста лодки'''
    response = client.get('/api/v1/boat')
    assert response.status_code == 200
    data = response.json()
    assert data['age'] == (date.today() - date(2000, 1, 1)).days


@pytest.mark.negative
def test_negative_add_extra_passenger(client, boat):
    '''Негативная проверка добавления пассажира'''
    query = f'?name={PASSENGER_THREE["name"]}'
    response = client.patch('/api/v1/boat/add_passenger' + query)
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'Больше нет мест на лодке'


@pytest.mark.negative
def test_negative_add_empty_query(client, empty_boat):
    '''Негативная проверка добавления пассажира без query'''
    response = client.patch('/api/v1/boat/add_passenger')
    assert response.status_code == 422


@pytest.mark.negative
def test_negative_add_passenger_already_on_boat(client, boat):
    '''Негативная проверка повторного добавления пассажира'''
    query = f'?name={PASSENGER_ONE["name"]}'
    response = client.patch('/api/v1/boat/add_passenger' + query)
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == f'{PASSENGER_ONE["name"]} уже на лодке'


@pytest.mark.positive
def test_postitive_add_passenger(client, boat_with_passenger_one_created_at):
    '''Проверка добаления пассажира в лодку'''
    query = f'?name={PASSENGER_THREE["name"]}'
    response = client.patch('/api/v1/boat/add_passenger' + query)
    assert response.status_code == 200
    data = response.json()
    assert PASSENGER_THREE['name'] in [
        passenger['name'] for passenger in data['passengers']
    ]


@pytest.mark.positive
def test_postitive_delete_passenger(
    client, boat_with_passenger_one_created_at
):
    '''Проверка удаление пассажира с лодки'''
    query = f'?name={PASSENGER_ONE["name"]}'
    response = client.patch('/api/v1/boat/delete_passenger' + query)
    assert response.status_code == 200
    data = response.json()
    assert len(data['passengers']) == 0


@pytest.mark.negative
def test_negative_delete_passenger(client, empty_boat):
    '''Негативная проверка удаления несуществующего пассажира с лодки'''
    query = f'?name={PASSENGER_ONE["name"]}'
    response = client.patch('/api/v1/boat/delete_passenger' + query)
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == f'Пассажира {PASSENGER_ONE["name"]} нет на лодке'


@pytest.mark.negative
def test_negative_delete_empty_query(client, boat):
    '''Негативная проверка удаления пассажира без query'''
    response = client.patch('/api/v1/boat/delete_passenger')
    assert response.status_code == 422


@pytest.mark.negative
def test_negative_reduce_num_of_seats_full_passengers(client, boat):
    '''Негативная проверка уменьшения количества мест в лодке
    при большим количестве пассажиров в лодке'''
    query = '?seats=1'
    response = client.patch('/api/v1/boat' + query)
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == ('Уберите пассажиров перед тем как '
                              'уменьшить количество мест')


@pytest.mark.positive
@pytest.mark.parametrize('num_seats', [1, 6])
def test_positive_patch_num_seats(client, empty_boat, num_seats):
    '''Проверка изменения колчиества мест в лодке'''
    query = f'?seats={num_seats}'
    response = client.patch('/api/v1/boat' + query)
    assert response.status_code == 200
    data = response.json()
    assert data['seats'] == num_seats


@pytest.mark.negative
@pytest.mark.parametrize('num_seats', [0, -1, 7])
def test_negative_patch_num_seats(client, empty_boat, num_seats):
    '''Негативная проверка изменения количества мест в лодке'''
    query = f'?seats={num_seats}'
    response = client.patch('/api/v1/boat' + query)
    assert response.status_code == 422


@pytest.mark.positive
@pytest.mark.parametrize('speed', [0, 4])
def test_positive_patch_speed(client, boat, speed):
    '''Проверка изменения скорости лодки'''
    query = f'?speed={speed}'
    response = client.patch('/api/v1/boat' + query)
    assert response.status_code == 200
    data = response.json()
    assert data['speed'] == speed


@pytest.mark.negative
@pytest.mark.parametrize('speed', [-1, 5])
def test_negative_patch_speed(client, empty_boat, speed):
    '''Негативная проверка изменения скорости лодки'''
    query = f'?speed={speed}'
    response = client.patch('/api/v1/boat' + query)
    assert response.status_code == 422


@pytest.mark.positive
@pytest.mark.parametrize('direction', ['Вперед', 'Назад'])
def test_positive_patch_direction(client, boat, direction):
    '''Проверка изменения направления лодки'''
    query = f'?direction={direction}'
    response = client.patch('/api/v1/boat' + query)
    assert response.status_code == 200
    data = response.json()
    assert data['direction'] == direction


@pytest.mark.negative
@pytest.mark.parametrize('direction', ['', 'Вбок'])
def test_negative_patch_direction(client, empty_boat, direction):
    '''Негативная проверка изменения направления лодки'''
    query = f'?direction={direction}'
    response = client.patch('/api/v1/boat' + query)
    assert response.status_code == 422
