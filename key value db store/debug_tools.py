import pickle
DEFAULT_FILE = 'kcv_store.pkl'
DEFAULT_FILE = 'codetestdata'

def inspect(file_name=DEFAULT_FILE):
    """
    unpickles data from disk, can be used to debug and inspect a pickled file.
    """
    pkl_file = open(file_name, 'rb')

    try:
        while True:

            data = pickle.load(pkl_file)
            print data
            if 'op' in data:
                # 'op' is the most frequent case so check for it first
                print 'op'
                # self._replay_op(data['op'])
            elif 'store' in data:
                print 'store'
                # self.store = data

            # pprint.pprint(data)

    except EOFError, e:
        pass
        # logging.info('load file completed.')

inspect()

