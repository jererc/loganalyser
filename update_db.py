#!/usr/bin/env python

import os
import os.path
import re
import gzip
import pymongo
import datetime
import my_config


def convert_data(d):
    """Convert date/time strings into datetime objects, digit strings into integers, EDGE_* values into seconds"""
    for k in d.keys():
        if k == 't':
            d[k] = datetime.datetime.strptime(d[k], '%Y-%m-%d %H:%M:%S')
        if isinstance(d[k], str) and d[k].isdigit():
            d[k] = int(d[k])
        if k.startswith('EDGE_'):
            try:
                d[k] /= 1000
            except TypeError:
                d[k] = 0
    return d


def main():
    #connect to the database and prepare the collection
    connection = pymongo.Connection(my_config.MONGODB_SERVER)
    db = connection.test
    db.drop_collection(my_config.MONGODB_COLLECTION)
    collection = pymongo.collection.Collection(db, my_config.MONGODB_COLLECTION)
    
    #browse the logs path, and read each file
    entries_added = 0
    for filename in os.listdir(my_config.PATH_LOG):
        filename = os.path.join(my_config.PATH_LOG, filename)
        f = gzip.open(filename)
        print 'reading %s...'%filename
        for line in f:
            log_line = my_config.RE_LOG_LINE.match(line).groupdict()
            if log_line['User_agent'] not in my_config.EXCLUSIONS_USER_AGENT:
                try:
                    request_path = my_config.RE_REQUEST_PATH.match(log_line['Uq']).groupdict()
                except AttributeError:
                    continue
                log_line.update(request_path)
                log_line=convert_data(log_line)
                
                #update the database
                collection.insert(log_line)
                entries_added += 1

        f.close()

        break
    
    print 'added %s entries to the database'%entries_added


if __name__=='__main__':
    main()
