import datetime
import sys
from html.parser import HTMLParser


class ImageUrlCrawler(HTMLParser):
    """
    class what will crawl image urls
    """
    # current tags
    is_article_tag = False
    is_ul_tag = False
    is_a_tag = False

    # need 3rd tag if not with_calendar else 2nd tag
    li_tag_counter = 0

    # collection of urls
    urls = []

    # tags with that classes is unnecessary
    unnecessary_classes = ('pmd clearfix', )

    def __init__(self, date=datetime.date.today(),
                 resolution='1920x1440', with_calendar=False):
        self.date = date
        self.resolution = resolution.replace('x', '×')
        self.with_calendar = with_calendar
        super().__init__()

    def handle_starttag(self, tag, attrs):
        self.check_article_tag(tag)
        self.check_ul_tag(tag, attrs)
        self.check_a_tag(tag)

        self.tag_attrs = attrs

        if self.is_ul_tag and tag == 'li':
            self.li_tag_counter += 1

    def handle_endtag(self, tag):
        self.check_article_tag(tag)
        self.check_ul_close_tag(tag)
        self.check_a_tag(tag)
        self.check_for_end(tag)

    def handle_data(self, data):
        wallpaper_wo_calendar = self.li_tag_counter == 3 and not self.with_calendar
        wallpaper_with_calendar = self.li_tag_counter == 2 and self.with_calendar
        if wallpaper_wo_calendar or wallpaper_with_calendar:
            if self.is_a_tag:
                self.collecti_url(data)

    def collecti_url(self, data):
        if data == self.resolution:
            url = dict(self.tag_attrs).get('href')
            if url:
                self.urls.append(url)

    def check_article_tag(self, tag):
        if tag == 'article':
            self.is_article_tag = not self.is_article_tag

    def check_ul_tag(self, tag, attrs):
        if self.is_article_tag and tag == 'ul':
            tag_class = dict(attrs).get('class')
            if tag_class not in self.unnecessary_classes:
                self.is_ul_tag = True

    def check_ul_close_tag(self, tag):
        if tag == 'ul':
            self.is_ul_tag = False
            self.li_tag_counter = 0

    def check_a_tag(self, tag):
        if tag == 'a':
            self.is_a_tag = not self.is_a_tag

    def check_for_end(self, tag):
        if not self.urls and tag == 'html':
            print('Urls wasn\'t found, may be resolution isn\'t correct')
            sys.exit()
