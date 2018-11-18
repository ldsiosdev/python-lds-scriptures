import json
import pkg_resources


class Testament(object):
    def __init__(self, uri):
        self.uri = uri

    def __eq__(self, other):
        if type(other) is type(self):
            return self.uri == other.uri
        return False


class Book(object):
    def __init__(self, uri):
        self.uri = uri

    def __eq__(self, other):
        if type(other) is type(self):
            return self.uri == other.uri
        return False


class Chapter(object):
    def __init__(self, uri, verse_count):
        self.uri = uri
        self.verse_count = verse_count

    def __eq__(self, other):
        if type(other) is type(self):
            return self.uri == other.uri and self.verse_count == other.verse_count
        return False


class Structure(object):
    def __init__(self):
        self.structure = json.loads(pkg_resources.resource_string(__name__, 'data/structure.json').decode('utf-8'))

        self._testaments = []
        self.books_by_testament_uri = {}
        self.chapters_by_book_uri = {}

        for raw_testament in self.structure['testaments']:
            testament = Testament(uri='/scriptures/' + raw_testament['name'])
            self._testaments.append(testament)

            self.books_by_testament_uri[testament.uri] = []
            for raw_book in raw_testament['books']:
                book = Book(uri=testament.uri + '/' + raw_book['name'])
                self.books_by_testament_uri[testament.uri].append(book)

                self.chapters_by_book_uri[book.uri] = []
                for i, raw_chapter in enumerate(raw_book['chapters']):
                    chapter = Chapter(uri=book.uri + '/' + str(i + 1), verse_count=raw_chapter["verses"])
                    self.chapters_by_book_uri[book.uri].append(chapter)

    def testaments(self):
        return self._testaments

    def books(self, testament):
        return self.books_by_testament_uri[testament.uri]

    def chapters(self, book):
        return self.chapters_by_book_uri[book.uri]
