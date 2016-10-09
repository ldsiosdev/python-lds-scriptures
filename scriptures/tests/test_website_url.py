import unittest
import scriptures


class TestWebsiteURL(unittest.TestCase):
    def test_no_verses(self):
        uri = '/scriptures/ot/isa/40'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_no_verses_with_lang(self):
        uri = '/scriptures/ot/isa/40'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40?lang=spa'
        self.assertEqual(scriptures.ref(uri).website_url(lang='spa'), website_url)

    def test_single_verse_with_first(self):
        uri = '/scriptures/ot/isa/40.1'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.1#primary'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_single_verse_range_with_first(self):
        uri = '/scriptures/ot/isa/40.1-4'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.1-4#primary'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_discontiguous_single_verses_with_first(self):
        uri = '/scriptures/ot/isa/40.1,4'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.1,4#primary'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_discontiguous_verse_and_verse_range_with_first(self):
        uri = '/scriptures/ot/isa/40.1,6-7'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.1,6-7#primary'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_discontiguous_verse_range_and_verse_with_first(self):
        uri = '/scriptures/ot/isa/40.1-4,6'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.1-4,6#primary'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_discontiguous_verse_ranges_with_first(self):
        uri = '/scriptures/ot/isa/40.1-4,6-7,10'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.1-4,6-7,10#primary'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_single_verse(self):
        uri = '/scriptures/ot/isa/40.2'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.2#1'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_single_verse_with_lang(self):
        uri = '/scriptures/ot/isa/40.2'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.2?lang=spa#1'
        self.assertEqual(scriptures.ref(uri).website_url(lang='spa'), website_url)

    def test_single_verse_range(self):
        uri = '/scriptures/ot/isa/40.2-4'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.2-4#1'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_discontiguous_single_verses(self):
        uri = '/scriptures/ot/isa/40.2,4'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.2,4#1'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_discontiguous_verse_and_verse_range(self):
        uri = '/scriptures/ot/isa/40.2,6-7'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.2,6-7#1'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_discontiguous_verse_range_and_verse(self):
        uri = '/scriptures/ot/isa/40.2-4,6'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.2-4,6#1'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_discontiguous_verse_ranges(self):
        uri = '/scriptures/ot/isa/40.2-4,6-7,10'
        website_url = 'https://www.lds.org/scriptures/ot/isa/40.2-4,6-7,10#1'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_parentheticals(self):
        uri = '/scriptures/dc-testament/dc/76.56-57(50-70)'
        website_url = 'https://www.lds.org/scriptures/dc-testament/dc/76.56-57(50-70)#55'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_parentheticals_with_lang(self):
        uri = '/scriptures/dc-testament/dc/76.56-57(50-70)'
        website_url = 'https://www.lds.org/scriptures/dc-testament/dc/76.56-57(50-70)?lang=spa#55'
        self.assertEqual(scriptures.ref(uri).website_url(lang='spa'), website_url)

    def test_chapter_ranges(self):
        uri = '/scriptures/bofm/alma/56-57'
        website_url = 'https://www.lds.org/scriptures/bofm/alma/56-57'
        self.assertEqual(scriptures.ref(uri).website_url(), website_url)

    def test_chapter_ranges_with_lang(self):
        uri = '/scriptures/bofm/alma/56-57'
        website_url = 'https://www.lds.org/scriptures/bofm/alma/56-57?lang=spa'
        self.assertEqual(scriptures.ref(uri).website_url(lang='spa'), website_url)
