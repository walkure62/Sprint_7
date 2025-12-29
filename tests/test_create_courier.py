import allure
import pytest
from api.courier_api import CourierApi
from helper import ChangeTestData


class TestCreateCourier:
    @allure.description("Создание курьера с валидными данными")
    def test_success_create_courier(self, courier_data):
        response = CourierApi.create_courier(courier_data)
        
        assert response.status_code == 201
        assert response.json()["ok"] is True
    
    @allure.description("Нельзя создать двух одинаковых курьеров")    
    def test_cannot_create_two_identical_couriers(self, courier_data):
        data = courier_data
        CourierApi.create_courier(data)
        
        response = CourierApi.create_courier(data)
        
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]
    
    @allure.description("Все поля при создании курьера обязательны для заполнения")
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
    
    @allure.description("Код ответа корректного запроса совпадает с ожидаемым")    
    def test_correct_status_code(self, courier_data):
        response = CourierApi.create_courier(courier_data)
        assert response.status_code == 201
    
    @allure.description("Текст ответа {'ok': True}")    
    def test_success_returns_ok_true(self, courier_data):
        response = CourierApi.create_courier(courier_data)
        json_response = response.json()
        
        assert response.status_code == 201
        assert json_response == {"ok": True}
    
    @allure.description("Нельзя создать курьера, если незаполнено одно из полей")     
    def test_unsuccess_create_courier_with_empty_input(self, courier_data):
        data = ChangeTestData.delete_key_body('password', courier_data)
        response = CourierApi.create_courier(data)
        
        assert response.status_code == 400
        error_msg = response.json()["message"]
        assert "Недостаточно данных" in error_msg
    
    @allure.description("Нельзя создать курьера с логином, который уже занят")     
    def test_unsuccess_create_courier_with_busy_login(self, courier_data):
        data = courier_data
        data_with_busy_login = ChangeTestData.modify_create_body('firstName', 'Anastasia', data)
        CourierApi.create_courier(data)
        response = CourierApi.create_courier(data_with_busy_login)
        
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]
        
        
        