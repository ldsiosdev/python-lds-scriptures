#!/usr/bin/env python

import argparse
import json
import re
import plistlib
from pysqlite2 import dbapi2 as sqlite3
import requests
from StringIO import StringIO
import tempfile
import zipfile

parser = argparse.ArgumentParser(description='Generate language definition with downloaded data.')
parser.add_argument('--lang', required=True)
parser.add_argument('--structure', dest='structure_path', required=True)
args = parser.parse_args()

SCHEMA_VERSION = 2
CDN_URL = 'http://broadcast3.lds.org/crowdsource/Mobile/GospelStudy/production/v1'

ITEM_URIS = [
    '/scriptures/ot',
    '/scriptures/nt',
    '/scriptures/bofm',
    '/scriptures/dc-testament',
    '/scriptures/pgp',
]

with open(args.structure_path, 'r') as f:
    structure = json.load(f)

testaments_data = dict()

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
            item = [item for item in catalog['items'] if item['uri'] == item_uri and item['languageCode'] == args.lang][0]
            
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
                
                package_sqlite_path = '{}/{}/package.sqlite'.format(item_package_path, item_id,)
                package_conn = sqlite3.connect(package_sqlite_path)
            
                for row in package_conn.execute('select ZURI, ZTITLE from ZNAVNODE order by ZURI'):
                    uri = row[0]
                    title = row[1]
                    
                    match = re.match(r'^/scriptures/([^/]+)(?:/([^/]+)(?:/\d+)?)?$', uri)
                    if match:
                        testament = match.group(1)
                        book = match.group(2)
                        
                        try:
                            testament_data = testaments_data[testament]
                        except:
                            testament_data = dict(books=dict())
                            testaments_data[testament] = testament_data
                            
                        if book:
                            testament_structure = next((x for x in structure['testaments'] if x['name'] == testament), None)
                            book_structure = next((x for x in testament_structure['books'] if x['name'] == book), None)
                            if book_structure:
                                if book not in testament_data['books']:
                                    testament_data['books'][book] = dict(title=title)
                        else:
                            testament_data['title'] = title
                

language_data = dict(testaments=testaments_data)
print json.dumps(language_data, sort_keys=True, indent=4, separators=(',', ': '))
