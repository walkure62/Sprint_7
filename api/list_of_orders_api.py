import requests
from urls import Urls

class ListOfOrdersApi:
    @staticmethod
    def get_list_of_orders():
        return requests.get(Urls.GET_LIST_OF_ORDER_URL)