import os
import json

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_channel_id_from_url(url):
    idx = url.rfind('/')
    return url[idx + 1:]


def get_list_of_dates(channel_id):

    with open('credentials.json', 'r') as file:
        credentials = json.load(file)

    api_service_name = "youtube"
    api_version = "v3"
    api_key = credentials["api_key"]

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
    list_of_dates = '\n'.join([item["snippet"]["publishedAt"]
                               for item in response["items"]])

    with open("results.json", "w") as file:
        json.dump(response, file)

    return list_of_dates


def main():
    cid = get_channel_id_from_url(
        "https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ")
    print(get_list_of_dates(cid))


if __name__ == "__main__":
    main()
