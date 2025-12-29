import requests
from urls import Urls

class OrderApi:
    @staticmethod
    def create_order(body):
        return requests.post(Urls.CREATE_ORDER_URL, json=body)