# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
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
        maxResults=50,
        q="whatever"
    )

    response = request.execute()

    with open('results.json', 'w') as file:
        json.dump(response, file)

    print(response)


if __name__ == "__main__":
    main()