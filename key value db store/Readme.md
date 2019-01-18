### Directory overview

##### key/column/value store
Implementation of a key/column/value store is in `shift.com/key_column_value_store.py`

KeyColumnValueStore is the implementation, using pure python dict and tuples.

RedisKeyColumnValueStore is a incomplete implementation that supports backing the data to redis.

##### REST API server
implemention a rest server that interfaces with KeyColumnValueStore in `shift.com/server.py`
you can run as follows
```
source bashrc
./run_server.sh
```

##### unitest to ensure functionality
`tests` dir includes all unittest
you can run as follows
```
source bashrc
./test_runner.sh
```
Ensure you have the web server running, else the `rest_api_test.py` will fail.

##### Persisted file
`codetestdata` is a preserved state of the store used in `load_from_file_test.py`
`kcv_store.pkl` is the default file that the store loads from is persisted to. `disk_persistance_test.py` deletes it every time it runs.

##### External dependencies
have been included in `requirements.txt`

### Implementation overview

##### Persisted disk file overview
Pickeled file on disk, consists of two objects
1. a dict containing the inital store state. for ex. `{'store': {...}}`
2. a sequence of operations performed on the store after intial load for ex `{'op': {'func': 'set', args': [key, val, col]}}`

Firstly, we load the initial store state from this file.
Secondly, we replay all operations sequentially.
Finally persist the current store state back to disk.

##### op_queue worker
We spin off a worker process to write operation sequentially to disk.
every operation wih side effects puts itself on this queue, before returning the results.
This helps to keep this async and avoid data corruption.

### Limitations and improvements
* RedisKeyColumnValueStore is incomplete, redis might me appropriate to scale.
* if the process where to crash, all inflight ops in op_queue will be lost without getting a chance to be written to disk.
* tornado server handlers could be made coroutines with yields.
* a two level of hash structure would be more efficient on redis, to avoid pickling loads and dumps.
{
    ...
    '<key>': [<column_name> ...(sorted list of column_names)]
    '<key>': [<column_name> ...(sorted list of column_names)]
    '<key>': [<column_name> ...(sorted list of column_names)]
    ...
}

{
    ...
    '<key>-<column_name>': <value>
    '<key>-<column_name>': <value>
    '<key>-<column_name>': <value>
    ...
}