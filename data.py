from api.courier_api import CourierApi
class CourierData:
    def get_login_password(courier_data, create_response = None):
        if create_response == None:
            create_response = CourierApi.create_courier(courier_data)
        
        if create_response.status_code == 201:
            login_pass = {
                "login": courier_data['login'],
                "password": courier_data['password']
            }
            return login_pass
        
    def get_courier_id(login_response):

        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            return courier_id