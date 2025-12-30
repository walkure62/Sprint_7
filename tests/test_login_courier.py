import allure
import pytest
from api.courier_api import CourierApi
from helper import ChangeTestData
from data import CourierData


class TestLoginCourier:
    def setup_method(self):
        self.created_couriers = []
    
    @allure.description("Авторизация курьера с валидными данными. При успешной авторизации в ответе возвращается id курьера")
    def test_success_login_courier(self, courier_data):
        login_data = CourierData.get_login_password(courier_data)
        response = CourierApi.login_courier(login_data)
        
        assert response.status_code == 200
        json_response = response.json()
        assert "id" in json_response
        assert json_response["id"] > 0
        
        courier_id = CourierData.get_courier_id(response)
        self.created_couriers.append(courier_id)
    
    @allure.description("Все поля. в форме авторизации являются обязательными. Возвращается ошибка, если не заполнено обязательное поле")    
    @pytest.mark.parametrize('key', [
                                    ('login'),
                                    ('password')
                                ])    
    def test_authorization_requires_all_fields(self, courier_data, key):
        login_data = CourierData.get_login_password(courier_data)
        response_1 = CourierApi.login_courier(login_data)
        login_data_without_login_or_password = ChangeTestData.delete_key_body(key, login_data)
        response_2 = CourierApi.login_courier(login_data_without_login_or_password)
        
        assert response_2.status_code == 400
        assert "Недостаточно данных для входа" in response_2.json()["message"]
        
        courier_id = CourierData.get_courier_id(response_1)
        self.created_couriers.append(courier_id)
    
    @allure.description("Нельзя авторизоваться с неправильным паролем или логином")
    def test_wrong_login_or_password_error(self, courier_data):
        wrong_pass = {
            "login": courier_data["login"],
            "password": "wrongpassword"
        }
        response = CourierApi.login_courier(wrong_pass)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]
    
    @allure.description("Возвращается ошибка, если при авторизации пользователь не был найден")  
    def test_unsuccess_login_courier_with_invalid_user(self):
        nonexistent = {
            "login": "nonexistent_user_1",
            "password": "12345"
        }
        response = CourierApi.login_courier(nonexistent)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]
