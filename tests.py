from io import open
import unittest
from partitioned_hash_join import (
    build_hash_table,
    h1,
    join,
    write
)


class PartitionedHashJoinTests(unittest.TestCase):

    def test_h1(self):
        self.assertEqual(h1('H1234567890'), 12)

    def test_join(self):
        r = open('r_test_bucket.txt', 'r')
        s = open('s_test_bucket.txt', 'r')
        hash_table = build_hash_table(r)
        result = join(hash_table, s)
        self.assertEqual(len(result.get('9019095166')), 3)


    def test_create_result_file(self):
        results = {488552576: set([u'D488552576\n', u'B488552576\n']),
                   482241448: set([u'G482241448\n']),
                   486356299: set([u'B486356299\n',
                                   u'D486356299\n',
                                   u'A486356299\n'])}
        write(results)
        expected_results = ['D488552576\n',
                            'B488552576\n',
                            'G482241448\n',
                            'B486356299\n',
                            'D486356299\n',
                            'A486356299\n']
        with open('result.txt') as f:
            for line in f:
                self.assertTrue(line in expected_results)

if __name__=='__main__':
    unittest.main()
