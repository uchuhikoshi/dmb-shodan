import os

import googleapiclient.discovery

def convert_duration(bad_duration):
    pass

def query_for(search_string):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ['YT_API_KEY']

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

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

    return videos

def make_results_list(results):
    results_list = []
    for i in range(len(results)):
        results_list.append({
                'title': results[i]['snippet']['title'],
                'duration': results[i]['contentDetails']['duration'],
                'url': "www.youtube.com/watch?v=" + results[i]['id']
            }
        )

    return results_list 

def search(request):
    response = query_for(request)
    found = make_results_list(response)

    return found

