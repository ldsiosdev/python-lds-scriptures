import unittest
import scriptures


class TestURLPath(unittest.TestCase):
    def test_no_verses(self):
        uri = '/scriptures/ot/isa/40'
        url_path = '/scriptures/ot/isa/40.html'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)

    def test_single_verse(self):
        uri = '/scriptures/ot/isa/40.1'
        url_path = '/scriptures/ot/isa/40.html?verse=1#p1'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)

    def test_single_verse_range(self):
        uri = '/scriptures/ot/isa/40.1-4'
        url_path = '/scriptures/ot/isa/40.html?verse=1-4#p1'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)

    def test_discontiguous_single_verses(self):
        uri = '/scriptures/ot/isa/40.1,4'
        url_path = '/scriptures/ot/isa/40.html?verse=1,4#p1'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)

    def test_discontiguous_verse_and_verse_range(self):
        uri = '/scriptures/ot/isa/40.1,6-7'
        url_path = '/scriptures/ot/isa/40.html?verse=1,6-7#p1'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)

    def test_discontiguous_verse_range_and_verse(self):
        uri = '/scriptures/ot/isa/40.1-4,6'
        url_path = '/scriptures/ot/isa/40.html?verse=1-4,6#p1'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)

    def test_discontiguous_verse_ranges(self):
        uri = '/scriptures/ot/isa/40.1-4,6-7,10'
        url_path = '/scriptures/ot/isa/40.html?verse=1-4,6-7,10#p1'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)

    def test_parentheticals(self):
        uri = '/scriptures/dc-testament/dc/76.56-57(50-70)'
        url_path = '/scriptures/dc-testament/dc/76.html?verse=56-57&context=50-70#p56'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)

    def test_chapter_ranges(self):
        uri = '/scriptures/bofm/alma/56-57'
        url_path = '/scriptures/bofm/alma/56.html'
        self.assertEqual(scriptures.ref(uri).url_path(), url_path)
