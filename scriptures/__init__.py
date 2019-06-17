from future import standard_library
standard_library.install_aliases()
import itertools
import json
import pkg_resources
import re
from memoize import memoize
from .structure import Structure
from urllib.parse import urlparse, parse_qs

FORMAT_LONG = 0
FORMAT_MEDIUM = 1
FORMAT_SHORT = 2


def ref(uri, validate_verses=True):
    return ScriptureRef(uri, validate_verses=validate_verses)


@memoize
def load_language_definition(lang):
    try:
        return json.loads(pkg_resources.resource_string(__name__, 'data/{}.json'.format(lang)).decode('utf-8'))
    except:
        if lang != 'eng':
            return load_language_definition('eng')
        return None


def format(ref_or_refs, lang='eng', include_book=True, book_format=FORMAT_LONG, formatter=None):
    language = load_language_definition(lang)

    if isinstance(ref_or_refs, ScriptureRef):
        ref = ref_or_refs

        def format_title(book_format, long_title, short_title):
            if short_title:
                if book_format == FORMAT_MEDIUM and len(short_title) / len(long_title) <= 0.25:
                    return short_title
                if book_format == FORMAT_SHORT:
                    return short_title
            return long_title

        # See if it's a testament
        if ref.testament and not ref.book:
            response = language['testaments'][ref.testament]['title']
        else:
            # Get the book
            language_book = language['testaments'][ref.testament]['books'][ref.book]

            # Format the ref
            if ref.chapter:
                if 'chapters' in language_book and str(ref.chapter) in language_book['chapters']:
                    language_chapter = language_book['chapters'][str(ref.chapter)]
                    response = format_title(book_format,
                                            language_chapter['title'],
                                            language_chapter.get('shortTitle'))
                else:
                    book = format_title(book_format,
                                        language_book.get('singularTitle', language_book['title']),
                                        language_book.get('singularShortTitle', language_book.get('shortTitle')))

                    response = book + ' ' if include_book else ''
                    if type(ref.chapter) is tuple:
                        response += u'{}\u2013{}'.format(ref.chapter[0], ref.chapter[1])
                    else:
                        response += str(ref.chapter)
                    if ref.verse_ranges:
                        response += ':' + ', '.join(str(x[0]) if x[0] == x[1] else u'{}\u2013{}'.format(x[0], x[1]) for x in ref.verse_ranges) if ref.verse_ranges else None

                    if ref.parens:
                        response += ' (%s)' % (str(ref.parens[0]) if ref.parens[0] == ref.parens[1] else u'{}\u2013{}'.format(ref.parens[0], ref.parens[1])) if ref.parens else None

            else:
                book = format_title(book_format,
                                    language_book['title'],
                                    language_book.get('shortTitle'))
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


@memoize
def load_structure():
    return Structure().structure


class ScriptureRef(object):
    SCRIPTURE_URI_REGEX = re.compile(r'''
        ^/scriptures
        /([^/]+)                      # testament
        /?([^/]+)?                    # book (optional)
        (?:/(\d+(-(\d+))?)            # chapter with optional range
            (?:\.(
                \d+(?:-\d+)?          # verse or verse range
                (?:,\d+(?:-\d+)?)*    # zero or more discontiguous verses and/or verse ranges
            ))?
        )?
        (\((?P<parens>.+?)\))?        # optional parentheses
        $
    ''', re.VERBOSE)

    GOSPEL_LIBRARY_URL_PATH_REGEX = re.compile(r'''
        ^/scriptures
        /([^/]+)                      # testament
        /?([^/]+)?                    # book (optional)
        (?:/(\d+(-(\d+))?))?          # chapter with optional range
        $
    ''', re.VERBOSE)

    def __init__(self, uri=None, gospel_library_url=None, testament=None, book=None, chapter=None, verse_ranges=None, parens=None, validate_verses=True):
        self.structure = load_structure()

        if uri:
            match = ScriptureRef.SCRIPTURE_URI_REGEX.match(uri)
            if match:
                testament = match.group(1)
                book = match.group(2)

                if match.group(3):
                    chapter_range_parts = match.group(3).split('-')
                    if len(chapter_range_parts) == 1:
                        chapter = int(chapter_range_parts[0])
                    else:
                        chapter = (int(chapter_range_parts[0]), int(chapter_range_parts[1]))
                        if chapter[0] == chapter[1]:
                            raise ValueError('range in chapter_ranges is invalid')

                    if match.group(6):
                        # Verse ranges (including those consisting of a single verse) are stored as a list of pairs
                        verse_ranges = []

                        previous_stop = 0
                        for verse_range in match.group(6).split(','):
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

        elif gospel_library_url:
            result = urlparse(gospel_library_url)
            if result.scheme != 'gospellibrary':
                raise ValueError('scheme is invalid')

            if result.netloc != 'content':
                raise ValueError('path is invalid')

            match = ScriptureRef.GOSPEL_LIBRARY_URL_PATH_REGEX.match(result.path)
            if match:
                testament = match.group(1)
                book = match.group(2)

                if match.group(3):
                    chapter_range_parts = match.group(3).split('-')
                    if len(chapter_range_parts) == 1:
                        chapter = int(chapter_range_parts[0])
                    else:
                        chapter = (int(chapter_range_parts[0]), int(chapter_range_parts[1]))
                        if chapter[0] == chapter[1]:
                            raise ValueError('range in chapter_ranges is invalid')

                    params = parse_qs(result.query)
                    if 'verse' in params:
                        verse = params['verse'][0]

                        # Verse ranges (including those consisting of a single verse) are stored as a list of pairs
                        verse_ranges = []

                        for verse_range in verse.split(','):
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

                    if 'context' in params:
                        context = params['context'][0]

                        # Paren ranges (including those consisting of a single verse) are stored as a list of pairs
                        parens = []

                        parens_range_parts = context.split('-')
                        if len(parens_range_parts) == 1:
                            start = int(parens_range_parts[0])
                            stop = start
                        else:
                            start = int(parens_range_parts[0])
                            stop = int(parens_range_parts[1])
                            if stop == start:
                                raise ValueError('range in parens_ranges is invalid')

                        parens = (start, stop)

        if testament:
            # Get the testament
            self.testament = testament
            testament_structure = next((x for x in self.structure['testaments'] if x['name'] == self.testament), None)
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
                self.chapter = chapter
                if type(self.chapter) is tuple:
                    start = self.chapter[0]
                    stop = self.chapter[1]
                    if stop < start:
                        raise ValueError('range in chapter_ranges is invalid')
                    if stop > len(book_structure['chapters']):
                        raise ValueError('range in chapter_ranges is not valid for chapter')
                else:
                    # Single chapter
                    # Get the chapter
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
                        if validate_verses and stop > chapter_structure['verses']:
                            raise ValueError('range in verse_ranges is not valid for chapter')

                        previous_stop = stop

            self.parens = None
            if parens:
                self.parens = parens

                # Validate the verse ranges
                start, stop = self.parens
                if stop < start:
                    raise ValueError('range in parens is invalid')

                if validate_verses and stop > chapter_structure['verses']:
                    raise ValueError('range in parens is not valid for chapter')
        else:
            if uri is not None:
                raise ValueError('uri is not a valid scripture ref')
            elif gospel_library_url is not None:
                raise ValueError('gospel_library_url is not a valid scripture URL')
            else:
                raise TypeError('missing required argument')

    def uri(self):
        uri = '/scriptures'
        if self.testament:
            uri += '/' + self.testament
            if self.book:
                uri += '/' + self.book
                if self.chapter:
                    if type(self.chapter) is tuple:
                        uri += '/{}-{}'.format(self.chapter[0], self.chapter[1])
                    else:
                        uri += '/' + str(self.chapter)
                    if self.verse_ranges:
                        uri += '.' + ','.join(str(x[0]) if x[0] == x[1] else '{}-{}'.format(x[0], x[1]) for x in self.verse_ranges)
                    if self.parens:
                        uri += '(%s)' % (str(self.parens[0]) if self.parens[0] == self.parens[1] else '{}-{}'.format(self.parens[0], self.parens[1]))
        return uri

    def website_url(self, lang=None):
        url = 'https://www.lds.org/scriptures'
        if self.testament:
            url += '/' + self.testament
            if self.book:
                url += '/' + self.book
                if self.chapter:
                    if type(self.chapter) is tuple:
                        url += '/{}-{}'.format(self.chapter[0], self.chapter[1])
                        if lang is not None:
                            url += '?lang={}'.format(lang)
                    else:
                        url += '/' + str(self.chapter)
                        if self.verse_ranges:
                            url += '.' + ','.join(str(x[0]) if x[0] == x[1] else '{}-{}'.format(x[0], x[1]) for x in self.verse_ranges)
                        if self.parens:
                            url += '(%s)' % (str(self.parens[0]) if self.parens[0] == self.parens[1] else '{}-{}'.format(self.parens[0], self.parens[1]))
                        if lang is not None:
                            url += '?lang={}'.format(lang)
                        if self.verse_ranges:
                            first_verse = self.verse_ranges[0][0]
                            url += '#{}'.format(first_verse - 1 if first_verse > 1 else 'primary')
        return url

    def universal_url(self, lang=None):
        url = 'https://www.churchofjesuschrist.org/study/scriptures'
        if self.testament:
            url += '/' + self.testament
            if self.book:
                url += '/' + self.book
                if self.chapter:
                    if type(self.chapter) is tuple:
                        url += '/{}-{}'.format(self.chapter[0], self.chapter[1])
                        if lang is not None:
                            url += '?lang={}'.format(lang)
                    else:
                        url += '/' + str(self.chapter)
                        if self.verse_ranges or self.parens or lang is not None:
                            parameters = []
                            if self.verse_ranges:
                                id_parameter = 'id=' + ','.join(('p' + str(x[0])) if x[0] == x[1] else 'p{}-p{}'.format(x[0], x[1]) for x in self.verse_ranges)
                                parameters.append(id_parameter)
                            if self.parens:
                                context_parameter = 'context=' + (('p' + str(self.parens[0])) if self.parens[0] == self.parens[1] else 'p{}-p{}'.format(self.parens[0], self.parens[1]))
                                parameters.append(context_parameter)
                            if lang is not None:
                                lang_parameter = 'lang={}'.format(lang)
                                parameters.append(lang_parameter)
                            url += '?' + '&'.join(parameters)
                        if self.verse_ranges:
                            first_verse = self.verse_ranges[0][0]
                            url += '#p{}'.format(first_verse)
        return url

    def gospel_library_url(self):
        url = 'gospellibrary://content/scriptures'
        if self.testament:
            url += '/' + self.testament
            if self.book:
                url += '/' + self.book
                if self.chapter:
                    if type(self.chapter) is tuple:
                        url += '/{}-{}'.format(self.chapter[0], self.chapter[1])
                    else:
                        url += '/{}'.format(self.chapter)

                    params = {}
                    if self.verse_ranges:
                        params['verse'] = ','.join(
                            str(x[0]) if x[0] == x[1] else '{}-{}'.format(x[0], x[1]) for x in self.verse_ranges)
                    if self.parens:
                        params['context'] = (
                            str(self.parens[0]) if self.parens[0] == self.parens[1] else '{}-{}'.format(self.parens[0], self.parens[1]))
                    if params:
                        url += '?' + '&'.join(['{}={}'.format(key, value) for (key, value) in params.items()])

                    if self.verse_ranges:
                        url += '#p' + str(self.verse_ranges[0][0])
        return url

    def url_path(self):
        path = '/scriptures'
        if self.testament:
            path += '/' + self.testament
            if self.book:
                path += '/' + self.book
                if self.chapter:
                    if type(self.chapter) is tuple:
                        path += '/{}.html'.format(self.chapter[0])
                    else:
                        path += '/{}.html'.format(self.chapter)

                    params = {}
                    if self.verse_ranges:
                        params['verse'] = ','.join(str(x[0]) if x[0] == x[1] else '{}-{}'.format(x[0], x[1]) for x in self.verse_ranges)
                    if self.parens:
                        params['context'] = (str(self.parens[0]) if self.parens[0] == self.parens[1] else '{}-{}'.format(self.parens[0], self.parens[1]))
                    if params:
                        path += '?' + '&'.join(['{}={}'.format(key, value) for (key, value) in params.items()])

                    if self.verse_ranges:
                        path += '#p' + str(self.verse_ranges[0][0])
        return path

    def __repr__(self):
        return 'ScriptureRef("{}")'.format(self.uri())

    def __str__(self):
        return format(self)

    def __unicode__(self):
        return format(self)

    def __lt__(self, other):
        self_testament_index, self_testament_structure = next(((i, x) for i, x in enumerate(self.structure['testaments']) if x['name'] == self.testament), -1)
        self_book_index, self_book_structure = next(((i, x) for i, x in enumerate(self_testament_structure['books']) if x['name'] == self.book), -1)

        other_testament_index, other_testament_structure = next(((i, x) for i, x in enumerate(self.structure['testaments']) if x['name'] == other.testament), -1)
        other_book_index, other_book_structure = next(((i, x) for i, x in enumerate(other_testament_structure['books']) if x['name'] == other.book), -1)

        self_first_verse_range_start = self.verse_ranges[0][0] if self.verse_ranges else -1
        self_first_verse_range_stop = self.verse_ranges[0][1] if self.verse_ranges else -1

        other_first_verse_range_start = other.verse_ranges[0][0] if other.verse_ranges else -1
        other_first_verse_range_stop = other.verse_ranges[0][1] if other.verse_ranges else -1

        return ((self_testament_index, self_book_index, self.chapter or -1, self_first_verse_range_start, self_first_verse_range_stop) <
                (other_testament_index, other_book_index, other.chapter or -1, other_first_verse_range_start, other_first_verse_range_stop))

    def __eq__(self, other):
        self_testament_index, self_testament_structure = next(((i, x) for i, x in enumerate(self.structure['testaments']) if x['name'] == self.testament), -1)
        self_book_index, self_book_structure = next(((i, x) for i, x in enumerate(self_testament_structure['books']) if x['name'] == self.book), -1)

        other_testament_index, other_testament_structure = next(((i, x) for i, x in enumerate(self.structure['testaments']) if x['name'] == other.testament), -1)
        other_book_index, other_book_structure = next(((i, x) for i, x in enumerate(other_testament_structure['books']) if x['name'] == other.book), -1)

        self_first_verse_range_start = self.verse_ranges[0][0] if self.verse_ranges else -1
        self_first_verse_range_stop = self.verse_ranges[0][1] if self.verse_ranges else -1

        other_first_verse_range_start = other.verse_ranges[0][0] if other.verse_ranges else -1
        other_first_verse_range_stop = other.verse_ranges[0][1] if other.verse_ranges else -1

        return ((self_testament_index, self_book_index, self.chapter or -1, self_first_verse_range_start, self_first_verse_range_stop) ==
                (other_testament_index, other_book_index, other.chapter or -1, other_first_verse_range_start, other_first_verse_range_stop))

    def merged(self, other):
        if self.testament != other.testament or self.book != other.book or (self.chapter != other.chapter and self.chapter and other.chapter):
            raise ValueError('scripture refs cannot be merged')

        testament = self.testament
        book = self.book
        chapter = None if self.chapter != other.chapter else self.chapter

        verse_ranges = None
        if self.verse_ranges and other.verse_ranges:
            verses = set(itertools.chain.from_iterable(list(range(start, stop + 1)) for start, stop in itertools.chain(self.verse_ranges, other.verse_ranges)))
            if len(verses) > 0:
                verse_ranges = list(ranges(sorted(verses)))

        return ScriptureRef(testament=testament, book=book, chapter=chapter, verse_ranges=verse_ranges)

    def chapters(self):
        testament_structure = next((x for x in self.structure['testaments'] if x['name'] == self.testament), None)
        book_structure = next((x for x in testament_structure['books'] if x['name'] == self.book), None)

        if not self.chapter:
            return list(range(1, len(book_structure['chapters']) + 1))

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
            testament_structure = next((x for x in self.structure['testaments'] if x['name'] == self.testament), None)
            book_structure = next((x for x in testament_structure['books'] if x['name'] == self.book), None)
            chapter_structure = book_structure['chapters'][self.chapter - 1]
            return list(range(1, chapter_structure['verses'] + 1))

        return sorted(set(itertools.chain.from_iterable(list(range(start, stop + 1)) for start, stop in self.verse_ranges)))


def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda range: range[1] - range[0]):
        b = list(b)
        yield b[0][1], b[-1][1]
