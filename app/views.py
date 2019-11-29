from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.utils import get_list_of_dates, get_count_per_month
import json


@api_view(['GET'])
def get_video_data(request):
    channel_id = request.query_params.get('id')
    dates = get_list_of_dates(channel_id)
    results = get_count_per_month(dates)
    json_data = json.dumps(results)
    return Response(json_data)
