import re
import urllib.request
import urllib.parse
import youtube_dl as yt


ytopts = {
	'default_search': 'ytsearch',
	'format': 'bestaudio/best',
	'extractaudio': True,
	# 'postprocessors': [{
	# 	'preferredconc': 'mp3',
	# 	'preferredquality': 192
	# }],
	'outtmpl': '/video_cache/%(title)s.%(ext)s',
}


def get_url(search):
	query_string = urllib.parse.urlencode({'search_query': search})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	urls = ["http://www.youtube.com/watch?v=" + res for res in search_results[:5]]

	return urls


def get_info(url):
	info = []

	with yt.YoutubeDL(ytopts) as ytdl:
		meta = ytdl.extract_info(url, download=False)
		info.append(meta.get('title'))
		info.append(f"{meta.get('duration') // 60}:{meta.get('duration') % 60}")
		info.append(url)

	return info


def get_query(search):
	query = {
		'title': [],
		'duration': [],
		'url': []
	}
	urls = get_url(search)
	url_infos = []

	for url in urls:
		url_infos.append(get_info(url))

	for url_info in url_infos:
		query['title'].append(url_info[0])
		query['duration'].append(url_info[1])
		query['url'].append(url_info[2])

	return query


def download(url):
	with yt.YoutubeDL(ytopts) as ytdl:
		ytdl.download(url)
