"""
Ensures given a perisited file, the store can be loaded corectly from codetestdata
"""
import os
import shutil
import unittest

from key_column_value_store import KeyColumnValueStore

class TestSequenceFunctions(unittest.TestCase):
    """container to hold different test scenarios."""


    def setUp(self):
        self.kcv_store = KeyColumnValueStore('codetestdata')

    def _consistency_check(self, key):
        isTrue = self.kcv_store.get_slice(key, 'ac', 'ae') == [('ac', 'x'), ('ad', 'x'), ('ae', 'x')]
        self.assertTrue(isTrue)

        isTrue = self.kcv_store.get_slice(key, 'ae', None) == [('ae', 'x'), ('af', 'x'), ('ag', 'x')]
        self.assertTrue(isTrue)

        isTrue = self.kcv_store.get_slice(key, None, 'ac') == [('aa', 'x'), ('ab', 'x'), ('ac', 'x')]
        self.assertTrue(isTrue)

        isTrue = self.kcv_store.get(key, 'aa') == 'x'
        self.assertTrue(isTrue)

    def test_load_from_file(self):
        self.kcv_store.set('a', 'aa', 'x')
        isTrue = self.kcv_store.get('a', 'aa') == 'x'
        self.assertTrue(isTrue)

        self._consistency_check(key='a')
        self._consistency_check(key='e')

if __name__ == '__main__':
    unittest.main()