"""
Test constitues level 1 and 2 functionality.
"""

import os
import unittest

from key_column_value_store import KeyColumnValueStore


class TestSequenceFunctions(unittest.TestCase):
    """container to hold different test scenarios."""


    def setUp(self):
        try:
            os.remove(KeyColumnValueStore.DEFAULT_FILE)
        except OSError:
            # some of the files may not exist
            pass

        self.kcv_store = KeyColumnValueStore()

    def test_level1(self):
        """basic test to ensure set()"""

        # given this store and dataset
        self.kcv_store.set('a', 'aa', 'x')
        self.kcv_store.set('a', 'ab', 'x')
        self.kcv_store.set('c', 'cc', 'x')
        self.kcv_store.set('c', 'cd', 'x')
        self.kcv_store.set('d', 'de', 'x')
        self.kcv_store.set('d', 'df', 'x')

        # try to insert already existing columns
        self.kcv_store.set('a', 'aa', 'x')
        self.kcv_store.set('a', 'ab', 'x')
        self.kcv_store.set('c', 'cc', 'x')
        self.kcv_store.set('c', 'cd', 'x')
        self.kcv_store.set('d', 'de', 'x')
        self.kcv_store.set('d', 'df', 'x')


        # the statements below will evaluate to True
        is_true = self.kcv_store.get('a', 'aa') == 'x'
        self.assertTrue(is_true)
        is_true = self.kcv_store.get_key('a') == [('aa', 'x'), ('ab', 'x')]
        self.assertTrue(is_true)

        # nonexistent keys/columns, the statements below
        # will evaluate to True
        is_true = self.kcv_store.get('z', 'yy') is None
        self.assertTrue(is_true)

        is_true = self.kcv_store.get_key('z') == []
        self.assertTrue(is_true)

        # if we set different values on the 'a' key:
        self.kcv_store.set('a', 'aa', 'y')
        self.kcv_store.set('a', 'ab', 'z')

        # the statements below will evaluate to True
        is_true = self.kcv_store.get('a', 'aa') == 'y'
        self.assertTrue(is_true)

        is_true = self.kcv_store.get_key('a') == [('aa', 'y'), ('ab', 'z')]
        self.assertTrue(is_true)

        # deleting
        self.kcv_store.delete('d', 'df')
        # this will evaluate to True
        is_true = self.kcv_store.get_key('d') == [('de', 'x')]
        self.assertTrue(is_true)

        # delete an entire key
        self.kcv_store.delete_key('c')

        # this will evaluate to True
        is_true = self.kcv_store.get_key('c') == []
        self.assertTrue(is_true)

    def test_level2(self):
        """tests to ensrure slicing operations functions as expected."""

        # given this store and dataset
        self.kcv_store.set('a', 'aa', 'x')
        self.kcv_store.set('a', 'ab', 'x')
        self.kcv_store.set('a', 'ac', 'x')
        self.kcv_store.set('a', 'ad', 'x')
        self.kcv_store.set('a', 'ae', 'x')
        self.kcv_store.set('a', 'af', 'x')
        self.kcv_store.set('a', 'ag', 'x')

        # the following statements will evaluate to True
        is_true = self.kcv_store.get_slice('a', 'ac', 'ae') == [('ac', 'x'), ('ad', 'x'), ('ae', 'x')]
        self.assertTrue(is_true)

        is_true = self.kcv_store.get_slice('a', 'ae', None) == [('ae', 'x'), ('af', 'x'), ('ag', 'x')]
        self.assertTrue(is_true)

        is_true = self.kcv_store.get_slice('a', None, 'ac') == [('aa', 'x'), ('ab', 'x'), ('ac', 'x')]
        self.assertTrue(is_true)


if __name__ == '__main__':
    unittest.main()