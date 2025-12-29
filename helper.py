from datetime import datetime, timedelta
import random
import string


class ChangeTestData:
    def modify_create_body(key, value, data):
        body = data.copy()
        body[key] = value
        return body
    
    def delete_key_body(key, data):
        body = data.copy()
        del body[key]
        return body
    
def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
    
def generate_random_date():
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        total_days = (end_date - start_date).days
        random_days = random.randint(0, total_days)
        random_future_date = start_date + timedelta(days=random_days)
        return random_future_date.strftime('%Y-%m-%d')

