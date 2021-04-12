from datetime import datetime
from pprint import pprint
import mwclient

class Wiki:
    def __init__(self, username, password):
        self.site = mwclient.Site('imperiumab.investigace.cz', path='/')
        self.site.login(username, password)

    def upload_file(self, file, file_name, file_description):
        self.site.upload(file, filename=file_name, description=file_description)

def parse_wiki_date(wiki_date):
    datetime_obj = datetime.strptime(wiki_date, '1/%Y/%m/%d')

    return datetime_obj.date()

def format_wiki_str(val_str):
    if val_str is None:
        return ''

    return val_str
