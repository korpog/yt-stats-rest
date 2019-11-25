import os
import json
import googleapiclient.discovery
from collections import Counter

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_channel_id_from_url(url):
    idx = url.rfind('/')
    return url[idx + 1:]


def datetime_to_date(datetime):
    # trim datetime string to date
    idx = datetime.find('T')
    date = datetime[:idx]
    return date


def date_to_tuple(date):
    date_tuple = tuple([int(n) for n in date.split('-')])
    return date_tuple


def append_dates_from_results(response, list_of_dates):
    # append api results to list of dates
    for item in response["items"]:
        date = datetime_to_date(item["snippet"]["publishedAt"])
        date_tuple = date_to_tuple(date)
        list_of_dates.append(date_tuple)


def get_list_of_dates(channel_id):
    # get submisssion dates for 500 most recent videos from channel with channel_id
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

    # results have to be queried multiple times using next page token
    count = 0
    while nextPageToken and count < 2:
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

    with open('tuples.txt', 'w') as file:
        file.write(
            '\n'.join(f"({t[0]}, {t[1]}, {t[2]})" for t in list_of_dates))

    print(list_of_dates)

    return list_of_dates


def fill_zeros(dictionary):
    # if key (month) wasn't present in the results, set it to zero
    for i in range(1, 13):
        if i not in dictionary.keys():
            dictionary[i] = 0


def get_count_per_month(list_tuples):
    # count videos per month for every year
    years_set = set([tup[0] for tup in list_tuples])
    results = {}
    for year in years_set:
        cntr = Counter()
        for tup in list_tuples:
            if tup[0] == year:
                cntr[tup[1]] += 1
        new_dict = dict(cntr)
        fill_zeros(new_dict)
        results[year] = new_dict
    return results


def main():
    cid = get_channel_id_from_url(
        "https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ")
    dates = get_list_of_dates(cid)
    results = get_count_per_month(dates)


if __name__ == "__main__":
    main()
