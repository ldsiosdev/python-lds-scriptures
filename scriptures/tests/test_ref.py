import unittest
import scriptures

class TestRef(unittest.TestCase):
    def test_completely_invalid(self):
        with self.assertRaises(TypeError):
            scriptures.ref(None)
        with self.assertRaises(ValueError):
            scriptures.ref('')
        with self.assertRaises(ValueError):
            scriptures.ref('/something')

    def test_no_testament(self):
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures')

    def test_no_book(self):
        uri = '/scriptures/ot'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', None, None, None)
        self.assertEqual(ref.uri(), uri)

    def test_invalid_testament(self):
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/something/alma')

    def test_invalid_book(self):
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/matt')

    def test_invalid_chapter(self):
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/0')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/23')

    def test_invalid_verses(self):
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.0')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.0-20')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.21')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.20-21')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.1,0')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.1,21')

    def test_incorrectly_ordered_verses(self):
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.1,1')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.1-1')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.2-1')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.2,1')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.5,3-6')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.5,1-4')
        with self.assertRaises(ValueError):
            scriptures.ref('/scriptures/bofm/1-ne/1.1-2,3,1')

    def test_no_chapter(self):
        uri = '/scriptures/ot/isa'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', 'isa')
        self.assertEqual(ref.uri(), uri)

    def test_no_verses(self):
        uri = '/scriptures/ot/isa/40'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40)
        self.assertEqual(ref.uri(), uri)

    def test_single_verse(self):
        uri = '/scriptures/ot/isa/40.1'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 1)])
        self.assertEqual(ref.uri(), uri)

    def test_single_verse_range(self):
        uri = '/scriptures/ot/isa/40.1-4'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 4)])
        self.assertEqual(ref.uri(), uri)

    def test_discontiguous_single_verses(self):
        uri = '/scriptures/ot/isa/40.1,4'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 1), (4, 4)])
        self.assertEqual(ref.uri(), uri)

    def test_discontiguous_verse_and_verse_range(self):
        uri = '/scriptures/ot/isa/40.1,6-7'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 1), (6, 7)])
        self.assertEqual(ref.uri(), uri)

    def test_discontiguous_verse_range_and_verse(self):
        uri = '/scriptures/ot/isa/40.1-4,6'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 4), (6, 6)])
        self.assertEqual(ref.uri(), uri)

    def test_discontiguous_verse_ranges(self):
        uri = '/scriptures/ot/isa/40.1-4,6-7,10'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 4), (6, 7), (10, 10)])
        self.assertEqual(ref.uri(), uri)

    def test_parentheticals(self):
        uri = '/scriptures/dc-testament/dc/76.56-57(50-70)'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'dc-testament', 'dc', 76, [(56, 57)], (50, 70))
        self.assertEqual(ref.uri(), uri)

    def test_chapter_ranges(self):
        uri = '/scriptures/bofm/alma/56-57'
        ref = scriptures.ref(uri)
        self.assert_scripture_ref(ref, 'bofm', 'alma', (56, 57))
        self.assertEqual(ref.uri(), uri)

    def assert_scripture_ref(self, ref, testament=None, book=None, chapter=None, verse_ranges=None, parens=None):
        self.assertEqual(ref.testament, testament)
        self.assertEqual(ref.book, book)
        self.assertEqual(ref.chapter, chapter)
        self.assertEqual(ref.verse_ranges, verse_ranges)
        self.assertEqual(ref.parens, parens)
