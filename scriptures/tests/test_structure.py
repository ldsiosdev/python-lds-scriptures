import unittest
from scriptures.structure import Structure, Testament, Book, Chapter


class TestStructure(unittest.TestCase):
    def test_testaments(self):
        self.assertEqual(Structure().testaments(), [
            Testament(uri='/scriptures/ot'),
            Testament(uri='/scriptures/nt'),
            Testament(uri='/scriptures/bofm'),
            Testament(uri='/scriptures/dc-testament'),
            Testament(uri='/scriptures/pgp'),
        ])

    def test_books(self):
        self.assertEqual(Structure().books(testament=Testament(uri='/scriptures/dc-testament')), [
            Book(uri='/scriptures/dc-testament/dc'),
            Book(uri='/scriptures/dc-testament/od'),
        ])
        self.assertEqual(Structure().books(testament=Testament(uri='/scriptures/pgp')), [
            Book(uri='/scriptures/pgp/moses'),
            Book(uri='/scriptures/pgp/abr'),
            Book(uri='/scriptures/pgp/js-m'),
            Book(uri='/scriptures/pgp/js-h'),
            Book(uri='/scriptures/pgp/a-of-f'),
        ])

    def test_chapters(self):
        self.assertEqual(Structure().chapters(book=Book(uri='/scriptures/dc-testament/od')), [
            Chapter(uri='/scriptures/dc-testament/od/1', verse_count=0),
            Chapter(uri='/scriptures/dc-testament/od/2', verse_count=0),
        ])
        self.assertEqual(Structure().chapters(book=Book(uri='/scriptures/ot/hag')), [
            Chapter(uri='/scriptures/ot/hag/1', verse_count=15),
            Chapter(uri='/scriptures/ot/hag/2', verse_count=23),
        ])
