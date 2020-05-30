import re
import urllib.request
import urllib.parse
import youtube_dl as yt


ytopts = {
	'default_search': 'ytsearch',
	'format': 'bestaudio/best',
	'extractaudio': True,
	'postprocessors': [{
		'preferredconc': 'mp3',
		'preferredquality': 192
	}],
	'outtmpl': '/video_cache/%(title)s.%(ext)s',
	'postprocessors': [{
		'preferredconc': 'mp3',
		'preferredquality': 192
	}],
	'match_title': '',
	'playlist_items': '',
}


def query(search):
	print("in `query`")
	# search = "eric brosius engineering"
	queryString = urllib.parse.urlencode({'search_query': search})
	print(f"queryString: {queryString}")
	htmlContent = urllib.request.urlopen("http://www.youtube.com/results?" + queryString)
	print("got html content")
	searchResults = re.findall(r'href=\"\/watch\?v=(.{11})', htmlContent.read().decode())
	print("got search results")
	url = "http://www.youtube.com/watch?v=" + searchResults[0]
	print(f"url: {url}")

	# with yt.YoutubeDL(ytopts) as ytdl:
	#	meta = ytdl.extract_info(url, download=False)
	#
	#	return {'title': meta.get('title'), 'duration': meta.get('duration')}

	return url


def get_info(url):
	with yt.YoutubeDL(ytopts) as ytdl:
		meta = ytdl.extract_info(url, download=False)

		return {'title': meta.get('title'), 'duration': meta.get('duration')}


def download(url):
	with yt.YoutubeDL(ytopts) as ytdl:
		ytdl.download(url)
