import json
import pkg_resources
import re

STRUCTURE = json.loads(pkg_resources.resource_string(__name__, 'data/structure.json'))

def ref(uri):
    return ScriptureRef(uri)

def format(ref, lang='eng'):
    # Load the language definition
    try:
        language = json.loads(pkg_resources.resource_string(__name__, 'data/{}.json'.format(lang)))
    except:
        language = json.loads(pkg_resources.resource_string(__name__, 'data/{}.json'.format('eng')))
    
    # Get the book
    book = language['testaments'][ref.testament]['books'][ref.book]['title']
    
    # Format the ref
    response = book
    if ref.chapter:
        response += ' ' + str(ref.chapter)
        if ref.verse_ranges:
            response += ':' + ', '.join(str(x[0]) if x[0] == x[1] else u'{}\u2013{}'.format(x[0], x[1]) for x in ref.verse_ranges) if ref.verse_ranges else None
    return response

class ScriptureRef:
    SCRIPTURE_URI_REGEX = re.compile(r'''
        ^/scriptures
        /([^/]+)                      # testament
        /([^/]+)                      # book
        (?:/(\d+)                     # chapter
            (?:\.(
                \d+(?:-\d+)?          # verse or verse range
                (?:,\d+(?:-\d+)?)*    # zero or more discontiguous verses and/or verse ranges
            ))?
        )?
        $
    ''', re.VERBOSE)
    
    def __init__(self, uri):
        match = ScriptureRef.SCRIPTURE_URI_REGEX.match(uri)
        if match:
            # Get the testament
            self.testament = match.group(1)
            testament_structure = next((x for x in STRUCTURE['testaments'] if x['name'] == self.testament), None)
            if not testament_structure:
                raise ValueError('uri is not a valid scripture ref')
            
            # Get the book
            self.book = match.group(2)
            book_structure = next((x for x in testament_structure['books'] if x['name'] == self.book), None)
            if not book_structure:
                raise ValueError('uri is not a valid scripture ref')
            
            # Assume no chapter or verse ranges
            self.chapter = None
            self.verse_ranges = None
                
            if match.group(3):
                # Get the chapter
                self.chapter = int(match.group(3))
                if self.chapter <= 0:
                    raise ValueError('uri is not a valid scripture ref')
                try:
                    chapter_structure = book_structure['chapters'][self.chapter - 1]
                except:
                    raise ValueError('uri is not a valid scripture ref')
            
                if match.group(4):
                    # Verse ranges (including those consisting of a single verse) are stored as a list of pairs
                    self.verse_ranges = []
                    
                    # Get the verse ranges
                    previous_stop = 0
                    for verse_range in match.group(4).split(','):
                        verse_range_parts = verse_range.split('-')
                        if len(verse_range_parts) == 1:
                            start = int(verse_range_parts[0])
                            stop = start
                        else:
                            start = int(verse_range_parts[0])
                            stop = int(verse_range_parts[1])
                            if stop <= start:
                                raise ValueError('uri is not a valid scripture ref')
                            
                        if start <= previous_stop:
                            raise ValueError('uri is not a valid scripture ref')
                        if stop > chapter_structure['verses']:
                            raise ValueError('uri is not a valid scripture ref')
                        
                        self.verse_ranges.append((start, stop))
                        previous_stop = stop
        else:
            raise ValueError('uri is not a valid scripture ref')
        
    def uri(self):
        uri = '/scriptures'
        if self.testament:
            uri += '/' + self.testament
            if self.book:
                uri += '/' + self.book
                if self.chapter:
                    uri += '/' + str(self.chapter)
                    if self.verse_ranges:
                        uri += '.' + ','.join(str(x[0]) if x[0] == x[1] else '{}-{}'.format(x[0], x[1]) for x in self.verse_ranges) if self.verse_ranges else None
        return uri
            
    def __repr__(self):
        return 'ScriptureRef("{}")'.format(self.uri())
    
    def __unicode__(self):
        return format(self)
