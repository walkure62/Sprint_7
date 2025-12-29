from faker import Faker

from data import CourierData
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
    
    create_response = CourierApi.create_courier(courier_data)
    login_data = CourierData.get_login_password(courier_data, create_response)
    login_response = CourierApi.login_courier(login_data)
    
    if login_response.status_code != 200:
        print(f"Логин курьера не удался: {login_response.status_code}")

    courier_id = CourierData.get_courier_id(login_response)
    
    delete_response = CourierApi.delete_courier(courier_id)
    
    if delete_response.status_code != 200:
        print(f"Не удалось удалить курьера id={courier_id}")
    

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