import pandas as pd
import requests
import numpy as np
import requests
import bs4
import json
from pymongo.errors import DuplicateKeyError, CollectionInvalid
from pymongo import MongoClient
import datetime as dt
import pandas as pd
from itertools import *

# For a single candidate, for example, Hillary Clinton

# Initiate Database and Collection for Articles
db = client['nyt_articles']
tab = db['table_hilary']
tab.insert({'hilary': 'test'})

# Initiate Table Database and Collection for Comments
db_comments = client['nyt_comments']
tab = db_comments['table_hilary']
db_comments.tab.insert({'hilary': 'test'})

# API Info
NYT_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
API_KEY = '74c73309c1052e6aa1785df7cd5cef8c:9:69947183'

# Query the NYT API once
def single_query(link, payload):
    '''
    INPUT URL, payload
    OUTPUT json 
    '''
    response = requests.get(link, params=payload)
    if response.status_code != 200:
        print 'WARNING', response.status_code
    else:
        return response.json()

# Determine if the results are more than 100 pages
def more_than_100_pages(total_page):
    if total_page > 100:
        pages_left = min(total_page - 100, 100)
        return 100, pages_left, True
    else:
        return total_page, 0, False

# Looping through the pages give the number of pages
def loop_through_pages(total_pages, link, payload, collection):
    for i in range(total_pages):
        if i % 50 == 0:
            print ' || Page ', i
        payload['page'] = str(i)
        content = single_query(link, payload)
        meta_lst = content['response']['docs']

        for meta in meta_lst:
            try:
                collection.insert(meta)
            except DuplicateKeyError:
                print 'DUPS!'


# Scrape the meta data (link to article and put it into Mongo)
def scrape_meta(days=1, search_term, collection):

    # The basic parameters for the NYT API
    link = NYT_URL
    payload = {'api-key': API_KEY, 'q' : search_term, 'sort': 'newest'}

    today = dt.datetime(2015, 9, 22)
    yesterday = dt.datetime(2003, 9, 22)
    
    for day in range(days):
        payload['end_date'] = today.strftime("%Y%m%d")
        yesterday = dt.date.today() - dt.timedelta(1)
        half_day = today - dt.timedelta(hours=12)
        payload['begin_date'] = yesterday.strftime("%Y%m%d")
        print payload
        print 'Scraping period: %s - %s ' % (str(yesterday), str(today))

        today -= dt.timedelta(days=2)
        
        content = single_query(link, payload)
        hits = content['response']['meta']['hits']
        total_pages = (hits / 10) + 1
        print 'HITS', hits

        newest_sort_pages, oldest_sort_pages, grt_100 = more_than_100_pages(total_pages)

        if grt_100:
            new_payload = payload.copy()
            old_payload = payload.copy()
            new_payload['sort']= 'newest'
            old_payload['sort'] = 'oldest'

        loop_through_pages(newest_sort_pages, link, new_payload, collection)
        loop_through_pages(oldest_sort_pages, link, old_payload, collection)

## Example search
search_terms = ['Hillary Cinton']
scrape_meta(days=1, search_terms, db.table_hilary)


# Retrieve article URLs from candidate's collection in the articles database
def get_links(collection):
    '''
    INPUT collection
    OUTPUT list
    '''
	links = collection.find({},{'web_url': 1, '_id' : 0})
	links_list = []
	for i in links:
	    link_list.append(str(i['web_url']))
    return links_list

links_list = get_links(db.table_hilary)

community_key = '603ff640088f24876c37e2857d83401f:1:73015248'

# Get comments from the Community API for each article URL
def get_comments(links_list, collection):
    '''
    INPUT list, collection (in the comments database)
    OUTPUT insertion into mongoDB
    '''
	for url in links_list:
    link = "http://api.nytimes.com/svc/community/v3/user-content/url.json?url=" + url
    payload = {'api-key': community_key}     
    content = single_query(link, payload)
    total = content['results']['totalCommentsFound'] 
    if total == 0:
        pass
    else:
        num_pages = list(np.arange(0, total, 25))  
        for i in num_pages:
            link = "http://api.nytimes.com/svc/community/v3/user-content/url.json?url=" + url
            payload = {'api-key': community_key, 'offset' : i}
            content = single_query(link, payload)
            
            # Insert each comment into mongoDB collection
            if len(content['results']['comments']) != 0: 
                for y in range(len(content['results']['comments'])): 
                    new_data = content['results']['comments'][y]
                    new_data['web_url'] = url
                    new_data['_id'] = content['results']['comments'][y]['commentID']
                    try:
                        collection.insert(new_data)
                    except DuplicateKeyError:
                        print 'Duplicate!'
                        pass
            else:
                pass

get_comments(links_list, db_comments.table_hilary)
