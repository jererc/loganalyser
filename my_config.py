import re

PATH_LOG = '/home/je/Desktop/log/'
RE_LOG_LINE = re.compile(r'(?P<t>.*?)\|(?P<h>.*?)\|(?P<Uq>.*?)\|(?P<s>.*?)\|(?P<O>.*?)\|(?P<D>.*?)\|(?P<EDGE_DURATION>.*?)\|(?P<EDGE_START>.*?)\|(?P<EDGE_SENT>.*?)\|(?P<XGEOIP_COUNTRY_CODE2>.*?)\|(?P<Referer>.*?)\|(?P<User_agent>.*)', re.I)
RE_REQUEST_PATH = re.compile(r'/(?P<user_id>.*?)/(?P<media_id>.*?)/(?P<asset_name>.*?)(\-(?P<timestamp>.*?))?\.(?P<extension>.*?)\?(?P<query_string>.*)', re.I)
MONGODB_SERVER = '127.0.0.1'
MONGODB_COLLECTION = 'apache2_logs'
EXCLUSIONS_USER_AGENT = [
    'check_http/v1.4.13 (nagios-plugins 1.4.13)',
]
