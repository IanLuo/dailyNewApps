import urllib2
import json
import constants
from django.shortcuts import render_to_response
from elementtree import ElementTree
from django.core.cache import cache,get_cache

def home(request):
    return render_to_response("home.html")

def get_new_apps(request):

    return render_to_response("result.html");

def get_app_list(request,list_type = "newapplications", genre = ""):
    entry_list = get_app_entries()

    sub_entries = list()

    for entry in get_app_entries():

        if list_type == "free":
            if entry['price'] == "Free" and (1 if (genre == '') else entry['genre_id'] == genre):
                sub_entries.append(entry)
        elif list_type == "paid":
            if entry['price'] != "Free" and (1 if (genre == '') else entry['genre_id'] == genre):
                sub_entries.append(entry)   
        else:
            if (1 if (genre == '') else entry['genre_id'] == genre):
                sub_entries.append(entry)

    return render_to_response('app_list.html',{"entries":sub_entries})


def get_app_entries(list_type = "newapplications", genre = ""):
    cache = get_cache(constants.CONST_CACHE_KEY)

    entry_list = cache.get(constants.CONST_CACHE_KEY_APP_ENTRY)
    
    if entry_list == None:
        url = creat_url(list_type,genre)
        
        print 'get url %s' % url
    
        result = urllib2.urlopen(url);
        entry_list = put_entries_into_cache(result,cache)
    else:
        print 'got %d app entry list from cache' % len(entry_list)
        
    return json.loads(entry_list)
    

def get_app_detail(request,app_id = None):
    cache = get_cache(constants.CONST_CACHE_KEY)
    
    data = cache.get(app_id)
    
    if data == None:
        detail = urllib2.urlopen('https://itunes.apple.com/lookup?id=' + app_id).read()
        data = json.loads(detail)
        
        cache.set(app_id,data,72000)
    else:
        print 'got data from cache for %s' % app_id

    return render_to_response('app_detail.html',{"data":data['results'][0]})

    
def put_entries_into_cache(xml_response,cache):
    xml_tree = ElementTree.parse(xml_response)
    entry_list = list()
    
    im_ns = '{http://itunes.apple.com/rss}'
    ns = '{http://www.w3.org/2005/Atom}'
    
    for element in xml_tree.getroot().getchildren():
        if element.tag[-5:] != 'entry':
            continue
        else:
            entry_list.append({"name":element.find(im_ns + "name").text,
                                "app_id":element.find(ns + "id").get(im_ns + 'id'),
                                "image":element.find(im_ns + "image").text,
                                "price":element.find(im_ns + "price").text,
                                "genre_id":element.find(ns + "category").get(im_ns + "id"),
                                "genre_name":element.find(ns + "category").get("term"),
                                })

    #put the 'today's apps into cache, and keep them for one hour, which means the list refresh each hour
    cache.set(constants.CONST_CACHE_KEY_APP_ENTRY, json.dumps(entry_list), 3600)

    return cache.get(constants.CONST_CACHE_KEY_APP_ENTRY)
    
def creat_url(list_type,genre):
    prefix = 'https://itunes.apple.com/us/rss/'
    surfix = '/xml'
    genre_str = '' if (len(genre) == 0) else "/genre=%s" % genre
    url = prefix + list_type + "/limit=10" + genre_str + surfix
    
    return url
    
    
    
    
    
    