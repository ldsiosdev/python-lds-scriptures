# coding=utf-8

import unittest
from scriptures import ref, format

class TestFormat(unittest.TestCase):
    def test_format_general(self):
        self.assertEqual(format(ref('/scriptures/ot/gen/40')), 'Genesis 40')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1')), 'Genesis 40:1')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1-3')), u'Genesis 40:1–3')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1,3')), 'Genesis 40:1, 3')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1,3-5')), u'Genesis 40:1, 3–5')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1-3,5')), u'Genesis 40:1–3, 5')
        self.assertEqual(format(ref('/scriptures/ot/gen/40.1-3,5-10')), u'Genesis 40:1–3, 5–10')
        
    def test_single_chapter_book(self):
        self.assertEqual(format(ref('/scriptures/ot/obad/1')), 'Obadiah 1')
        self.assertEqual(format(ref('/scriptures/nt/jude/1')), 'Jude 1')
        self.assertEqual(format(ref('/scriptures/bofm/4-ne/1')), u'4\u00a0Nephi 1')
        self.assertEqual(format(ref('/scriptures/pgp/js-m/1')), u'Joseph Smith—Matthew 1')
        
    def test_format_eng(self):
        self.assertEqual(format(ref('/scriptures/ot/isa/40')), 'Isaiah 40')
        self.assertEqual(format(ref('/scriptures/nt/rev/11')), 'Revelation 11')
        self.assertEqual(format(ref('/scriptures/bofm/2-ne/5')), u'2\u00a0Nephi 5')
        self.assertEqual(format(ref('/scriptures/dc-testament/dc/110')), 'Doctrine and Covenants 110')
        self.assertEqual(format(ref('/scriptures/pgp/moses/2')), 'Moses 2')
        
    def test_format_spa(self):
        self.assertEqual(format(ref('/scriptures/ot/isa/40'), lang='spa'), u'Isaías 40')
        self.assertEqual(format(ref('/scriptures/nt/rev/11'), lang='spa'), u'Apocalipsis 11')
        self.assertEqual(format(ref('/scriptures/bofm/2-ne/5'), lang='spa'), u'2\u00a0Nefi 5')
        self.assertEqual(format(ref('/scriptures/dc-testament/dc/110'), lang='spa'), u'Doctrina y Convenios 110')
        self.assertEqual(format(ref('/scriptures/pgp/moses/2'), lang='spa'), u'Moisés 2')
