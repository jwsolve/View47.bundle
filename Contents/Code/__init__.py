######################################################################################
#
#	View47.com - v0.10
#
######################################################################################

TITLE = "View 47"
PREFIX = "/video/view47"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_LIST = "icon-list.png"
ICON_COVER = "icon-cover.png"
ICON_SEARCH = "icon-search.png"
ICON_NEXT = "icon-next.png"
ICON_MOVIES = "icon-movies.png"
ICON_SERIES = "icon-series.png"
ICON_QUEUE = "icon-queue.png"
BASE_URL = "http://view47.com"
MOVIES_URL = "http://view47.com/genres"
SEARCH_URL = "http://view47.com/search/"

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_LIST)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_MOVIES)
	VideoClipObject.art = R(ART)
	
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
	HTTP.Headers['Referer'] = 'http://view47.com/'
	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	oc.add(InputDirectoryObject(key = Callback(Search), title='Search', summary='Search View47', prompt='Search for...'))

	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Film Noir", category="film-noir", page_count = 1), title = "Film Noir", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Talk Show", category="talk-show", page_count = 1), title = "Talk Show", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="News", category="news", page_count = 1), title = "News", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Reality TV", category="reality-tv", page_count = 1), title = "Realty TV", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Documentary", category="documentary", page_count = 1), title = "Documentary", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Short", category="short", page_count = 1), title = "Short", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Family", category="family", page_count = 1), title = "Family", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Fantasy", category="fantasy", page_count = 1), title = "Fantasy", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="History", category="history", page_count = 1), title = "History", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Horror", category="horror", page_count = 1), title = "Horror", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Music", category="music", page_count = 1), title = "Music", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Mystery", category="mystery", page_count = 1), title = "Mystery", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Romance", category="romance", page_count = 1), title = "Romance", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Sci-Fi", category="sci-fi", page_count = 1), title = "Sci-Fi", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Short", category="short", page_count = 1), title = "Short", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Sport", category="sport", page_count = 1), title = "Sport", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Talk Show", category="talk-show", page_count = 1), title = "Talk Show", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Thriller", category="thriller", page_count = 1), title = "Thriller", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="War", category="war", page_count = 1), title = "War", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Western", category="western", page_count = 1), title = "Western", thumb = R(ICON_MOVIES)))
	return oc

######################################################################################
# Creates page url from category and creates objects from that page

@route(PREFIX + "/showcategory")	
def ShowCategory(title, category, page_count):

	oc = ObjectContainer(title1 = title)
	if page_count == "1":
		page_data = HTML.ElementFromURL(BASE_URL + '/genres/' + str(category) + '.html')
	else:
		page_data = HTML.ElementFromURL(BASE_URL + '/genres/' + str(category) + '.html?p=' + str(page_count) + '/')
	for each in page_data.xpath("//div[contains(@rel,'items-')]"):
		url = each.xpath("./a/@href")[0]
		title = each.xpath("./a/@title")[0]
		thumb = each.xpath("./img/@src")[0]
		
		oc.add(DirectoryObject(
			key = Callback(EpisodeDetail, title = title, url = url),
			title = title,
			thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-cover.png')
			)
		)

	oc.add(NextPageObject(
		key = Callback(ShowCategory, title = category, category = category, page_count = int(page_count) + 1),
		title = "More...",
		thumb = R(ICON_NEXT)
			)
		)
	
	return oc

######################################################################################
# Gets metadata and google docs link from episode page. Checks for trailer availablity.

@route(PREFIX + "/episodedetail")
def EpisodeDetail(title, url):
	
	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL(url)
	title = page_data.xpath("//div[@class='info-movie']/h2/text()")
	thumb = page_data.xpath("//div[@class='info-movie']/div/a/img/@src")[0]

	#load recursive iframes to find google docs url
	first_frame_url = page_data.xpath("//param[@name='flashvars']/text()")
	#page_content = HTTP.Request(url).content
	title = first_frame_url
	#title = url
	#title = Regex('.*&proxy.link=(.*)', Regex.IGNORECASE|Regex.MULTILINE).search(page_content).groups()[0]
	
	oc.add(VideoClipObject(
		url = url,
		title = title,
		thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-cover.png')
		)
	)	
	
	return oc	

####################################################################################################
@route(PREFIX + "/search")
def Search(query):

	oc = ObjectContainer(title2='Search Results')
	data = HTTP.Request(SEARCH_URL + '%s' % String.Quote(query, usePlus=True), headers="").content

	html = HTML.ElementFromString(data)

	for movie in html.xpath("//ul[@class='list-film']/li"):
		url = movie.xpath("./div[@class='inner']/a/@href")[0]
		title = movie.xpath("./div[@class='inner']/a/@title")[0]
		thumb = movie.xpath("./div[@class='inner']/a/img/@data-original")[0]

		oc.add(DirectoryObject(
				key = Callback(EpisodeDetail, title = title, url = url),
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-cover.png')
				)
		)

	return oc