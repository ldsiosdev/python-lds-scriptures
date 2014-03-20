import unittest
from scriptures import ref

class TestChaptersAndVerses(unittest.TestCase):
    def test_book_chapters(self):
        self.assertEqual(len(ref('/scriptures/ot/gen').chapters()), 50)
        self.assertEqual(len(ref('/scriptures/ot/gen').verses()), 0)
    
    def test_chapter_verses(self):
        self.assertEqual(len(ref('/scriptures/ot/gen/2').chapters()), 1)
        self.assertEqual(len(ref('/scriptures/ot/gen/2').verses()), 25)
        
    def test_verses(self):
        self.assertEqual(len(ref('/scriptures/ot/gen/2.3').chapters()), 0)
        self.assertEqual(len(ref('/scriptures/ot/gen/2.1-25').chapters()), 1)
        self.assertEqual(len(ref('/scriptures/ot/gen/2.1-2,3,4-25').chapters()), 1)
        self.assertEqual(len(ref('/scriptures/ot/gen/2.3').verses()), 1)
        self.assertEqual(len(ref('/scriptures/ot/gen/2.2-9').verses()), 8)
        self.assertEqual(len(ref('/scriptures/ot/gen/2.2-9,14,17-18').verses()), 11)
