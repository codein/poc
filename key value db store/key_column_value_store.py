"""
Implementation of a key/column/value store.

KeyColumnValueStore is the implementation,
using pure python dict and tuples.

RedisKeyColumnValueStore is a incomplete implementation
that supports backing the data to redis.
"""

from Queue import Queue
from threading import Thread
import inspect
import logging
import pickle

import redis

LOG_FORMAT = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)


class KeyColumnValueStore(object):
    """
    Implementation of a key/column/value store.

    A key column value store is similar to a nested hash table,
    with the following requirements:

    * like a hash table, a key can only occur once
    * within a given key, a column cannot appear more than once, like a hash table
    * when querying the contents of a key, a list of column/value tuples are returned,
        sorted by column
    * all keys, columns, and values will be strings of variable length
    * errors shouldn't be raised if a nonexistent key/column is accessed,
        empty lists / None values should be returned

    write a class that gets, sets, and deletes keys, columns, and values, iterate over
    keys, return columns in order by implementing the class defined below
    you should design your implementation with the assumption that reads will be much
    more frequent than writes
    """
    DEFAULT_FILE = 'kcv_store.pkl'

    def __init__(self, path=DEFAULT_FILE):
        """
        Loads the store from a persisted file on disk.
        KeyColumnValueStore('codetest') will load store from a user defined file

        KeyColumnValueStore() will try to load from the DEFAULT_FILE.
        if a file doesn't exist an empty store is instantiated.
        """
        self.store = None
        self.thread = None
        self.persist = False
        self.op_queue = None
        self._load_file(path)
        self._initialize_op_queue()

    # Internal function to achieve persistance to disk.
    def _load_file(self, file_name=DEFAULT_FILE):
        """
        Loads store from a given file, where the store was persisted to disk.

        Pickeled file on disk, consists of two objects
        1. a dict containing the inital store state.
        for ex. {'store': {...}}
        2. a sequence of operations performed on the store after intial load
        for ex {'op': {'func': 'set', args': [key, val, col]}}

        Firstly, we load the initial store state.
        Secondly, we replay all operations sequentially.
        Finally persist the current store state to disk.
        """
        self.persist = False

        try:
            with open(file_name, 'rb') as pkl_file:
                try:

                    while True:
                        data = pickle.load(pkl_file)
                        if 'op' in data:
                            # 'op' is the most frequent case so check for it first
                            self._replay_op(data['op'])
                        elif 'store' in data:
                            self.store = data['store']
                            logging.info('Store loaded.')

                except EOFError:
                    logging.info('load file completed.')

        except IOError:
            logging.error('No file on disk, creating a empty store.')
            self.store = {}

        self._persist_store(mode='wb+')
        self.persist = True

    def _initialize_op_queue(self):
        """
        A worker queue is initialized to persist each operations performed on the store.

        Every `set` and `delete` operations needs to be put on this op_queue
        inorder to be persisted to disk.
        """
        self.op_queue = Queue()

        def worker():
            """
            worker thread waiting for ops to be put on op_queue.
            """
            try:
                while True:
                    op = self.op_queue.get(True)
                    self._persist_op(op)
                    self.op_queue.task_done()

            except EOFError:
                logging.error('Operation queue closed.')

        self.thread = Thread(target=worker)
        self.thread.daemon = True
        self.thread.start()

    def _replay_op(self, op):
        """replays a given op to modify the current store state."""
        func = op['func']
        args = op['args']

        operation = getattr(self, op['func'])
        operation(*op['args'])
        logging.info('Replayed operation %s(*%s)', func, args)

    def _persist_to_file(self, data, file_name, mode):
        """persists a given data to disk"""
        output = open(file_name, mode)
        # Pickle the list using the highest protocol available.
        pickle.dump(data, output, -1)
        output.close()

    def _persist_store(self, file_name=DEFAULT_FILE, mode='ab'):
        """persists the store to disk."""
        self._persist_to_file({'store': self.store}, file_name, mode)

    def _persist_op(self, op, file_name=DEFAULT_FILE):
        """persists a given op to disk."""
        self._persist_to_file({'op': op}, file_name, mode='ab')

    def _get_op(self, frame):
        """given a frame object returns an op dict that can be persisited."""

        func = frame[0][3]
        arg_info = inspect.getargvalues(frame[0][0])
        args = []
        for arg in arg_info.args:
            if arg != 'self':
                args.append(arg_info.locals[arg])

        return {
            'func': func,
            'args': args
        }

    def _push_op_stack(self, stack):
        """
        if persistence is enabled. get the op object and put it on the op_queue."""
        if self.persist:
            op = self._get_op(stack)
            self.op_queue.put(op)

    # Write operations
    def set(self, key, col, val):
        """ sets the value at the given key/column """
        try:
            record = self.store[key]
        except KeyError:
            logging.info('Key %s not found.', key)
            record = []
            self.store[key] = record

        for index, column_tuple in enumerate(record):
            column, value = column_tuple
            if column == col:
                logging.info('column %s already exists, set to %s', col, val)
                record[index] = (col, val)
                break

            elif column > col:
                record.insert(index, (col, val))
                break
        else:
            # if none are found then append to the tail
            record.append((col, val))

        self._push_op_stack(inspect.stack())
        return True

    def delete(self, key, col):
        """ removes a column/value from the given key """
        try:
            record = self.store[key]
        except KeyError:
            logging.error('Key %s not found.', key)
            return None

        for index, column_value in enumerate(record):
            column, value = column_value
            if column == col:
                record.remove(column_value)
                self._push_op_stack(inspect.stack())
                return True

        logging.error('Column %s not found.', col)
        return None

    def delete_key(self, key):
        """ removes all data associated with the given key """
        try:
            del self.store[key]
        except KeyError:
            logging.error('Key %s not found.', key)
            return None

        self._push_op_stack(inspect.stack())
        return True

    # Read operations
    def get(self, key, col):
        """ return the value at the specified key/column """
        try:
            record = self.store[key]
        except KeyError:
            logging.error('Key %s not found.', key)
            return None

        for column, value in record:
            if column == col:
                return value

        logging.error('Column %s not found.', col)
        return None

    def get_key(self, key):
        """ returns a sorted list of column/value tuples """
        try:
            record = self.store[key]
        except KeyError:
            logging.error('Key %s not found.', key)
            return []

        return record

    def get_keys(self):
        """ returns a set containing all of the keys in the store """
        return self.store.keys()

    def get_slice(self, key, start, stop):
        """
        returns a sorted list of column/value tuples where the column
        values are between the start and stop values, inclusive of the
        start and stop values. Start and/or stop can be None values,
        leaving the slice open ended in that direction
        """
        try:
            record = self.store[key]
        except KeyError:
            logging.error('Key %s not found.', key)
            return None

        _slice = []
        has_reached_start = False
        has_reached_stop = False
        for index, column_value in enumerate(record):
            column, value = column_value

            if not has_reached_start:
                if column == start or start is None:
                    has_reached_start = True

            if has_reached_start and not has_reached_stop:
                _slice.append(column_value)

            if column == stop:
                has_reached_stop = True

        return _slice


class RedisKeyColumnValueStore(KeyColumnValueStore):
    """
    RedisKeyColumnValueStore is a incomplete implementation that could support
    backing the store to redis.
    """
    def __init__(self, path=KeyColumnValueStore.DEFAULT_FILE):
        self.redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)
        self._load_file(path)
        self._initialize_op_queue()

    def _load_file(self, file_name=KeyColumnValueStore.DEFAULT_FILE):
        self.persist = False

        try:
            with open(file_name, 'rb') as pkl_file:
                try:
                    while True:

                        data = pickle.load(pkl_file)
                        if 'op' in data:
                            # 'op' is the most frequent case so check for it first
                            self._replay_op(data['op'])
                        elif 'store' in data:
                            for key, record in data['store'].iteritems():
                                record_pkl = pickle.dumps(record)
                                self.redis_store.set(key, record_pkl)

                            logging.info('Store loaded.')

                except EOFError:
                    logging.info('load file completed.')

        except IOError:
            logging.error('No file on disk, creating a empty store.')
            self.store = {}

        self._persist_store(mode='wb+')
        self.persist = True


    # Write operations
    def set(self, key, col, val):
        """ sets the value at the given key/column """
        record_pkl = self.redis_store.get(key)
        if record_pkl is None:
            logging.info('Key %s not found.', key)
            record = []

        record = pickle.loads(record_pkl)
        for index, column_tuple in enumerate(record):
            print column_tuple
            column, value = column_tuple
            if column == col:
                logging.info('column %s already exists, set to %s', col, val)
                record[index] = (col, val)
                break

            elif column > col:
                record.insert(index, (col, val))
                break
        else:
            # if none are found then append to the tail
            record.append((col, val))

        record_pkl = pickle.dumps(record)
        self.redis_store.set(key, record_pkl)
        self._push_op_stack(inspect.stack())
        return True

    def delete(self, key, col):
        """ removes a column/value from the given key """
        record_pkl = self.redis_store.get(key)
        if record_pkl is None:
            logging.error('Key %s not found.', key)
            return None

        record = pickle.loads(record_pkl)
        for index, column_value in enumerate(record):
            column, value = column_value
            if column == col:
                record.remove(column_value)

                record_pkl = pickle.dumps(record)
                self.redis_store.set(key, record_pkl)
                self._push_op_stack(inspect.stack())
                return True

        logging.error('Column %s not found.', col)
        return None

    def delete_key(self, key):
        """ removes all data associated with the given key """
        self.redis_store.delete(key)
        self._push_op_stack(inspect.stack())
        return True

    # Read operations
    def get(self, key, col):
        """ return the value at the specified key/column """
        record_pkl = self.redis_store.get(key)
        if record_pkl is None:
            logging.error('Key %s not found.', key)
            return None

        record = pickle.loads(record_pkl)
        for column, value in record:
            if column == col:
                return value

        logging.error('Column %s not found.', col)
        return None

    def get_key(self, key):
        """ returns a sorted list of column/value tuples """
        record_pkl = self.redis_store.get(key)
        if record_pkl is None:
            logging.error('Key %s not found.', key)
            return []

        record = pickle.loads(record_pkl)
        return record

    def get_keys(self):
        """ returns a set containing all of the keys in the store """
        return self.redis_store.keys()

    def get_slice(self, key, start, stop):
        """
        returns a sorted list of column/value tuples where the column
        values are between the start and stop values, inclusive of the
        start and stop values. Start and/or stop can be None values,
        leaving the slice open ended in that direction
        """
        record_pkl = self.redis_store.get(key)
        if record_pkl is None:
            logging.error('Key %s not found.', key)
            return None

        record = pickle.loads(record_pkl)

        _slice = []
        has_reached_start = False
        has_reached_stop = False
        for index, column_value in enumerate(record):
            column, value = column_value

            if not has_reached_start:
                if column == start or start is None:
                    has_reached_start = True

            if has_reached_start and not has_reached_stop:
                _slice.append(column_value)

            if column == stop:
                has_reached_stop = True

        return _slice
