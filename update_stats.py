#!/usr/bin/env python

import datetime
import pymongo
import my_config


def check_time_delta(date_time, delta_max):
    """Check the time delta between now and date_time. Takes a datetime object (date_time) and an integer (delta_max, in hours)."""
    delta = datetime.datetime.now() - date_time
    if delta.seconds / 60 <= delta_max:
        return True


def main():
    """Read the mongodb log collection and process different stats based on types and dates, then store them in a dedicated mongodb collection."""
    #connect to the database and prepare the collections
    connection = pymongo.Connection(my_config.MONGODB_SERVER)
    db = connection.test
    collection_logs = pymongo.collection.Collection(db, my_config.MONGODB_LOGS_COLLECTION)
    collection_stats = pymongo.collection.Collection(db, my_config.MONGODB_STATS_COLLECTION)

    #process stats for each time delta specified in the config file
    for time_delta in my_config.STATS_TIME_DELTA:

        #prepare the stats dicts
        users = {}
        countries = {}
        asset_names = {}
        for d in collection_logs.find():
            if check_time_delta(d['date_time'], time_delta):
                if d['user_id'] not in users:
                    users[d['user_id']] = [0, 0]
                if d['country_code'] not in countries:
                    countries[d['country_code']] = 0
                if d['asset_name'] not in asset_names:
                    asset_names[d['asset_name']] = 0
        
        #update the stats dicts
        print 'processing stats for a %s hours time delta'%time_delta
        total_entries = 0
        for d in collection_logs.find():
            if check_time_delta(d['date_time'], time_delta):
                total_entries += 1
                #update the stats dicts values
                users[d['user_id']][0] += d['edge_sent']
                users[d['user_id']][1] += d['bytes_sent']
                countries[d['country_code']] += 1
                asset_names[d['asset_name']] += 1
        #calculate percentages
        for i in countries:
            countries[i] = float(countries[i]) * 100 / total_entries
        for i in asset_names:
            asset_names[i] = float(asset_names[i]) * 100 / total_entries
        
        #convert the stats dicts into lists so that the view has the minimum to process
        stats = {
            'users': [['User ID', 'Total data sent (ko)', 'Total viewing time (seconds)']],
            'countries': [['Country', 'Request %']],
            'asset_names': [['Asset name', 'Request %']],
            }
        for user in users:
            stats['users'].append([user, users[user][0], users[user][1]])
        for country in countries:
            stats['countries'].append([country, countries[country]])
        for asset_name in asset_names:
            stats['asset_names'].append([asset_name, asset_names[asset_name]])
        
        #update the stats collection
        for t in ['users', 'countries', 'asset_names']:
            collection_stats.remove({'stats_type': t, 'stats_time': time_delta})
            collection_stats.insert({'stats_type': t, 'stats_time': time_delta, 'stats': stats[t]})


if __name__=='__main__':
    main()
