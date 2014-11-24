from io import open
import unittest
from partitioned_hash_join import (
    build_hash_table,
    h1,
    is_duplicate,
    join,
    letters_for_result,
    value_for_letter,
    LETTERS
)

class PartitionedHashJoinTests(unittest.TestCase):

    def test_h1(self):
        self.assertEqual(h1('H1234567890'), 123)

    def test_is_duplicate(self):
        self.assertTrue(is_duplicate(100, 100))
        self.assertTrue(is_duplicate(10, 1010))
        self.assertFalse(is_duplicate(100, 1010))

    def test_join(self):
        r = open('r_test_bucket.txt', 'r')
        s = open('s_test_bucket.txt', 'r')
        hash_table = build_hash_table(r)
        result = join(hash_table, s)
        self.assertEqual(result.get('9019095166'), 100010001)

    def test_value_for_letter(self):
        for idx, l in enumerate(LETTERS):
            self.assertEqual(10**idx, value_for_letter(l))

    def test_letters_for_result(self):
        self.assertTrue(x in letters_for_result(100100010) for x in ['F', 'B', 'I'])


if __name__=='__main__':
    unittest.main()
