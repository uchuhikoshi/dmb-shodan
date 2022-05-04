import os
import re

import googleapiclient.discovery

def get_duration(bad_duration):
    pass

def get_query(search_string):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ['YT_API_KEY']

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=10,
        q=search_string
    )
    response = request.execute()
    items = response['items']

    videoIds = []
    playlistIds = []
    
    for item in items:
        if item['id']['kind'] == "youtube#video":
            videoIds.append(item['id']['videoId'])
        else:
            playlistIds.append(item['id'])
    
    videoIds = ','.join(videoIds)
    # playlistIds = ','.join(playlistIds)

    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=videoIds
    )
    response = request.execute()
    videos = response['items']

    query_list = {
        'title': list(),
        'duration': list(),
        'link': list()
    }
    for video in videos:
        query_list['title'].append(video['snippet']['title'])
        query_list['duration'].append(get_duration(video['contentDetails']['duration']))
        query_list['link'].append(video['id'])

    print(query_list)

    return query_list

