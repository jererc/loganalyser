from django.template import RequestContext
from django.shortcuts import render_to_response
import pymongo
import my_config


def home(request):
    #connect to the database
    connection = pymongo.Connection(my_config.MONGODB_SERVER)
    db = connection.test
    collection = pymongo.collection.Collection(db, my_config.MONGODB_COLLECTION)
    
    #format data before sending it to the template
    data = {
        'users': {},
        'countries': {},
        'asset_names': {},
        }
    users = {}
    countries = {}
    asset_names = {}
    db_query = collection.find()
    total_entries = db_query.count()
    for d in db_query:
        if d['user_id'] not in users:
            users[d['user_id']] = [0, 0]
        if d['country_code'] not in countries:
            countries[d['country_code']] = 0
        if d['asset_name'] not in asset_names:
            asset_names[d['asset_name']] = 0
    for user in users:
        for d in collection.find({'user_id': user}):
            users[user][0] += d['edge_sent']
            users[user][1] += d['bytes_sent']
    for country in countries:
        for d in collection.find({'country_code': country}):
            countries[country] += 1
        countries[country] = float(countries[country]) * 100 / total_entries
    for asset_name in asset_names:
        for d in collection.find({'asset_name': asset_name}):
            asset_names[asset_name] += 1
        asset_names[asset_name] = float(asset_names[asset_name]) * 100 / total_entries
    
    return render_to_response('base.html', locals(), context_instance=RequestContext(request))
