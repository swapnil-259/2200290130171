from django.http import JsonResponse
from django.views import View
from apps.numstats.api.v1.services import NumberService

class NumberView(View):
    def get(self, request, numberid):
        window_prev_state, window_curr_state, numbers, average = NumberService.add_and_calculate_average(numberid)

        if window_prev_state is None:
            return JsonResponse({
                'error': 'Error in fetching numbers or processing data.'
            }, status=400)
        response_data = {
            'windowPrevState': window_prev_state,
            'windowCurrState': window_curr_state,
            'numbers': numbers,
            'avg': round(average, 2) if average is not None else None
        }
        return JsonResponse(response_data)
