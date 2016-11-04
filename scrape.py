
# coding: utf-8
import argparse

parser = argparse.ArgumentParser(description='Download some images with a query')
parser.add_argument('--query', dest='query', 
                    help='Query to search.')
parser.add_argument('--n', dest='n', 
                    help='Number of items to return.')

args = parser.parse_args()

# In[1]:

import json
keys = json.loads(open('keys.json', 'r').read())
# keys


# In[68]:

from googleapiclient.discovery import build

def image_search (query, start=1):
    service = build("customsearch", "v1",
               developerKey=keys['developerKey'])
    return service.cse().list(
        q=query,
        filter="1", # filter duplicates
        start=start,
        cx=keys['cx'],
        searchType='image',
    ).execute()

def images_from (res):
    urls = [item['link'] for item in res['items']]
    return urls
    

# In[72]:

from time import sleep

def query_images (q, n=100):
    resList = []
    queried=0
    while(queried<n):
        res = image_search(q, queried+1)
        resList.append(res)
        queried+=10
        sleep(1)
    return resList



# In[74]:

#from io import BytesIO
import requests
#from PIL import Image

def load_image_bytes (url):
    return requests.get(url).content

#def load_image (bytes):
#    img = BytesIO(bytes)
#    return Image.open(img)

#img = img_urls[0]
#load_image(img)


# In[75]:

query_res = query_images(args.query)#, n=args.n)
url_lists = [images_from(res) for res in query_res]
img_urls = [url for url_list in url_lists for url in url_list]
print(img_urls)


# In[80]:

# query_res


# In[76]:

def filename (url):
    return url.split('/')[-1]

#filename(img_urls[0])


# In[79]:

from os import mkdir
from os.path import exists
from os.path import join
from datetime import datetime
from io import TextIOWrapper

if not exists(args.query):
    mkdir(args.query)
out_dir = join(args.query, 
              datetime.now().isoformat())
mkdir(out_dir)

for i, url in enumerate(img_urls):
    try:
        print(url)
        fn = str(i) + '_' + filename(url)
        path = join(out_dir, fn)
        print(path)
        img = load_image_bytes(url)
        print('downloaded')
        with open(path, 'wb') as f:
            f.write(img)
    except:
        print('something went wrong?')
    
path = join(out_dir, 'query-results.json')
with open (path, 'w') as f:
    f.write(json.dumps(query_res))
print('done', path)


# In[ ]:



