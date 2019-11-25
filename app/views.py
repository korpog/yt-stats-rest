from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import utils


@api_view
def get_video_data(request):
    cid = utils.get_channel_id_from_url(
        "https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ")
    dates = utils.get_list_of_dates(cid)
    results = utils.get_count_per_month(dates)
    json_data = json.dumps(results)
    return Response(json_data)
