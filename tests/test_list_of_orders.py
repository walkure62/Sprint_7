import allure
from api.list_of_orders_api import ListOfOrdersApi

class TestListOfOrder:
    
    @allure.description("В тело ответа возвращается список заказов")  
    def test_orders_list_returns_list_of_orders(self):
        response = ListOfOrdersApi.get_list_of_orders()
        json_response = response.json()
        
        assert response.status_code == 200
        assert "orders" in json_response
        assert isinstance(json_response["orders"], list)

    