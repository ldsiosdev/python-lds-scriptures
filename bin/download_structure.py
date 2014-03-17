#!/usr/bin/env python

import bs4
import json
import os
import re
import plistlib
import requests
from StringIO import StringIO
import tempfile
import zipfile

SCHEMA_VERSION = 2
CDN_URL = 'http://broadcast3.lds.org/crowdsource/Mobile/GospelStudy/production/v1'

ITEM_URIS = [
    '/scriptures/ot',
    '/scriptures/nt',
    '/scriptures/bofm',
    '/scriptures/dc-testament',
    '/scriptures/pgp',
]

testaments_data = []

print 'Getting the current schema {} catalog version...'.format(SCHEMA_VERSION)
index_url = '{}/schemas/{}/index.json'.format(CDN_URL, SCHEMA_VERSION)
r = requests.get(index_url)
if r.status_code != 200:
    print r.text
else:
    index = r.json()
    catalog_version = index['catalogVersion']

    print 'Getting catalog {}...'.format(catalog_version)
    catalog_url = '{}/catalog/{}.xml'.format(CDN_URL, SCHEMA_VERSION)
    r = requests.get(catalog_url)
    if r.status_code != 200:
        print r.text
    else:
        catalog = plistlib.readPlistFromString(r.content)
        
        for item_uri in ITEM_URIS:
            item = [item for item in catalog['items'] if item['uri'] == item_uri and item['languageCode'] == '000'][0]
            
            item_id = item['itemID']
            item_version = item['version']
            
            print 'Getting item {}...'.format(item_uri)
            item_zip_url = '{}/content/{}/{}.zip'.format(CDN_URL, item_id, item_version)
            r = requests.get(item_zip_url)
            if r.status_code != 200:
                print r.text
            else:
                item_package_path = tempfile.mkdtemp()
                with zipfile.ZipFile(StringIO(r.content), 'r') as zip_file:
                    zip_file.extractall(item_package_path)
                
                item_xml_path = '%s/%s/item.xml' % (item_package_path, item_id,)
                item_doc = bs4.BeautifulSoup(open(item_xml_path))
                
                for testament in item_doc.find_all('div', type='testament', uri=True):
                    testament_name = os.path.basename(testament['uri'])
                    
                    books_data = []
                    testament_data = dict(
                        name=testament_name,
                        books=books_data,
                    )
                    testaments_data.append(testament_data)
                
                    for book in testament.find_all('div', type='book', uri=True):
                        book_name = os.path.basename(book['uri'])
                    
                        chapters_data = []
                        book_data = dict(
                            name=book_name,
                            chapters=chapters_data,
                        )
                        books_data.append(book_data)
                
                        for chapter in book.find_all('div', type='chapter', uri=True):
                            if re.match(r'^/scriptures/[^/]+/[^/]+/\d+$', chapter['uri']):
                                verses = len(chapter.find_all('p', class_='verse', uri=True))
                                
                                chapter_data = dict(
                                    verses=verses,
                                )
                                chapters_data.append(chapter_data)
                            
                                
                                
structure_data = dict(testaments=testaments_data)
print json.dumps(structure_data, sort_keys=True, indent=4, separators=(',', ': '))
