import unittest

from scriptures import ScriptureRef


class TestGospelLibraryURL(unittest.TestCase):
    def test_completely_invalid(self):
        with self.assertRaises(TypeError):
            ScriptureRef(gospel_library_url=None)
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/something')

    def test_no_testament(self):
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures')

    def test_no_book(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', None, None, None)
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_invalid_testament(self):
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/something/alma')

    def test_invalid_book(self):
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/matt')

    def test_invalid_chapter(self):
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/0')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/23')

    def test_invalid_verses(self):
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=0')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=0-20')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=21')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=20-21')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=1,0')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=1,21')

    def test_invalid_verses_without_validation(self):
        gospel_library_url = 'gospellibrary://content/scriptures/bofm/1-ne/1?verse=21#p21'
        ref = ScriptureRef(gospel_library_url=gospel_library_url, validate_verses=False)
        self.assert_scripture_ref(ref, 'bofm', '1-ne', 1, [(21, 21)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

        gospel_library_url = 'gospellibrary://content/scriptures/bofm/1-ne/1?verse=20-21#p20'
        ref = ScriptureRef(gospel_library_url=gospel_library_url, validate_verses=False)
        self.assert_scripture_ref(ref, 'bofm', '1-ne', 1, [(20, 21)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

        gospel_library_url = 'gospellibrary://content/scriptures/bofm/1-ne/1?verse=1,21#p1'
        ref = ScriptureRef(gospel_library_url=gospel_library_url, validate_verses=False)
        self.assert_scripture_ref(ref, 'bofm', '1-ne', 1, [(1, 1), (21, 21)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_incorrectly_ordered_verses(self):
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=1,1')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=1-1')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=2-1')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=2,1')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=5,3-6')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=5,1-4')
        with self.assertRaises(ValueError):
            ScriptureRef(gospel_library_url='gospellibrary://content/scriptures/bofm/1-ne/1?verse=1-2,3,1')

    def test_no_chapter(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot/isa'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', 'isa')
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_no_verses(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot/isa/40'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40)
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_single_verse(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot/isa/40?verse=1#p1'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 1)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_single_verse_range(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot/isa/40?verse=1-4#p1'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 4)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_discontiguous_single_verses(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot/isa/40?verse=1,4#p1'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 1), (4, 4)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_discontiguous_verse_and_verse_range(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot/isa/40?verse=1,6-7#p1'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 1), (6, 7)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_discontiguous_verse_range_and_verse(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot/isa/40?verse=1-4,6#p1'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 4), (6, 6)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_discontiguous_verse_ranges(self):
        gospel_library_url = 'gospellibrary://content/scriptures/ot/isa/40?verse=1-4,6-7,10#p1'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'ot', 'isa', 40, [(1, 4), (6, 7), (10, 10)])
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_parentheticals(self):
        gospel_library_url = 'gospellibrary://content/scriptures/dc-testament/dc/76?verse=56-57&context=50-70#p56'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'dc-testament', 'dc', 76, [(56, 57)], (50, 70))
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def test_chapter_ranges(self):
        gospel_library_url = 'gospellibrary://content/scriptures/bofm/alma/56-57'
        ref = ScriptureRef(gospel_library_url=gospel_library_url)
        self.assert_scripture_ref(ref, 'bofm', 'alma', (56, 57))
        self.assertEqual(ref.gospel_library_url(), gospel_library_url)

    def assert_scripture_ref(self, ref, testament=None, book=None, chapter=None, verse_ranges=None, parens=None):
        self.assertEqual(ref.testament, testament)
        self.assertEqual(ref.book, book)
        self.assertEqual(ref.chapter, chapter)
        self.assertEqual(ref.verse_ranges, verse_ranges)
        self.assertEqual(ref.parens, parens)
