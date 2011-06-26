from django.template import RequestContext
from django.shortcuts import render_to_response
import pymongo
import my_config


def get_collection_keys(key, collection):
    """Get all keys available in the mongodb collection"""
    all_keys = {}
    for d in collection.find({key: {'$exists': True}}):
        if d[key] not in all_keys:
            all_keys[d[key]] = True
    return sorted(all_keys.keys())


def home(request):
    #connect to the database
    connection = pymongo.Connection(my_config.MONGODB_SERVER)
    db = connection.test
    collection = pymongo.collection.Collection(db, my_config.MONGODB_STATS_COLLECTION)
    
    #get the form select fields values
    stats_types = get_collection_keys('stats_type', collection)
    time_delta = my_config.STATS_TIME_DELTA
    
    try:
        #get the post values from the form
        stats_type = request.POST['stats_type']
        stats_time = request.POST['stats_time']
    except:
        return render_to_response('base.html', locals(), context_instance=RequestContext(request))
    else:
        #get the database document according to the stats type and time from the form
        document = collection.find_one({'stats_type': stats_type, 'stats_time': int(stats_time)})
        if document:
            stats = document['stats']
        else:
            stats = []

        return render_to_response('content.html', locals(), context_instance=RequestContext(request))
