import codecs
import requests
import json
import sys

DESTINATION = 'data/{code}.json'

SOURCE_URL = 'https://script.google.com/macros/s/AKfycbw_hA5vXFZr2KuhZFe4msmq0x2_N9fmrk17f8w9EMtRuRAXxJOc/exec?sheet_id=0AuWQ-iCrlReTdE9YeVJhdFk0NW4zZlpRZTYtQzN3a2c&sheet_name=Scriptures'

if __name__ == '__main__':
    print 'Loading book name spreadsheet data.'

    r = requests.get(SOURCE_URL)

    if r.ok:
        print 'Splitting out into individual files'

        data = r.json()

        for filename, file_dict in sorted(data.iteritems()):
            with codecs.open(DESTINATION.format(code=filename), "wb", encoding='utf-8') as langFile:
                output = json.dumps(file_dict, langFile, sort_keys=True, indent=4, separators=(',', ': '))

                # Convert double backslashes back to single backslashes
                langFile.write(output.replace("\\\\", "\\"))
