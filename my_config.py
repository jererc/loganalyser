import re

PATH_LOG = '/home/je/Desktop/log/'
RE_LOG_LINE = re.compile(r'(?P<date_time>.*?)\|.*?\|(?P<url>.*?)\|.*?\|(?P<bytes_sent>.*?)\|.*?\|(?P<edge_duration>.*?)\|(?P<edge_start>.*?)\|(?P<edge_sent>.*?)\|(?P<country_code>.*?)\|.*?\|(?P<user_agent>.*)', re.I)
RE_REQUEST_PATH = re.compile(r'/(?P<user_id>.*?)/(?P<media_id>.*?)/(?P<asset_name>.*?)(\-.*?)?\..*?\?.*', re.I)
MONGODB_SERVER = '127.0.0.1'
MONGODB_LOGS_COLLECTION = 'apache2_logs'
MONGODB_STATS_COLLECTION = 'apache2_stats'
EXCLUSIONS_USER_AGENT = [
    'check_http/v1.4.13 (nagios-plugins 1.4.13)',
]
STATS_TIME_DELTA = [24, 24*7, 24*30, 24*365] #time delta for stats, in hours
