import datetime

from factories import DirFactory, UrlFactory


class FakeArgs:
    date = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_url_factory():
    url = UrlFactory.create_url(FakeArgs())
    assert url != None

    url = UrlFactory.create_url(FakeArgs(date='05-2015'))
    test_url = 'https://www.smashingmagazine.com/2015/04/desktop-wallpaper-calendars-may-2015/'
    assert url == test_url

    url = UrlFactory.create_url(FakeArgs(date='01-2012'))
    test_url = 'https://www.smashingmagazine.com/2011/12/desktop-wallpaper-calendars-january-2012/'
    assert url == test_url


def test_dir_factory():
    dirname = DirFactory.new_name()
    test_dirname = '-'.join((str(datetime.date.today()),
                             DirFactory.default_postfix))
    assert dirname == test_dirname

    dirname = DirFactory.new_name(postfix='qwer', date='05-2012')
    test_dirname = '05-2012-qwer'
    assert dirname == test_dirname
