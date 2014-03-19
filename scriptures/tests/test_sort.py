import unittest
from scriptures import ref

class TestSort(unittest.TestCase):
    def test_testaments(self):
        ot1 = ref('/scriptures/ot/gen')
        nt1 = ref('/scriptures/nt/matt/7')
        nt2 = ref('/scriptures/nt/mark/11')
        bofm1 = ref('/scriptures/bofm/1-ne')
        dc1 = ref('/scriptures/dc-testament/dc/108')
        pgp1 = ref('/scriptures/pgp/moses')
        
        self.assertEqual(sorted([ nt1, ot1, bofm1, pgp1, dc1, nt2 ]), [ ot1, nt1, nt2, bofm1, dc1, pgp1 ])
        
    def test_books(self):
        nt1 = ref('/scriptures/nt/matt')
        nt2 = ref('/scriptures/nt/mark/8')
        nt3 = ref('/scriptures/nt/luke')
        nt4 = ref('/scriptures/nt/john/3')
        nt5 = ref('/scriptures/nt/rev/11')
        
        self.assertEqual(sorted([ nt4, nt2, nt3, nt5, nt1 ]), [ nt1, nt2, nt3, nt4, nt5 ])
        
    def test_chapters(self):
        matt1 = ref('/scriptures/nt/matt/1')
        matt2 = ref('/scriptures/nt/matt/4')
        matt3 = ref('/scriptures/nt/matt/7')
        matt4 = ref('/scriptures/nt/matt/8')
        matt5 = ref('/scriptures/nt/matt/17')
        
        self.assertEqual(sorted([ matt4, matt2, matt3, matt5, matt1 ]), [ matt1, matt2, matt3, matt4, matt5 ])
        
    def test_with_and_without_chapter(self):
        matt1 = ref('/scriptures/nt/matt')
        matt2 = ref('/scriptures/nt/matt/4')
        
        self.assertEqual(sorted([ matt2, matt1 ]), [ matt1, matt2 ])
        
    def test_single_verses(self):
        matt1 = ref('/scriptures/nt/matt/1.1')
        matt2 = ref('/scriptures/nt/matt/1.3')
        matt3 = ref('/scriptures/nt/matt/1.8')
        matt4 = ref('/scriptures/nt/matt/1.11')
        matt5 = ref('/scriptures/nt/matt/1.23')
        
        self.assertEqual(sorted([ matt4, matt2, matt3, matt5, matt1 ]), [ matt1, matt2, matt3, matt4, matt5 ])
        
    def test_single_verse_ranges(self):
        matt1 = ref('/scriptures/nt/matt/1.1')
        matt2 = ref('/scriptures/nt/matt/1.1-5')
        matt3 = ref('/scriptures/nt/matt/1.2')
        matt4 = ref('/scriptures/nt/matt/1.2-3')
        matt5 = ref('/scriptures/nt/matt/1.2-6')
        
        self.assertEqual(sorted([ matt2, matt3, matt5, matt4, matt1 ]), [ matt1, matt2, matt3, matt4, matt5 ])
        
    def test_verse_ranges(self):
        matt1 = ref('/scriptures/nt/matt/1.1,7-21')
        matt2 = ref('/scriptures/nt/matt/1.1-5')
        matt3 = ref('/scriptures/nt/matt/1.2,3-5')
        matt4 = ref('/scriptures/nt/matt/1.2-3,11-12,19-20')
        matt5 = ref('/scriptures/nt/matt/1.2-6,9')
        
        self.assertEqual(sorted([ matt4, matt2, matt3, matt5, matt1 ]), [ matt1, matt2, matt3, matt4, matt5 ])
        
    def test_with_and_without_verses(self):
        matt1 = ref('/scriptures/nt/matt/1')
        matt2 = ref('/scriptures/nt/matt/1.1-5')
        
        self.assertEqual(sorted([ matt2, matt1 ]), [ matt1, matt2 ])
        
    def test_with_and_without_chapter_and_verses(self):
        matt1 = ref('/scriptures/nt/matt')
        matt2 = ref('/scriptures/nt/matt/1')
        matt3 = ref('/scriptures/nt/matt/1.2')
        
        self.assertEqual(sorted([ matt2, matt3, matt1 ]), [ matt1, matt2, matt3 ])
