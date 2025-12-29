class CourierData:
    def get_login_password(courier_data, create_response):
        data = courier_data

        if create_response.status_code == 201:
            login_pass = {
                "login": data['login'],
                "password": data['password']
            }
            return login_pass
        
    def get_courier_id(login_response):

        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            return courier_id