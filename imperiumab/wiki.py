from datetime import datetime
from pprint import pprint
import mwclient


class Wiki:
    def __init__(self, username, password):
        self.site = mwclient.Site('imperiumab.investigace.cz', path='/')
        self.site.login(username, password)

        self.base_url = 'https://imperiumab.investigace.cz/wiki/'

    def upload_file(self, file, file_name, file_description):
        # ignore=True needed, because otherwise the upload will silently fail on any warning
        # from MediaWiki like that file already exists
        self.site.upload(file, filename=file_name, description=file_description, ignore=True)


def parse_wiki_date(wiki_date):
    datetime_obj = datetime.strptime(wiki_date, '1/%Y/%m/%d')

    return datetime_obj.date()


def format_wiki_str(val_str):
    if val_str is None:
        return ''

    return val_str
