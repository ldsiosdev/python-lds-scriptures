import itertools
import json
import pkg_resources
import re

FORMAT_LONG = 0
FORMAT_SHORT = 1

STRUCTURE = json.loads(pkg_resources.resource_string(__name__, 'data/structure.json'))

def ref(uri):
    return ScriptureRef(uri)

def format(ref_or_refs, lang='eng', include_book=True, book_format=FORMAT_LONG, formatter=None):
    # Load the language definition
    try:
        language = json.loads(pkg_resources.resource_string(__name__, 'data/{}.json'.format(lang)))
    except:
        language = json.loads(pkg_resources.resource_string(__name__, 'data/{}.json'.format('eng')))

    if isinstance(ref_or_refs, ScriptureRef):
        ref = ref_or_refs

        # See if it's a testament
        if ref.testament and not ref.book:
            response = language['testaments'][ref.testament]['title']
        else:
            # Get the book
            language_book = language['testaments'][ref.testament]['books'][ref.book]
            book = language_book['title']
            if book_format == FORMAT_SHORT and 'shortTitle' in language_book:
                book = language_book['shortTitle']

            # Format the ref
            if ref.chapter:
                if 'chapters' in language_book and str(ref.chapter) in language_book['chapters']:
                    language_chapter = language_book['chapters'][str(ref.chapter)]
                    chapter = language_chapter['title']
                    if book_format == FORMAT_SHORT and 'shortTitle' in language_chapter:
                        chapter = language_chapter['shortTitle']

                    response = chapter
                else:
                    if book_format == FORMAT_LONG and 'singularTitle' in language_book:
                        book = language_book['singularTitle']

                    response = book if include_book else ''
                    if response:
                        response += ' '
                    response += str(ref.chapter)
                    if ref.verse_ranges:
                        response += ':' + ', '.join(str(x[0]) if x[0] == x[1] else u'{}\u2013{}'.format(x[0], x[1]) for x in ref.verse_ranges) if ref.verse_ranges else None

                    if ref.parens:
                        response += ' (%s)' % (str(ref.parens[0]) if ref.parens[0] == ref.parens[1] else u'{}\u2013{}'.format(ref.parens[0], ref.parens[1])) if ref.parens else None

            else:
                response = book if include_book else ''

        if formatter is not None:
            return formatter(response, ref)
        else:
            return response
    else:
        # It's a list of references
        refs = merged(ref_or_refs)

        response = ''

        prev_book = None
        pending_chapter_range = None
        for ref in refs:
            if prev_book == ref.book and not ref.verse_ranges and pending_chapter_range and pending_chapter_range[1] == ref.chapter - 1:
                pending_chapter_range = (pending_chapter_range[0], ref.chapter)
            else:
                if pending_chapter_range:
                    if pending_chapter_range[0] != pending_chapter_range[1]:
                        response += u'\u2013{}'.format(pending_chapter_range[1])
                    pending_chapter_range = None

                if response:
                    response += '; '
                response += format(ref, lang=lang, include_book=(prev_book != ref.book), book_format=book_format, formatter=formatter)

                prev_book = ref.book
                if ref.chapter and not ref.verse_ranges:
                    pending_chapter_range = (ref.chapter, ref.chapter)

        if pending_chapter_range and pending_chapter_range[0] != pending_chapter_range[1]:
            response += u'\u2013{}'.format(pending_chapter_range[1])

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
        /?([^/]+)?                    # book (optional)
        (?:/(\d+)                     # chapter
            (?:\.(
                \d+(?:-\d+)?          # verse or verse range
                (?:,\d+(?:-\d+)?)*    # zero or more discontiguous verses and/or verse ranges
            ))?
        )?
        (\((?P<parens>.+?)\))?        # optional parentheses
        $
    ''', re.VERBOSE)

    def __init__(self, uri=None, testament=None, book=None, chapter=None, verse_ranges=None, parens=None):
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

                if match.group('parens'):
                    # Paren ranges (including those consisting of a single verse) are stored as a list of pairs
                    parens = []

                    previous_stop = 0
                    parens_range_parts = match.group('parens').split('-')
                    if len(parens_range_parts) == 1:
                        start = int(parens_range_parts[0])
                        stop = start
                    else:
                        start = int(parens_range_parts[0])
                        stop = int(parens_range_parts[1])
                        if stop == start:
                            raise ValueError('range in parens_ranges is invalid')

                    parens = (start, stop)
                    previous_stop = stop

        if testament:
            # Get the testament
            self.testament = testament
            testament_structure = next((x for x in STRUCTURE['testaments'] if x['name'] == self.testament), None)
            if not testament_structure:
                raise ValueError('testament is invalid')

            # Assume no book
            self.book = None

            if book is not None:
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

            self.parens = None
            if parens:
                self.parens = parens

                # Validate the verse ranges
                start, stop = self.parens
                if stop < start:
                    raise ValueError('range in parens is invalid')

                if stop > chapter_structure['verses']:
                    raise ValueError('range in parens is not valid for chapter')
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
                    if self.parens:
                        uri += '(%s)' % (str(self.parens[0]) if self.parens[0] == self.parens[1] else '{}-{}'.format(self.parens[0], self.parens[1])) if self.parens else None
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

    def chapters(self):
        testament_structure = next((x for x in STRUCTURE['testaments'] if x['name'] == self.testament), None)
        book_structure = next((x for x in testament_structure['books'] if x['name'] == self.book), None)

        if not self.chapter:
            return range(1, len(book_structure['chapters']) + 1)

        if not self.verse_ranges:
            return [ self.chapter ]

        chapter_structure = book_structure['chapters'][self.chapter - 1]
        if len(self.verses()) == chapter_structure['verses']:
            return [ self.chapter ]

        return []

    def verses(self):
        if not self.chapter:
            return []

        if not self.verse_ranges:
            testament_structure = next((x for x in STRUCTURE['testaments'] if x['name'] == self.testament), None)
            book_structure = next((x for x in testament_structure['books'] if x['name'] == self.book), None)
            chapter_structure = book_structure['chapters'][self.chapter - 1]
            return range(1, chapter_structure['verses'] + 1)

        return sorted(set(itertools.chain.from_iterable(range(start, stop + 1) for start, stop in self.verse_ranges)))

def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda (x, y): y - x):
        b = list(b)
        yield b[0][1], b[-1][1]
