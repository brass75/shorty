import json
import logging
from json import JSONDecodeError
from typing import Any
import os
from lib.utils import get_data_dir


class ShortyDB:
    """Data handler class for src"""

    class ShortyDBError(Exception):
        pass

    FILE_STORE = f'{get_data_dir()}/shorty.json'
    __version__ = '1.0'

    def __init__(self, file_store: str = None, path: str = None):
        """
        Initialize the data store

        :param file_store: Location for the file store
        """
        self.logger = logging.getLogger('db')
        if file_store:
            self._file_store = file_store
        else:
            self._file_store = os.path.join(path, self.FILE_STORE) if path else self.FILE_STORE
        self._datastore = {}
        self._urls = {}
        try:
            with open(self._file_store) as f:
                self._datastore = json.load(f)
        except FileNotFoundError:
            self.logger.warning(f'No file found at {self._file_store} - initializing a new data store.')
        except JSONDecodeError as e:
            self.logger.error(f'Error parsing JSON in data store:\n{e.msg}')
        else:
            self.logger.debug(f'Found db at {self._file_store}.')
            self.logger.debug(json.dumps(self._datastore, indent=2))
        self._update_datastore()

    def get(self, key, default=None):
        """
        Return the data associated with the key or default

        :param key: The key to check
        :param default: The default value to return
        """
        return self._urls.get(key, default)

    def add(self, key: str, value: Any):
        """
        Add an entry into the data store

        :param key: Key of the entry to add
        :param value: Value to add
        :raises ShortyDB.ShortyDBError if key already exists
        """
        if key in self._urls:
            raise self.ShortyDBError(f'ERROR: {repr(key)} exists in the datastore!')
        self._urls[key] = value
        self._store_db()

    def _store_db(self):
        """
        Update the persistent data store
        :return:
        """
        self.logger.warning(f'Saving data store to {self._file_store=}')
        with open(self._file_store, 'w') as f:
            json.dump(self._datastore, f, indent=1)

    def __getitem__(self, item: str):
        """
        Retrieve an entry from the data store

        :param item: Key of the entry to add
        :raises ShortyDB.ShortyDBError if key already exists
        """
        try:
            return self._urls[item]
        except KeyError:
            raise self.ShortyDBError(f'ERROR: {repr(item)} does not exist in the datastore')

    def __setitem__(self, key, value):
        return self.add(key, value)

    def _update_datastore(self):
        """
        Updates the data store to the current version. Populates and variables in self.
        """
        update_needed = True
        match version := self._datastore.get('version'):
            case self.__version__:
                update_needed = False
            case None:
                self._datastore = {'version': self.__version__, 'urls': self._datastore}
            case _:
                print(f'Unknown data store {version=}')
                self._datastore = {
                    'version': self.__version__,
                    'urls': self._datastore.get('urls', {}),
                }
        self._urls = self._datastore.get('urls', {})
        if update_needed:
            self._store_db()

    def items(self):
        """
        Return the items from the URLs

        :return: dict_items from the URLs
        """
        return self._urls.items()
