import allure
import pytest
from api.courier_api import CourierApi
from data import CourierData
from helper import ChangeTestData


class TestCreateCourier:
    def setup_method(self):
        self.created_couriers = []
    
    @allure.description("Создание курьера с валидными данными")
    def test_success_create_courier(self, courier_data):
        response = CourierApi.create_courier(courier_data)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_data = CourierData.get_login_password(courier_data, response)
        login_response = CourierApi.login_courier(login_data)
        courier_id = CourierData.get_courier_id(login_response)
        self.created_couriers.append(courier_id)
    
    @allure.description("Нельзя создать двух одинаковых курьеров")    
    def test_cannot_create_two_identical_couriers(self, courier_data):
        data = courier_data
        response_1 = CourierApi.create_courier(data)
        
        response_2 = CourierApi.create_courier(data)
        
        assert response_2.status_code == 409
        assert "Этот логин уже используется" in response_2.json()["message"]
        
        login_data = CourierData.get_login_password(data, response_1)
        login_response = CourierApi.login_courier(login_data)
        courier_id = CourierData.get_courier_id(login_response)
        self.created_couriers.append(courier_id)
    
    @allure.description("Все поля при создании курьера обязательны для заполнения. Нельзя создать курьера, если незаполнено одно из полей")
    @pytest.mark.parametrize('key', 
                             [('login'),
                              ('password'),
                              ('firstName')
                              ])     
    def test_create_requires_all_fields(self, courier_data, key):
        data = ChangeTestData.delete_key_body(key, courier_data)
        response = CourierApi.create_courier(data)
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]
    
    @allure.description("Нельзя создать курьера с логином, который уже занят")     
    def test_unsuccess_create_courier_with_busy_login(self, courier_data):
        data = courier_data
        response_1 = CourierApi.create_courier(data)
        data_with_busy_login = ChangeTestData.modify_create_body('firstName', 'Anastasia', data)
        CourierApi.create_courier(data)
        response_2 = CourierApi.create_courier(data_with_busy_login)
        
        assert response_2.status_code == 409
        assert "Этот логин уже используется" in response_2.json()["message"]
        
        login_data = CourierData.get_login_password(data, response_1)
        login_response = CourierApi.login_courier(login_data)
        courier_id = CourierData.get_courier_id(login_response)
        self.created_couriers.append(courier_id)
        
        
        