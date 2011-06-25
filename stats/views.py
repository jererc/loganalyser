from django.template import RequestContext
from django.shortcuts import render_to_response
import pymongo
import my_config


def home(request):
    time_delta = my_config.STATS_TIME_DELTA
    
    try:
        #grab the post values from the form
        stats_type = request.POST['stats_type']
        stats_time = request.POST['stats_time']
    except:
        return render_to_response('base.html', locals(), context_instance=RequestContext(request))
    else:
        #connect to the database
        connection = pymongo.Connection(my_config.MONGODB_SERVER)
        db = connection.test
        collection = pymongo.collection.Collection(db, my_config.MONGODB_STATS_COLLECTION)

        #find the databse document according to the stats type and time from the form
        document = collection.find_one({'stats_type': stats_type, 'stats_time': int(stats_time)})
        if document:
            stats = document['stats']
        else:
            stats = []
        
        return render_to_response('content.html', locals(), context_instance=RequestContext(request))
