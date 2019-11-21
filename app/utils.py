import os
import json

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_channel_id_from_url(url):
    idx = url.rfind('/')
    return url[idx + 1:]


def datetime_to_date(datetime):
    idx = datetime.find('T')
    date = datetime[:idx]
    return date


def date_to_tuple(date):
    date_tuple = tuple(date.split('-'))
    return date_tuple


def append_dates_from_results(response, list_of_dates):
    for item in response["items"]:
        date = datetime_to_date(item["snippet"]["publishedAt"])
        date_tuple = date_to_tuple(date)
        list_of_dates.append(date_tuple)


def get_list_of_dates(channel_id):

    with open('credentials.json', 'r') as file:
        credentials = json.load(file)

    api_service_name = "youtube"
    api_version = "v3"
    api_key = credentials["api_key"]

    list_of_dates = []

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        relevanceLanguage="en",
        channelId=channel_id,
        maxResults=50,
        order="date",
    )

    response = request.execute()
    append_dates_from_results(response, list_of_dates)
    nextPageToken = response["nextPageToken"]

    count = 0
    while nextPageToken and count <= 9:
        request = youtube.search().list(
            part="snippet",
            relevanceLanguage="en",
            channelId=channel_id,
            maxResults=50,
            order="date",
            pageToken=nextPageToken
        )
        response = request.execute()
        append_dates_from_results(response, list_of_dates)
        count += 1
        if response["nextPageToken"] is None:
            break

    with open("results.json", "w") as file:
        json.dump(response, file)

    print(len(list_of_dates))
    return list_of_dates


def main():
    cid = get_channel_id_from_url(
        "https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ")
    print(get_list_of_dates(cid))


if __name__ == "__main__":
    main()
