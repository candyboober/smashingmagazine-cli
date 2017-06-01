import argparse
import os
import uuid
from urllib.request import urlopen, urlretrieve

from factories import DirFactory, UrlFactory
from parsers import ImageUrlCrawler


def crawl_images(urls, to):
    for url in urls:
        urlretrieve(url, os.path.join(to, uuid.uuid4().hex + '.jpg'))

def get_cli_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-D, --date',
        help='Format mm-YYYY, default datetime.date.today()',
        dest='date')
    arg_parser.add_argument(
        '-R, --resolution',
        help='Format XxY, default 1920x1440',
        dest='resolution')
    arg_parser.add_argument(
        '-P --postfix',
        help='Postfix for directory name, default smashingmagazine',
        dest='postfix')
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = get_cli_args()
    url = UrlFactory.create_url(args)

    crawler = ImageUrlCrawler()
    data = str(urlopen(url).read())
    crawler.feed(data)

    dirname = DirFactory.make_dir(args.postfix, args.date)

    crawl_images(crawler.urls, dirname)
