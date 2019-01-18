"""
tornado web server
Implement a REST server that interfaces with KeyColumnValueStore
and supports all of the operations.
"""

import json
import logging

import tornado.ioloop
import tornado.web

from key_column_value_store import KeyColumnValueStore

LOG_FORMAT = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)


class JsonRequestHandler(tornado.web.RequestHandler):
    """Base Handler with capabiblity to write json data back"""

    @property
    def store(self):
        """store property from the main application object is referenced"""
        if not hasattr(self, '_store'):
            self._store = self.application.store

        return self._store

    def json_write(self, data):
        """Given a python dict wraps it in a data attribute and returned."""
        self.write(json.dumps({'data': data}))

class AllKeysHandler(JsonRequestHandler):
    """
    '/keys' endpoint is served
    Only GET is exposed
    """

    def get(self):
        """returns a set containing all of the keys in the store"""
        data = self.store.get_keys()
        self.json_write(data)

class KeyHandler(JsonRequestHandler):
    """
    '/key/<key>' endpoint is served
    Only GET and DELETE are exposed.
    """

    def get(self, key):
        """ returns a sorted list of column/value tuples """
        data = self.store.get_key(key)
        self.json_write(data)

    def delete(self, key):
        data = self.store.delete_key(key)
        self.json_write(data)

class KeyColumnHandler(JsonRequestHandler):
    """
    '/key/<key>/col/<col>' endpoint is served
    Only GET and DELETE are exposed.
    """

    def get(self, key, col):
        """ return the value at the specified key/column """
        data = self.store.get(key, col)
        self.json_write(data)

    def delete(self, key, col):
        """ removes a column/value from the given key """
        data = self.store.delete(key, col)
        self.json_write(data)

class KeyColumnValueHandler(JsonRequestHandler):
    """
    '/key/<key>/col/<col>/val/<val>' endpoint is served
    Only PUT is exposed.
    """

    def put(self, key, col, val):
        """ sets the value at the given key/column """
        data = self.store.set(key, col, val)
        self.json_write(data)

class SliceHandler(JsonRequestHandler):
    """
    '/key/<key>/start/<start>/stop/<stop>' endpoint is served
    Only GET is exposed.
    """

    def get(self, key, start, stop):
        """
        returns a sorted list of column/value tuples where the column
        values are between the start and stop values, inclusive of the
        start and stop values. Start and/or stop can be None values,
        leaving the slice open ended in that direction
        """
        if start == '0':
            start = None
        if stop == '0':
            stop = None

        data = self.store.get_slice(key, start, stop)
        self.json_write(data)


class KeyColumnValueStoreApp(tornado.web.Application):
    """Main app KeyColumnValueStore singleton is an attribute of this object."""
    handlers = [
        (r"/keys", AllKeysHandler),
        (r"/key/*([a-zA-Z0-9-]*)", KeyHandler),
        (r"/key/*([a-zA-Z0-9-]*)/col/*([a-zA-Z0-9-]*)", KeyColumnHandler),
        (r"/key/*([a-zA-Z0-9-]*)/col/*([a-zA-Z0-9-]*)/val/*([a-zA-Z0-9-]*)", KeyColumnValueHandler),
        (r"/key/*([a-zA-Z0-9-]*)/start/*([a-zA-Z0-9-]*)/stop/*([a-zA-Z0-9-]*)", SliceHandler)
    ]

    def __init__(self):
        tornado.web.Application.__init__(self, self.handlers, debug=True)

    @property
    def store(self):
        """intantiates the KeyColumnValueStore object."""
        if not hasattr(self, '_store'):
            self._store = KeyColumnValueStore()

        return self._store

if __name__ == "__main__":
    application = KeyColumnValueStoreApp()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

