import unittest
import scriptures


class TestUniversalURL(unittest.TestCase):
    def test_no_verses(self):
        uri = '/scriptures/ot/isa/40'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_no_verses_with_lang(self):
        uri = '/scriptures/ot/isa/40'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?lang=spa'
        self.assertEqual(scriptures.ref(uri).universal_url(lang='spa'), universal_url)

    def test_single_verse_with_first(self):
        uri = '/scriptures/ot/isa/40.1'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p1#p1'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_single_verse_range_with_first(self):
        uri = '/scriptures/ot/isa/40.1-4'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p1-p4#p1'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_discontiguous_single_verses_with_first(self):
        uri = '/scriptures/ot/isa/40.1,4'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p1,p4#p1'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_discontiguous_verse_and_verse_range_with_first(self):
        uri = '/scriptures/ot/isa/40.1,6-7'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p1,p6-p7#p1'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_discontiguous_verse_range_and_verse_with_first(self):
        uri = '/scriptures/ot/isa/40.1-4,6'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p1-p4,p6#p1'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_discontiguous_verse_ranges_with_first(self):
        uri = '/scriptures/ot/isa/40.1-4,6-7,10'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p1-p4,p6-p7,p10#p1'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_single_verse(self):
        uri = '/scriptures/ot/isa/40.2'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p2#p2'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_single_verse_with_lang(self):
        uri = '/scriptures/ot/isa/40.2'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p2&lang=spa#p2'
        self.assertEqual(scriptures.ref(uri).universal_url(lang='spa'), universal_url)

    def test_single_verse_range(self):
        uri = '/scriptures/ot/isa/40.2-4'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p2-p4#p2'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_discontiguous_single_verses(self):
        uri = '/scriptures/ot/isa/40.2,4'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p2,p4#p2'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_discontiguous_verse_and_verse_range(self):
        uri = '/scriptures/ot/isa/40.2,6-7'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p2,p6-p7#p2'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_discontiguous_verse_range_and_verse(self):
        uri = '/scriptures/ot/isa/40.2-4,6'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p2-p4,p6#p2'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_discontiguous_verse_ranges(self):
        uri = '/scriptures/ot/isa/40.2-4,6-7,10'
        universal_url = 'https://www.lds.org/study/scriptures/ot/isa/40?id=p2-p4,p6-p7,p10#p2'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_parentheticals(self):
        uri = '/scriptures/dc-testament/dc/76.56-57(50-70)'
        universal_url = 'https://www.lds.org/study/scriptures/dc-testament/dc/76?id=p56-p57&context=p50-p70#p56'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_parentheticals_with_lang(self):
        uri = '/scriptures/dc-testament/dc/76.56-57(50-70)'
        universal_url = 'https://www.lds.org/study/scriptures/dc-testament/dc/76?id=p56-p57&context=p50-p70&lang=spa#p56'
        self.assertEqual(scriptures.ref(uri).universal_url(lang='spa'), universal_url)

    def test_chapter_ranges(self):
        uri = '/scriptures/bofm/alma/56-57'
        universal_url = 'https://www.lds.org/study/scriptures/bofm/alma/56-57'
        self.assertEqual(scriptures.ref(uri).universal_url(), universal_url)

    def test_chapter_ranges_with_lang(self):
        uri = '/scriptures/bofm/alma/56-57'
        universal_url = 'https://www.lds.org/study/scriptures/bofm/alma/56-57?lang=spa'
        self.assertEqual(scriptures.ref(uri).universal_url(lang='spa'), universal_url)
