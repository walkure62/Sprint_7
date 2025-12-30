import allure
import pytest
from api.order_api import OrderApi
from helper import ChangeTestData

class TestCreateOrder:
    
    @allure.description("Можно создать заказ с разным цветом самоката или без выбора цвета")  
    @pytest.mark.parametrize("color", [
                                        ["BLACK"],           
                                        ["GREY"],            
                                        ["BLACK", "GREY"],              
                                        [],                  
                                    ])
    def test_create_order_color_variants(self, order_data, color):
        test_data = order_data.copy()
        test_data["color"] = color
        
        response = OrderApi.create_order(test_data)
        
        assert response.status_code == 201
        json_response = response.json()
        assert "track" in json_response
        track_id = json_response["track"]
        assert isinstance(track_id, int)
        assert track_id > 0
        
        print(f"Заказ создан: track={track_id}, color={color}")
    
    @allure.description("Успешное создание заказа со всеми заполненными полями")     
    def test_create_order_all_fields(self, order_data):
        response = OrderApi.create_order(order_data)
        
        assert response.status_code == 201
        json_response = response.json()
        assert "track" in json_response
    
    @allure.description("Успешное создание заказа со всеми обязательными полями")
    def test_create_order_no_color(self, order_data):
        
        test_data = ChangeTestData.delete_key_body('color', order_data)
        
        response = OrderApi.create_order(test_data)
        
        assert response.status_code == 201
        json_response = response.json()
        assert "track" in json_response
    
    @allure.description("Тело ответа содержит track")    
    def test_create_order_response_contains_track(self, order_data):
        response = OrderApi.create_order(order_data)
        
        assert response.status_code == 201
        json_response = response.json()
        assert "track" in json_response
        assert isinstance(json_response["track"], int)
        assert json_response["track"] > 0
    
    @allure.description("При отсутствии обязательного поля отображается ошибка, заказ не создается")      
    @pytest.mark.parametrize("missing_field", [
        "firstName", "lastName", "address", "metroStation", 
        "phone", "rentTime", "deliveryDate"
    ])
    def test_create_order_missing_required_field(self, order_data, missing_field):
    
        test_data = ChangeTestData.delete_key_body(missing_field, order_data)
        
        response = OrderApi.create_order(test_data)
        
        assert response.status_code == 400
