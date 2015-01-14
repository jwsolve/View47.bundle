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
MOVIES_URL = "http://view47.com/list/"
SEARCH_URL = "http://view47.com/search.php?q="

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

	oc.add(DirectoryObject(key = Callback(ShowCategory, title="New Movies", category="new-movies.html", page_count = 1), title = "New Movies", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Cinema Movies", category="cinema-movies.html", page_count = 1), title = "Cinema Movies", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Movies", category="single-movies.html", page_count = 1), title = "Movies", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="TV Series", category="series-movies.html", page_count = 1), title = "TV Series", thumb = R(ICON_MOVIES)))

	return oc

######################################################################################
# Creates page url from category and creates objects from that page

@route(PREFIX + "/showcategory")	
def ShowCategory(title, category, page_count):

	oc = ObjectContainer(title1 = title)
	if page_count == "1":
		try:
			page_data = HTML.ElementFromURL(str(category))
		except:
			page_data = HTML.ElementFromURL(MOVIES_URL + str(category))
	else:
		try:
			page_data = HTML.ElementFromURL(str(category) + '?p=' + str(page_count) + '/')
		except:
			page_data = HTML.ElementFromURL(MOVIES_URL + str(category) + '?p=' + str(page_count) + '/')
	for each in page_data.xpath("//div[contains(@rel,'items-')]"):
		url = each.xpath("./a/@href")[0]
		title = each.xpath("./a/@title")[0]
		thumb = each.xpath("./img/@src")[0]
		
		if title.find("season"):
			oc.add(DirectoryObject(
				key = Callback(ShowEpisodes, title = title, url = url),
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png')
				)
			)
		else:
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
# Creates page url from tv episodes and creates objects from that page

@route(PREFIX + "/showepisodes")	
def ShowEpisodes(title, url):

	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL(url)
	thumb = page_data.xpath("//div[@class='poster']/a/img/@src")
	for each in page_data.xpath("//span[@class='svep']/a"):
		url = each.xpath("./@href")[0]
		title = each.xpath("./@title")[0]

		oc.add(DirectoryObject(
			key = Callback(EpisodeDetail, title = title, url = url),
			title = title,
			thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-cover.png')
			)
		)
	
	return oc

######################################################################################
# Gets metadata and google docs link from episode page. Checks for trailer availablity.

@route(PREFIX + "/episodedetail")
def EpisodeDetail(title, url):
	
	oc = ObjectContainer(title1 = title)
	page = HTML.ElementFromURL(url)

	title = page.xpath("//title/text()")[0].replace(' | View47.Com','',1)
	description = page.xpath("//div[@class='info-txt']/p/text()")[0]
	thumb = page.xpath("//div[@class='poster']/a/img/@src")[0]
	director = page.xpath("//dl[1]/dd[1]/a/text()")
	imdb_rating = page.xpath("//dl[2]/dd[4]/text()")[0]
	
	oc.add(VideoClipObject(
		title = title,
		summary = description,
		directors = director,
		thumb = thumb,
		url = url
		)
	)	
	
	return oc	
