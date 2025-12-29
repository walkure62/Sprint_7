import allure
import pytest
from api.courier_api import CourierApi
from helper import ChangeTestData
from data import CourierData


class TestLoginCourier:
    @allure.description("Авторизация курьера с валидными данными")
    def test_success_login_courier(self, courier_data):
        create_response = CourierApi.create_courier(courier_data)
        login_data = CourierData.get_login_password(courier_data, create_response)
        response = CourierApi.login_courier(login_data)
        
        assert response.status_code == 200
        json_response = response.json()
        assert "id" in json_response
        assert json_response["id"] > 0
    
    @allure.description("Все поля. в форме авторизации являются обязательными")    
    @pytest.mark.parametrize('key', [
                                    ('login'),
                                    ('password')
                                ])    
    def test_authorization_requires_all_fields(self, courier_data, key):
        create_data = CourierApi.create_courier(courier_data)
        login_data = CourierData.get_login_password(courier_data, create_data)
        login_data_without_login_or_password = ChangeTestData.delete_key_body(key, login_data)
        response = CourierApi.login_courier(login_data_without_login_or_password)
        
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json()["message"]
    
    @allure.description("Нельзя авторизоваться с неправильным паролем или логином")
    def test_wrong_login_or_password_error(self, courier_data):
        wrong_pass = {
            "login": courier_data["login"],
            "password": "wrongpassword"
        }
        response = CourierApi.login_courier(wrong_pass)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]
    
    @allure.description("Возвращается ошибка, если не заполнено обязательное поле")        
    def test_missing_field_returns_error(self, courier_data):
        no_login = {"password": courier_data["password"]}
        response = CourierApi.login_courier(no_login)
        
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json()["message"]
    
    @allure.description("Возвращается ошибка, если при авторизации пользователь не был найден")  
    def test_unsuccess_login_courier_with_invalid_user(self):
        nonexistent = {
            "login": "nonexistent_user_1",
            "password": "12345"
        }
        response = CourierApi.login_courier(nonexistent)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]
    
    @allure.description("При успешной авторизации в ответе возвращается id курьера")  
    def test_success_returns_id(self, courier_data):
        login_data = CourierData.get_login_password(courier_data, CourierApi.create_courier(courier_data))
        response = CourierApi.login_courier(login_data)
        
        assert response.status_code == 200
        json_response = response.json()
        assert "id" in json_response
        assert isinstance(json_response["id"], int)
        assert json_response["id"] > 0
