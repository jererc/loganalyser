#!/usr/bin/env python

import os
import os.path
import re
import gzip
import pymongo
import my_config


def clean_data(d):
    """Convert digit strings to integers, convert EDGE_* values to seconds"""
    for v in d.keys():
        if d[v] != None and d[v].isdigit():
            d[v]=int(d[v])
        if v.startswith('EDGE_'):
            try:
                d[v] /= 1000
            except TypeError:
                d[v] = 0
    return d


def main():
    #connect to the database
    connection = pymongo.Connection(my_config.mongodb_server)
    db = connection.test
    db.drop_collection('logs')
    
    #browse the logs path, and read each file
    entries_added = 0
    for filename in os.listdir(my_config.path_log):
        filename = os.path.join(my_config.path_log, filename)
        f = gzip.open(filename)
        print 'reading %s...'%filename
        for line in f:
            log_line = my_config.re_log_line.match(line).groupdict()
            if log_line['User_agent'] not in my_config.exclusions_user_agent:
                try:
                    request_path = my_config.re_request_path.match(log_line['Uq']).groupdict()
                except AttributeError:
                    continue
                log_line.update(request_path)
                log_line=clean_data(log_line)

                #update the database
                db.logs.insert(log_line)
                entries_added += 1

        f.close()
    
    print 'added %s entries to the database'%entries_added


if __name__=='__main__':
    main()
