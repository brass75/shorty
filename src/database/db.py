import json
from json import JSONDecodeError
from typing import Any


class ShortyDB:
    """ Data handler class for shorty """
    class ShortyDBError(Exception):
        pass

    FILE_STORE = 'shorty.json'

    def __init__(self, file_store: str = None):
        """
        Initialize the data store

        :param file_store: Location for the file store
        """
        self._file_store = file_store or self.FILE_STORE
        self._datastore = {}
        try:
            with open(self._file_store) as f:
                self._datastore = json.load(f)
        except FileNotFoundError:
            print(f'No file found at {self._file_store} - initializing a new data store.')
        except JSONDecodeError as e:
            print(f'Error parsing JSON in data store:\n{e.msg}')

    def get(self, key, default=None):
        """
        Return the data associated with the key or default

        :param key: The key to check
        :param default: The default value to return
        """
        return self._datastore.get(key, default)

    def add(self, key: str, value: Any):
        """
        Add an entry into the data store

        :param key: Key of the entry to add
        :param value: Value to add
        :raises ShortyDB.ShortyDBError if key already exists
        """
        if key in self._datastore:
            raise self.ShortyDBError(f'ERROR: {repr(key)} exists in the datastore!')
        self._datastore[key] = value
        with open(self._file_store, 'w') as f:
            json.dump(self._datastore, f, indent=1)

    def __getitem__(self, item: str):
        """
        Retrieve an entry from the data store

        :param item: Key of the entry to add
        :raises ShortyDB.ShortyDBError if key already exists
        """
        try:
            return self._datastore[item]
        except KeyError:
            raise self.ShortyDBError(f'ERROR: {repr(item)} does not exist in the datastore')

    def __setitem__(self, key, value):
        return self.add(key, value)

