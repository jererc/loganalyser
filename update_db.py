#!/usr/bin/env python

import os
import os.path
import re
import gzip
import pymongo
import datetime
import my_config


def convert_data(d):
    """Convert date_time string into datetime object, digit strings into integers, edge_* values into seconds"""
    d['date_time'] = datetime.datetime.strptime(d['date_time'], '%Y-%m-%d %H:%M:%S')
    for k in d.keys():
        if k in ['bytes_sent', 'edge_duration', 'edge_start', 'edge_sent']:
            try:
                d[k] = int(d[k])
            except:
                d[k] = 0
        if k in ['edge_duration', 'edge_start', 'edge_sent']:
            d[k] /= 1000
    return d


def main():
    #connect to the database and prepare the collection
    connection = pymongo.Connection(my_config.MONGODB_SERVER)
    db = connection.test
    collection = pymongo.collection.Collection(db, my_config.MONGODB_COLLECTION)
    
    #browse the logs path, and read each file
    entries_added = 0
    for filename in os.listdir(my_config.PATH_LOG):
        filename = os.path.join(my_config.PATH_LOG, filename)
        f = gzip.open(filename)
        print 'reading %s...'%filename
        for line in f:
            #grab the values from the log line, and convert them into a dict
            log_line = my_config.RE_LOG_LINE.match(line).groupdict()
            if log_line['user_agent'] not in my_config.EXCLUSIONS_USER_AGENT:
                #grab the url path values and add them to the log dict
                try:
                    request_path = my_config.RE_REQUEST_PATH.match(log_line['url']).groupdict()
                except AttributeError:
                    continue
                log_line.update(request_path)
                #add the raw log line to the dict for reference
                log_line['raw'] = line
                log_line = convert_data(log_line)
                
                #update the database, check if the log line already exists in the db
                if not collection.find({'raw': log_line['raw']}).count():
                    collection.insert(log_line)
                    entries_added += 1
        f.close()
    
    print 'added %s entries to the database'%entries_added


if __name__=='__main__':
    main()
