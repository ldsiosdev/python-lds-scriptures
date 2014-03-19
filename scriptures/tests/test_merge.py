import unittest
from scriptures import ref, merged

class TestMerge(unittest.TestCase):
    def test_merge_fail(self):
        with self.assertRaises(ValueError):
            ref('/scriptures/ot/gen/1').merged(ref('/scriptures/ot/gen/2'))
        with self.assertRaises(ValueError):
            ref('/scriptures/ot/gen/1.1-4').merged(ref('/scriptures/ot/gen/2.3-4,6'))
            
    def test_merge(self):
        self.assertEqual(ref('/scriptures/ot/gen/1.1-4').merged(ref('/scriptures/ot/gen/1.5')), ref('/scriptures/ot/gen/1.1-5'))
        self.assertEqual(ref('/scriptures/ot/gen/1.1-4').merged(ref('/scriptures/ot/gen/1.6')), ref('/scriptures/ot/gen/1.1-4,6'))
        self.assertEqual(ref('/scriptures/ot/gen/1.1').merged(ref('/scriptures/ot/gen/1.4-6')), ref('/scriptures/ot/gen/1.1,4-6'))
        self.assertEqual(ref('/scriptures/ot/gen/1.1,5-6').merged(ref('/scriptures/ot/gen/1.3-8')), ref('/scriptures/ot/gen/1.1,3-8'))
        self.assertEqual(ref('/scriptures/ot/gen/1.1,5-6').merged(ref('/scriptures/ot/gen/1.17')), ref('/scriptures/ot/gen/1.1,5-6,17'))
        
    def test_merge_with_and_without_chapter(self):
        self.assertEqual(ref('/scriptures/ot/gen/1').merged(ref('/scriptures/ot/gen/1.5')), ref('/scriptures/ot/gen/1'))
        self.assertEqual(ref('/scriptures/ot/gen/1.5').merged(ref('/scriptures/ot/gen/1')), ref('/scriptures/ot/gen/1'))
        
    def test_merge_with_and_without_book_and_chapter(self):
        self.assertEqual(ref('/scriptures/ot/gen').merged(ref('/scriptures/ot/gen/1')), ref('/scriptures/ot/gen'))
        self.assertEqual(ref('/scriptures/ot/gen').merged(ref('/scriptures/ot/gen/1.5')), ref('/scriptures/ot/gen'))
        self.assertEqual(ref('/scriptures/ot/gen/1').merged(ref('/scriptures/ot/gen')), ref('/scriptures/ot/gen'))
        self.assertEqual(ref('/scriptures/ot/gen/1.5').merged(ref('/scriptures/ot/gen')), ref('/scriptures/ot/gen'))
    
    def test_merged(self):
        self.assertEqual(merged([
            ref('/scriptures/ot/gen/1.1-4'),
            ref('/scriptures/ot/gen/2.3-4,6'),
            ref('/scriptures/ot/gen/2.5'),
            ref('/scriptures/ot/gen/3.1-7'),
            ref('/scriptures/ot/gen/3.9-11'),
            ref('/scriptures/ot/gen/3.13-14'),
            ref('/scriptures/ot/gen/3.12-16'),
        ]), [
            ref('/scriptures/ot/gen/1.1-4'),
            ref('/scriptures/ot/gen/2.3-6'),
            ref('/scriptures/ot/gen/3.1-7,9-16'),
        ])