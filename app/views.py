from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.utils import get_channel_id_from_url, get_list_of_dates, get_count_per_month
import json


@api_view
def get_video_data(request, url):
    cid = get_channel_id_from_url(url)
    dates = get_list_of_dates(cid)
    results = get_count_per_month(dates)
    json_data = json.dumps(results)
    return Response(json_data)
