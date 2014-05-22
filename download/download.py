import codecs
import requests
import json
import sys
import collections
import os

DESTINATION = 'data/{code}.json'

SOURCE_URL = 'https://script.google.com/macros/s/AKfycbw_hA5vXFZr2KuhZFe4msmq0x2_N9fmrk17f8w9EMtRuRAXxJOc/exec?sheet_id=0AuWQ-iCrlReTdE9YeVJhdFk0NW4zZlpRZTYtQzN3a2c&sheet_name=Scriptures'

# list(find_key(file_dict, 'title'))
# Used to make list of all values of 'title' keys (so we can assess completion)
def find_key(dictionary, key):
    for k, v in dictionary.iteritems():
        if isinstance(v, collections.Mapping):
            for inner_value in find_key(v, key):
                if inner_value != '':
                    yield inner_value
        else:
            if v != '':
                yield v

if __name__ == '__main__':
    print 'Loading book name spreadsheet data.'

    r = requests.get(SOURCE_URL)

    if r.ok:
        print 'Splitting out into individual files'

        data = r.json()

        exported_list = []
        incomplete_list = []

        for filename, file_dict in sorted(data.iteritems()):
            output_filename = DESTINATION.format(code=filename)

            # Check if translation is complete (length should be 184)
            compressed_list = list(find_key(file_dict, 'title'))
            if len(compressed_list) == 184:
                with codecs.open(output_filename, "wb", encoding='utf-8') as langFile:
                    output = json.dumps(file_dict, langFile, sort_keys=True, indent=4, separators=(',', ': '))

                    # Convert double backslashes back to single backslashes
                    langFile.write(output.replace("\\\\", "\\"))

                exported_list.append(filename)
            else:
                # Remove the file if it's there
                if os.path.exists(output_filename):
                    os.remove(output_filename)

                incomplete_list.append(filename)

        print 'Exported (%d): %s' % (len(exported_list), ', '.join(exported_list))
        print 'Incomplete (%d): %s' % (len(incomplete_list), ', '.join(incomplete_list))
