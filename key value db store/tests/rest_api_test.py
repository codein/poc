"""
Test constitues level 4 functionality.

implement a rest server that interfaces with level 3 and supports all of the operations
described above.
"""


import requests
import json
import shutil
import httplib
import unittest


class TestSequenceFunctions(unittest.TestCase):
    """container to hold different test scenarios."""
    def setUp(self):
        self.base_url = 'http://localhost:8888'

    def _get_url(self, path):
        """given a relative path, return full url"""
        return '%s/%s' % (self.base_url, path)

    def test1_set(self):
        """
        test scenario checks functionality of set, delete and get
        firtly, add 2 keys with 2 coulmns.
        Secondly, check if gets works.
        Next delete a few columns and ensure get behaves as expected.
        finally delete all the keys.
        """
        data = self.put('key/a/col/aa/val/y')
        self.assertTrue(data['data'])

        data = self.put('key/a/col/ab/val/y')
        self.assertTrue(data['data'])

        data = self.put('key/b/col/ab/val/x')
        self.assertTrue(data['data'])

        data = self.put('key/b/col/aa/val/x')
        self.assertTrue(data['data'])

        data = self.get('key/a/col/aa')
        self.assertTrue(data['data'] == 'y')

        data = self.get('key/b/col/aa')
        self.assertTrue(data['data'] == 'x')

        data = self.get('keys')
        self.assertTrue('a' in data['data'])
        self.assertTrue('b' in data['data'])

        data = self.delete('key/a/col/aa')
        self.assertTrue(data['data'])

        data = self.get('key/a/col/aa')
        self.assertTrue(data['data'] is None)

        data = self.get('key/a/col/ab')
        self.assertTrue(data['data'] == 'y')

        data = self.delete('key/a')
        self.assertTrue(data['data'])

        data = self.get('key/a/col/ab')
        self.assertTrue(data['data'] is None)

        data = self.delete('key/b')
        self.assertTrue(data['data'])

        data = self.get('key/b/col/aa')
        self.assertTrue(data['data'] is None)

        data = self.get('key/b/col/ab')
        self.assertTrue(data['data'] is None)

    def test_slice(self):
        """
        add 7 columns to key
        slice mid
        slice tail
        silce head
        """
        data = self.put('key/a/col/aa/val/x')
        self.assertTrue(data['data'])

        data = self.put('key/a/col/ab/val/x')
        self.assertTrue(data['data'])

        data = self.put('key/a/col/ac/val/x')
        self.assertTrue(data['data'])

        data = self.put('key/a/col/ad/val/x')
        self.assertTrue(data['data'])

        data = self.put('key/a/col/ae/val/x')
        self.assertTrue(data['data'])

        data = self.put('key/a/col/af/val/x')
        self.assertTrue(data['data'])

        data = self.put('key/a/col/ag/val/x')
        self.assertTrue(data['data'])

        data = self.get('key/a/start/ac/stop/ae')
        self.assertTrue(data['data'] == [['ac', 'x'], ['ad', 'x'], ['ae', 'x']])

        data = self.get('key/a/start/ae/stop/0')
        self.assertTrue(data['data'] == [['ae', 'x'], ['af', 'x'], ['ag', 'x']])

        data = self.get('key/a/start/0/stop/ac')
        self.assertTrue(data['data'] == [['aa', 'x'], ['ab', 'x'], ['ac', 'x']])

    def _loads_response(self, response):
        """given a response object json.loads the data and return."""
        if response.status_code == httplib.OK:
            return json.loads(response.text)

    def delete(self, path):
        """helper to make DELETE requests"""
        url = self._get_url(path)
        response = requests.delete(url)
        return self._loads_response(response)

    def put(self, path):
        """helper to make PUT requests"""
        url = self._get_url(path)
        response = requests.put(url)
        return self._loads_response(response)

    def get(self, path, data=None):
        """helper to make GET requests"""
        url = self._get_url(path)
        response = requests.get(url)
        return self._loads_response(response)

if __name__ == '__main__':
    unittest.main()