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

	html = HTML.ElementFromURL(BASE_URL)
	for nav in html.xpath("//ul[@class='col-2']/li"):
		title = nav.xpath("./a/@title")[0]
		category = nav.xpath("./a/@href")[0].replace('http://view47.com/genres','',1)
		oc.add(DirectoryObject(key = Callback(ShowCategory, title=title, category=category, page_count = 1), title = title, thumb = R(ICON_MOVIES)))

	return oc

######################################################################################
# Creates page url from category and creates objects from that page

@route(PREFIX + "/showcategory")	
def ShowCategory(title, category, page_count):

	oc = ObjectContainer(title1 = title)
	if page_count == "1":
		page_data = HTML.ElementFromURL(MOVIES_URL + str(category))
	else:
		page_data = HTML.ElementFromURL(MOVIES_URL + str(category) + '?p=' + str(page_count) + '/')
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
	title = page_data.xpath("//div[@class='info-movie']/h2/text()")[0]
	thumb = page_data.xpath("//div[@class='info-movie']/div/a/img/@src")[0]
	
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
	data = HTTP.Request(SEARCH_URL + '%s' % String.Quote(query + '.html', usePlus=True), headers="").content

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