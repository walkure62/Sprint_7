from faker import Faker

from api.courier_api import CourierApi
from helper import generate_random_string, generate_random_date

import pytest

@pytest.fixture
def courier_data():
    
    password = generate_random_string(10)
    fake_ru = Faker('ru_RU')
    
    courier_data = {
        "login": fake_ru.user_name(),
        "password": password,
        "firstName": fake_ru.first_name()
    }
    
    yield courier_data
    print(courier_data)

@pytest.fixture(autouse=True)
def cleanup_courier_after_test(request):
    
    def fin():
        if hasattr(request.instance, 'created_couriers'):
            for courier_id in request.instance.created_couriers:
                CourierApi.delete_courier(courier_id)
                print(f"Курьер ID={courier_id} удален")
    
    request.addfinalizer(fin)
    yield

@pytest.fixture
def order_data():
    fake_ru = Faker('ru_RU')

    order_data = {
    "firstName": fake_ru.first_name(),
    "lastName": fake_ru.last_name(),
    "address": generate_random_string(10),
    "metroStation": 4,
    "phone": f'7{fake_ru.msisdn()[3:]}',
    "rentTime": 5,
    "deliveryDate": generate_random_date(),
    "comment": fake_ru.text(),
    "color": ["BLACK"]
}
    return order_data

