from urllib.request import urlopen

from parsers import ImageUrlCrawler


def test_crawler():
    url = 'https://www.smashingmagazine.com/2017/04/desktop-wallpaper-calendars-may-2017/'
    urls = get_urls_by_crawler(url)
    assert urls is not None


def get_urls_by_crawler(url):
    crawler = ImageUrlCrawler()
    data = str(urlopen(url).read())
    crawler.feed(data)
    return crawler.urls
