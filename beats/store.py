import contextlib
import json

import lmdb


class MISSING(object):
    pass


class D(object):
    def __init__(self, target):
        self.target = target

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        value = self.target.get(key, MISSING)
        if value is MISSING:
            raise KeyError(key)
        return json.loads(value)

    def __setitem__(self, key, value):
        return self.target.put(key, json.dumps(value))

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False


class Store(object):
    def __init__(self, path):
        self.env = lmdb.open(path, mode=0700, max_dbs=10)

    @contextlib.contextmanager
    def db(self, name, write=False):
        with self.env.begin(db=self.env.open_db(name), write=write) as txn:
            yield D(txn)

    def drop(self, name, delete=True):
        db = self.env.open_db(name)
        with self.env.begin(write=True) as txn:
            txn.drop(db, delete=delete)
