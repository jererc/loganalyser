from django.template import RequestContext
from django.shortcuts import render_to_response
import pymongo
import my_config


def home(request):
    #connect to the database
    connection = pymongo.Connection(my_config.mongodb_server)
    db = connection.test

    #format data before sending them to the template: {user: [EDGE_SENT, BYTES_SENT]; ...}
    users = {}
    for d in db.logs.find():
        if d['user_id'] not in users:
            users[d['user_id']] = [0, 0]
    for user in users:
        for d in db.logs.find({'user_id': user}):
            users[user][0] += d['EDGE_SENT']
            users[user][1] += d['O']
    
    return render_to_response('template.html', locals(), context_instance=RequestContext(request))