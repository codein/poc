"""
Test constitues level 3 persistance to disk.
"""

import os
import shutil
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

    def _load_data(self):
        """load a preferined keys columns and values"""

        # given this store and dataset
        self.kcv_store.set('a', 'aa', 'x')
        self.kcv_store.set('a', 'ab', 'x')

        self.kcv_store.set('c', 'cc', 'x')
        self.kcv_store.set('c', 'cd', 'x')

        self.kcv_store.set('d', 'de', 'x')
        self.kcv_store.set('d', 'df', 'x')
        # deleting
        self.kcv_store.delete('d', 'df')

        # if we set different values on the 'a' key:
        self.kcv_store.set('a', 'aa', 'y')
        self.kcv_store.set('a', 'ab', 'z')

        self.kcv_store.set('a', 'aa', 'x')
        self.kcv_store.set('a', 'ab', 'x')
        self.kcv_store.set('a', 'ac', 'x')
        self.kcv_store.set('a', 'ad', 'x')
        self.kcv_store.set('a', 'ae', 'x')
        self.kcv_store.set('a', 'af', 'x')
        self.kcv_store.set('a', 'ag', 'x')


        # deleting
        self.kcv_store.delete('d', 'df')

        # delete an entire key
        self.kcv_store.delete_key('c')

    def _consistency_check_after_delete(self):
        "asserts the store state after few deletions have been performed."
        # this will evaluate to True
        is_true = self.kcv_store.get_key('d') == [('de', 'x')]
        self.assertTrue(is_true)

        # this will evaluate to True
        is_true = self.kcv_store.get_key('c') == []
        self.assertTrue(is_true)


    def _consistency_check(self, key):
        "asserts the store state after few set operations have been performed."
        is_true = self.kcv_store.get_slice(key, 'ac', 'ae') == [('ac', 'x'), ('ad', 'x'), ('ae', 'x')]
        self.assertTrue(is_true)

        is_true = self.kcv_store.get_slice(key, 'ae', None) == [('ae', 'x'), ('af', 'x'), ('ag', 'x')]
        self.assertTrue(is_true)

        is_true = self.kcv_store.get_slice(key, None, 'ac') == [('aa', 'x'), ('ab', 'x'), ('ac', 'x')]
        self.assertTrue(is_true)

        is_true = self.kcv_store.get(key, 'aa') == 'x'
        self.assertTrue(is_true)

    def test1_dry_start(self):
        """
        Simulates a start without a prior persisted files.
        loads some data
        the store is re instantiated to load from disk
        Verify the state with asserts previously performed.
        """

        self._load_data()

        self._consistency_check(key='a')
        self._consistency_check_after_delete()

        self.kcv_store = KeyColumnValueStore()

        self._consistency_check(key='a')
        self._consistency_check_after_delete()

        self.kcv_store.set('a', 'aa', 'x')
        is_true = self.kcv_store.get('a', 'aa') == 'x'
        self.assertTrue(is_true)

        self.kcv_store.set('e', 'aa', 'x')
        self.kcv_store.set('e', 'ab', 'x')
        self.kcv_store.set('e', 'ac', 'x')
        self.kcv_store.set('e', 'ad', 'x')
        self.kcv_store.set('e', 'ae', 'x')
        self.kcv_store.set('e', 'af', 'x')
        self.kcv_store.set('e', 'ag', 'x')

        self.kcv_store.set('e', 'aa', 'x')
        is_true = self.kcv_store.get('e', 'aa') == 'x'
        self.assertTrue(is_true)

        self._consistency_check(key='e')


if __name__ == '__main__':
    unittest.main()