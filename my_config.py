import re

path_log = '/home/je/Desktop/log/'
re_log_line = re.compile(r'(?P<t>.*?)\|(?P<h>.*?)\|(?P<Uq>.*?)\|(?P<s>.*?)\|(?P<O>.*?)\|(?P<D>.*?)\|(?P<EDGE_DURATION>.*?)\|(?P<EDGE_START>.*?)\|(?P<EDGE_SENT>.*?)\|(?P<XGEOIP_COUNTRY_CODE2>.*?)\|(?P<Referer>.*?)\|(?P<User_agent>.*)', re.I)
re_request_path = re.compile(r'/(?P<user_id>.*?)/(?P<media_id>.*?)/(?P<asset_name>.*?)(\-(?P<timestamp>.*?))?\.(?P<extension>.*?)\?(?P<query_string>.*)', re.I)
mongodb_server = '127.0.0.1'
mongodb_collection = 'logs'
exclusions_user_agent = [
    'check_http/v1.4.13 (nagios-plugins 1.4.13)',
]
