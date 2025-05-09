import requests
from django.db.models import Avg
from apps.numstats.models import Number
from apps.numstats.choices import StatusChoices

class NumberFetcher:
    BASE_URL = "http://20.244.56.144/evaluation-service/"
    API_TOKEN ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQ2ODAwODI1LCJpYXQiOjE3NDY4MDA1MjUsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjAwYTViMDFjLWZiYWUtNDY4Ny04ZmEzLWY0MGM4NWJmMjhiOCIsInN1YiI6InN3YXBuaWwuMjIyNmVjMTA4OEBraWV0LmVkdSJ9LCJlbWFpbCI6InN3YXBuaWwuMjIyNmVjMTA4OEBraWV0LmVkdSIsIm5hbWUiOiJzd2FwbmlsIGFncmF3YWwiLCJyb2xsTm8iOiIyMjAwMjkwMTMwMTcxIiwiYWNjZXNzQ29kZSI6IlN4VmVqYSIsImNsaWVudElEIjoiMDBhNWIwMWMtZmJhZS00Njg3LThmYTMtZjQwYzg1YmYyOGI4IiwiY2xpZW50U2VjcmV0Ijoic0FyRWp0VXNkenBGSGFrViJ9.4o6k2l2FmVcU4U7RsjU7LuFQpSJrpjdSAzSJyBcmKAc"

    @staticmethod
    def fetch_numbers(number_id):
        headers = {
            "Authorization": f"Bearer {NumberFetcher.API_TOKEN}"
        }
        try:
            response = requests.get(
                f"{NumberFetcher.BASE_URL}{number_id}",
                headers=headers,
                timeout=0.5
            )
            response.raise_for_status()
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {number_id}: {e}")
            return None



class NumberService:
    WINDOW_SIZE = 10

    @staticmethod
    def add_and_calculate_average(number_id):
        fetched_numbers = NumberFetcher.fetch_numbers(number_id)
        print("fetch", fetched_numbers)
        
        if fetched_numbers is None:
            return None, None, None, None 

        number_list = fetched_numbers.get("numbers", [])

        window_prev_state = list(Number.objects.filter(number_id=number_id).order_by('created_at').values_list('value', flat=True))

        stored_numbers_set = set(window_prev_state)
        new_numbers = []

        for num in number_list:
            if num not in stored_numbers_set:
                stored_numbers_set.add(num)
                Number.objects.create(
                number_id=number_id,
                value=num,
            )
                new_numbers.append(num)

        while Number.objects.filter(number_id=number_id).exclude(status=StatusChoices.DELETE).count() > NumberService.WINDOW_SIZE:
            oldest_number = Number.objects.filter(number_id=number_id).exclude(status=StatusChoices.DELETE).order_by('created_at').first()
            oldest_number.status =StatusChoices.DELETE
            oldest_number.save()

        stored_numbers = Number.objects.filter(number_id=number_id).exclude(status=StatusChoices.DELETE).order_by('created_at')

        if stored_numbers.count() >= NumberService.WINDOW_SIZE:
            average = stored_numbers.aggregate(Avg('value'))['value__avg']
        else:
            average = None  

        window_prev_state = list(stored_numbers.values('value')) 
        window_curr_state = list(stored_numbers.values('value')) 
        numbers = new_numbers  

        return window_prev_state, window_curr_state, numbers, average
