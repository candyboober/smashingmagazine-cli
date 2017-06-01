import datetime
import os
import sys

import consts


class UrlFactory(object):
    """
    class that create url for paraser by args
    that was got by argparse like argv(arguments of command line)
    """
    @classmethod
    def create_url(cls, args):
        date, year, month = cls._get_date(args)
        pub_year, pub_month = cls._get_pub_date(date)

        return consts.URL.format(
            pub_year=pub_year,
            pub_month=pub_month,
            month=consts.MONTHS[int(month) - 1],
            year=year
        )

    @classmethod
    def _get_date(cls, args):
        date = args.date
        if date:
            month, year = date.split('-')
            date = datetime.date(int(year), int(month), 1)
        else:
            date = datetime.date.today()
            month = date.month
            year = date.year
        return (date, year, month)

    @classmethod
    def _get_pub_date(cls, date):
        pub_date = date - datetime.timedelta(days=30)
        pub_year, pub_month, _ = str(pub_date).split('-')
        return pub_year, pub_month


class DirFactory(object):
    """
    Directory factory for store all images
    """
    default_postfix = 'smashingmagazine'

    @classmethod
    def make_dir(cls, postfix=None, date=None):
        dirname = cls.new_name(postfix, date)

        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        else:
            print('You already have directory with images')
            sys.exit()

        return dirname

    @classmethod
    def new_name(cls, postfix=None, date=None):
        postfix = postfix or cls.default_postfix
        if date:
            dirname = '-'.join((date, postfix))
        else:
            dirname = '-'.join((str(datetime.date.today()), postfix))
        return dirname
