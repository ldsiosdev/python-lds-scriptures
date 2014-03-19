import itertools
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

def merged(refs):
    merged_refs = []
    
    current_ref = None
    for ref in sorted(refs):
        if not current_ref:
            current_ref = ref
        else:
            try:
                current_ref = current_ref.merged(ref)
            except ValueError:
                merged_refs.append(current_ref)
                current_ref = ref
    
    if current_ref:
        merged_refs.append(current_ref)
    
    return merged_refs

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
    
    def __init__(self, uri=None, testament=None, book=None, chapter=None, verse_ranges=None):
        if uri:
            match = ScriptureRef.SCRIPTURE_URI_REGEX.match(uri)
            if match:
                testament = match.group(1)
                book = match.group(2)
                if match.group(3):
                    chapter = int(match.group(3))
                
                    if match.group(4):
                        # Verse ranges (including those consisting of a single verse) are stored as a list of pairs
                        verse_ranges = []
                        
                        previous_stop = 0
                        for verse_range in match.group(4).split(','):
                            verse_range_parts = verse_range.split('-')
                            if len(verse_range_parts) == 1:
                                start = int(verse_range_parts[0])
                                stop = start
                            else:
                                start = int(verse_range_parts[0])
                                stop = int(verse_range_parts[1])
                                if stop == start:
                                    raise ValueError('range in verse_ranges is invalid')
                            
                            verse_ranges.append((start, stop))
                            previous_stop = stop
        
        if testament:
            # Get the testament
            self.testament = testament
            testament_structure = next((x for x in STRUCTURE['testaments'] if x['name'] == self.testament), None)
            if not testament_structure:
                raise ValueError('testament is invalid')
            
            # Get the book
            self.book = book
            book_structure = next((x for x in testament_structure['books'] if x['name'] == self.book), None)
            if not book_structure:
                raise ValueError('book is not valid for testament')
            
            # Assume no chapter or verse ranges
            self.chapter = None
            self.verse_ranges = None
            
            if chapter is not None:
                # Get the chapter
                self.chapter = chapter
                if self.chapter <= 0:
                    raise ValueError('chapter is not valid for book')
                try:
                    chapter_structure = book_structure['chapters'][self.chapter - 1]
                except:
                    raise ValueError('chapter is not valid for book')
                
                if verse_ranges:
                    self.verse_ranges = verse_ranges
                    
                    # Validate the verse ranges
                    previous_stop = 0
                    for verse_range in self.verse_ranges:
                        start = verse_range[0]
                        stop = verse_range[1]
                        if stop < start:
                            raise ValueError('range in verse_ranges is invalid')
                            
                        if start <= previous_stop:
                            raise ValueError('range in verse_ranges is invalid')
                        if stop > chapter_structure['verses']:
                            raise ValueError('range in verse_ranges is not valid for chapter')
                        
                        previous_stop = stop
        else:
            if uri is not None:
                raise ValueError('uri is not a valid scripture ref')
            else:
                raise TypeError('missing required argument')
        
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
    
    def __lt__(self, other):
        self_testament_index, self_testament_structure = next(((i, x) for i, x in enumerate(STRUCTURE['testaments']) if x['name'] == self.testament), None)
        self_book_index, self_book_structure = next(((i, x) for i, x in enumerate(self_testament_structure['books']) if x['name'] == self.book), None)
            
        other_testament_index, other_testament_structure = next(((i, x) for i, x in enumerate(STRUCTURE['testaments']) if x['name'] == other.testament), None)
        other_book_index, other_book_structure = next(((i, x) for i, x in enumerate(other_testament_structure['books']) if x['name'] == other.book), None)
        
        self_first_verse_range_start = self.verse_ranges[0][0] if self.verse_ranges else None
        self_first_verse_range_stop = self.verse_ranges[0][1] if self.verse_ranges else None
        
        other_first_verse_range_start = other.verse_ranges[0][0] if other.verse_ranges else None
        other_first_verse_range_stop = other.verse_ranges[0][1] if other.verse_ranges else None
        
        return ((self_testament_index, self_book_index, self.chapter, self_first_verse_range_start, self_first_verse_range_stop) <
                (other_testament_index, other_book_index, other.chapter, other_first_verse_range_start, other_first_verse_range_stop))
    
    def __eq__(self, other):
        self_testament_index, self_testament_structure = next(((i, x) for i, x in enumerate(STRUCTURE['testaments']) if x['name'] == self.testament), None)
        self_book_index, self_book_structure = next(((i, x) for i, x in enumerate(self_testament_structure['books']) if x['name'] == self.book), None)
            
        other_testament_index, other_testament_structure = next(((i, x) for i, x in enumerate(STRUCTURE['testaments']) if x['name'] == other.testament), None)
        other_book_index, other_book_structure = next(((i, x) for i, x in enumerate(other_testament_structure['books']) if x['name'] == other.book), None)
        
        self_first_verse_range_start = self.verse_ranges[0][0] if self.verse_ranges else None
        self_first_verse_range_stop = self.verse_ranges[0][1] if self.verse_ranges else None
        
        other_first_verse_range_start = other.verse_ranges[0][0] if other.verse_ranges else None
        other_first_verse_range_stop = other.verse_ranges[0][1] if other.verse_ranges else None
        
        return ((self_testament_index, self_book_index, self.chapter, self_first_verse_range_start, self_first_verse_range_stop) ==
                (other_testament_index, other_book_index, other.chapter, other_first_verse_range_start, other_first_verse_range_stop))
        
    def merged(self, other):
        if self.testament != other.testament or self.book != other.book or (self.chapter != other.chapter and self.chapter and other.chapter):
            raise ValueError('scripture refs cannot be merged')
        
        testament = self.testament
        book = self.book
        chapter = None if self.chapter != other.chapter else self.chapter
        
        verse_ranges = None
        if self.verse_ranges and other.verse_ranges:
            verses = set(itertools.chain.from_iterable(range(start, stop + 1) for start, stop in itertools.chain(self.verse_ranges, other.verse_ranges)))
            if len(verses) > 0:
                verse_ranges = list(ranges(sorted(verses)))
        
        return ScriptureRef(testament=testament, book=book, chapter=chapter, verse_ranges=verse_ranges)

def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda (x, y): y - x):
        b = list(b)
        yield b[0][1], b[-1][1]
