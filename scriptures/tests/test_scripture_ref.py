import unittest
from scriptures import ScriptureRef

class TestScriptureRef(unittest.TestCase):
    def test_no_args(self):
        with self.assertRaises(TypeError):
            ScriptureRef()
                    
    def test_no_book(self):
        with self.assertRaises(ValueError):
            ScriptureRef(testament='ot')
        
    def test_invalid_testament(self):
        with self.assertRaises(ValueError):
            ScriptureRef(testament='something')
        
    def test_invalid_book(self):
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='matt')
        
    def test_invalid_chapter(self):
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=0)
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=23)
        
    def test_invalid_verses(self):
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(0, 0)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(0, 20)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(21, 21)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(20, 21)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(1, 0)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(1, 21)])
        
    def test_incorrectly_ordered_verses(self):
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(1, 1), (1, 1)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(2, 1)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(2, 2), (1, 1)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(5, 5), (3, 6)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(5, 5), (1, 4)])
        with self.assertRaises(ValueError):
            ScriptureRef(testament='bofm', book='1-ne', chapter=1, verse_ranges=[(1, 2), (3, 3), (1, 1)])
        
    def test_no_chapter(self):
        self.assert_scripture_ref(ScriptureRef(testament='ot', book='isa'), 'ot', 'isa')
    
    def test_no_verses(self):
        self.assert_scripture_ref(ScriptureRef(testament='ot', book='isa', chapter=40), 'ot', 'isa', 40)
    
    def test_single_verse(self):
        self.assert_scripture_ref(ScriptureRef(testament='ot', book='isa', chapter=40, verse_ranges=[(1, 1)]), 'ot', 'isa', 40, [(1, 1)])
    
    def test_single_verse_range(self):
        self.assert_scripture_ref(ScriptureRef(testament='ot', book='isa', chapter=40, verse_ranges=[(1, 4)]), 'ot', 'isa', 40, [(1, 4)])
    
    def test_discontiguous_single_verses(self):
        self.assert_scripture_ref(ScriptureRef(testament='ot', book='isa', chapter=40, verse_ranges=[(1, 1), (4, 4)]), 'ot', 'isa', 40, [(1, 1), (4, 4)])
    
    def test_discontiguous_verse_and_verse_range(self):
        self.assert_scripture_ref(ScriptureRef(testament='ot', book='isa', chapter=40, verse_ranges=[(1, 1), (6, 7)]), 'ot', 'isa', 40, [(1, 1), (6, 7)])
    
    def test_discontiguous_verse_range_and_verse(self):
        self.assert_scripture_ref(ScriptureRef(testament='ot', book='isa', chapter=40, verse_ranges=[(1, 4), (6, 6)]), 'ot', 'isa', 40, [(1, 4), (6, 6)])
    
    def test_discontiguous_verse_ranges(self):
        self.assert_scripture_ref(ScriptureRef(testament='ot', book='isa', chapter=40, verse_ranges=[(1, 4), (6, 7), (10, 10)]), 'ot', 'isa', 40, [(1, 4), (6, 7), (10, 10)])

    def assert_scripture_ref(self, ref, testament=None, book=None, chapter=None, verse_ranges=None):
        self.assertEqual(ref.testament, testament)
        self.assertEqual(ref.book, book)
        self.assertEqual(ref.chapter, chapter)
        self.assertEqual(ref.verse_ranges, verse_ranges)
