# coding=utf-8

import unittest
from scriptures import ref, format, FORMAT_LONG, FORMAT_SHORT

class TestFormat(unittest.TestCase):
    def test_format_general(self):
        def formatter_test(label, ref):
            return '<a href="%s">%s</a>' % (ref.uri(), label)

        self.assertEqual(format(ref('/scriptures/ot/gen/40')), 'Genesis 40')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1')), 'Genesis 40:1')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1-3')), u'Genesis 40:1–3')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1,3')), 'Genesis 40:1, 3')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1,3-5')), u'Genesis 40:1, 3–5')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1-3,5')), u'Genesis 40:1–3, 5')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1-3,5-10')), u'Genesis 40:1–3, 5–10')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1-3,5-10'), formatter=formatter_test), u'<a href="/scriptures/ot/gen/40.1-3,5-10">Genesis 40:1–3, 5–10</a>')

    def test_single_chapter_book(self):
        self.assertEqual(format(ref('/scriptures/ot/obad/1')), 'Obadiah 1')
        self.assertEqual(format(ref('/scriptures/nt/jude/1')), 'Jude 1')
        self.assertEqual(format(ref('/scriptures/bofm/4-ne/1')), u'4\u00a0Nephi 1')
        self.assertEqual(format(ref('/scriptures/pgp/js-m/1')), u'Joseph Smith—Matthew 1')

    def test_format_eng(self):
        self.assertEqual(format(ref('/scriptures/ot')), 'Old Testament')
        self.assertEqual(format(ref('/scriptures/ot/isa/40')), 'Isaiah 40')
        self.assertEqual(format(ref('/scriptures/nt/rev/11')), 'Revelation 11')
        self.assertEqual(format(ref('/scriptures/bofm/2-ne/5')), u'2\u00a0Nephi 5')
        self.assertEqual(format(ref('/scriptures/dc-testament/dc/110')), 'Doctrine and Covenants 110')
        self.assertEqual(format(ref('/scriptures/pgp/moses/2')), 'Moses 2')

    def test_format_spa(self):
        self.assertEqual(format(ref('/scriptures/ot'), lang='spa'), u'Antiguo Testamento')
        self.assertEqual(format(ref('/scriptures/ot/isa/40'), lang='spa'), u'Isaías 40')
        self.assertEqual(format(ref('/scriptures/nt/rev/11'), lang='spa'), u'Apocalipsis 11')
        self.assertEqual(format(ref('/scriptures/bofm/2-ne/5'), lang='spa'), u'2\u00a0Nefi 5')
        self.assertEqual(format(ref('/scriptures/dc-testament/dc/110'), lang='spa'), u'Doctrina y Convenios 110')
        self.assertEqual(format(ref('/scriptures/pgp/moses/2'), lang='spa'), u'Moisés 2')

    def test_format_dc_variations(self):
        self.assertEqual(format(ref('/scriptures/dc-testament/dc/110'), book_format=FORMAT_LONG), 'Doctrine and Covenants 110')
        self.assertEqual(format(ref('/scriptures/dc-testament/dc/110'), book_format=FORMAT_SHORT), 'D&C 110')

    def test_format_od(self):
        self.assertEqual(format(ref('/scriptures/dc-testament/od'), book_format=FORMAT_LONG), 'Official Declarations')
        self.assertEqual(format(ref('/scriptures/dc-testament/od'), book_format=FORMAT_SHORT), 'OD')
        self.assertEqual(format(ref('/scriptures/dc-testament/od/1'), book_format=FORMAT_LONG), u'Official Declaration—1')
        self.assertEqual(format(ref('/scriptures/dc-testament/od/1'), book_format=FORMAT_SHORT), u'OD—1')
        self.assertEqual(format(ref('/scriptures/dc-testament/od/2'), book_format=FORMAT_LONG), u'Official Declaration—2')
        self.assertEqual(format(ref('/scriptures/dc-testament/od/2'), book_format=FORMAT_SHORT), u'OD—2')

    def test_format_psalms(self):
        self.assertEqual(format(ref('/scriptures/ot/ps'), book_format=FORMAT_LONG), 'Psalms')
        self.assertEqual(format(ref('/scriptures/ot/ps'), book_format=FORMAT_SHORT), 'Ps.')
        self.assertEqual(format(ref('/scriptures/ot/ps/3'), book_format=FORMAT_LONG), 'Psalm 3')
        self.assertEqual(format(ref('/scriptures/ot/ps/3'), book_format=FORMAT_SHORT), 'Ps. 3')
        self.assertEqual(format([ref('/scriptures/ot/ps/3.1'), ref('/scriptures/ot/ps/3.2-3')]), u'Psalm 3:1–3')

        # TODO
        # self.assertEqual(format([ref('/scriptures/ot/ps/3'), ref('/scriptures/ot/ps/4')]), u'Psalms 3–4')

    def test_format_multiple_refs_in_chapter(self):
        self.assertEqual(format([ref('/scriptures/ot/gen/40.1'), ref('/scriptures/ot/gen/40.1-5')]), u'Genesis 40:1–5')
        self.assertEqual(format([ref('/scriptures/ot/gen/40.1'), ref('/scriptures/ot/gen/40.3-5')]), u'Genesis 40:1, 3–5')

    def test_format_multiple_refs_in_book(self):
        self.assertEqual(format([ref('/scriptures/ot/gen/39.1'), ref('/scriptures/ot/gen/40.1-5')]), u'Genesis 39:1; 40:1–5')
        self.assertEqual(format([ref('/scriptures/ot/gen/39'), ref('/scriptures/ot/gen/40.3-5')]), u'Genesis 39; 40:3–5')
        self.assertEqual(format([ref('/scriptures/ot/gen/39'), ref('/scriptures/ot/gen/40')]), u'Genesis 39–40')
        self.assertEqual(format([ref('/scriptures/ot/gen/39'), ref('/scriptures/ot/gen/41')]), u'Genesis 39; 41')
        self.assertEqual(format([ref('/scriptures/ot/gen/39'), ref('/scriptures/ot/gen/41'), ref('/scriptures/ot/gen/42')]), u'Genesis 39; 41–42')

    def test_format_multiple_refs_across_books(self):
        self.assertEqual(format([ref('/scriptures/ot/gen/39.1'), ref('/scriptures/ot/ex/10.1-5')]), u'Genesis 39:1; Exodus 10:1–5')
        self.assertEqual(format([ref('/scriptures/ot/gen/39'), ref('/scriptures/ot/ex/40.3-5')]), u'Genesis 39; Exodus 40:3–5')
        self.assertEqual(format([ref('/scriptures/ot/gen/39'), ref('/scriptures/ot/ex/21'), ref('/scriptures/ot/ex/22')]), u'Genesis 39; Exodus 21–22')

    def test_short_format(self):
        self.assertEqual(format([
            ref("/scriptures/nt/matt/23"),
            ref("/scriptures/nt/matt/24"),
            ref("/scriptures/nt/acts/3"),
            ref("/scriptures/nt/acts/6"),
            ref("/scriptures/nt/acts/11"),
            ref("/scriptures/nt/rom/8"),
            ref("/scriptures/nt/1-cor/4"),
            ref("/scriptures/nt/gal/1"),
            ref("/scriptures/nt/2-thes/2"),
            ref("/scriptures/nt/2-tim/4"),
            ref("/scriptures/nt/titus/1"),
            ref("/scriptures/nt/1-pet/4"),
            ref("/scriptures/nt/1-jn/2"),
            ref("/scriptures/dc-testament/dc/1"),
            ref("/scriptures/dc-testament/dc/102"),
            ref("/scriptures/dc-testament/dc/107"),
            ref("/scriptures/dc-testament/dc/115"),
            ref("/scriptures/pgp/js-h/1")
        ], book_format=FORMAT_SHORT), u'Matt. 23–24; Acts 3; 6; 11; Rom. 8; 1\u00a0Cor. 4; Gal. 1; 2\u00a0Thes. 2; 2\u00a0Tim. 4; Titus 1; 1\u00a0Pet. 4; 1\u00a0Jn. 2; D&C 1; 102; 107; 115; JS—H 1')

    def test_format_closure(self):
        def formatter_test(label, ref):
            return '<a href="%s">%s</a>' % (ref.uri(), label)

        self.assertEqual(format([ref('/scriptures/ot/gen/39.1'), ref('/scriptures/ot/ex/10.1-5')], formatter=formatter_test), u'<a href="/scriptures/ot/gen/39.1">Genesis 39:1</a>; <a href="/scriptures/ot/ex/10.1-5">Exodus 10:1–5</a>')
        self.assertEqual(format(ref('/scriptures/ot/gen/39.1'), formatter=formatter_test), u'<a href="/scriptures/ot/gen/39.1">Genesis 39:1</a>')

    def test_parentheticals(self):
        self.assertEqual(format(ref('/scriptures/dc-testament/dc/76.56-57,60(50-70)')), u'Doctrine and Covenants 76:56–57, 60 (50–70)')

    def test_chapter_ranges(self):
        self.assertEqual(format(ref('/scriptures/dc-testament/dc/76.56-57,60(50-70)')), u'Doctrine and Covenants 76:56–57, 60 (50–70)')
