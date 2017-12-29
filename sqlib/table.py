import sqlite3
import functools
from .column import Column
from .variables import CONFIG
from .functions import *


class Table:
    """ Represents an sqlite3 table. """
    def __init__(self, name):
        self._name = None
        self.name = name

        self._conn = sqlite3.connect(CONFIG['database'])
        self._c = self._conn.cursor()

        self._c.execute(f"PRAGMA TABLE_INFO ({self.name})")

        self._columns = list(map(
            lambda x: Column(x[1], x[2], not_null=bit_to_bool(x[3]), default=x[4], primary_key=bit_to_bool(x[5])),
            self._c.fetchall()
            ))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        # TODO: update name in database
        self._name = name

    @property
    def columns(self):
        return self._columns

    @property
    def string(self):
        primaries = [column for column in self.columns if column.PRIMARY_KEY is True]

        if len(primaries) > 1:
            def_primaries = f", PRIMARY KEY ({functools.reduce(lambda x, y: x.name+', '+y.name, primaries)})"

            def_columns = []
            for column in self.columns:
                if column in primaries:
                    def_columns.append(column.string.replace(" PRIMARY KEY", ""))
                else:
                    def_columns.append(column.string)

        else:
            def_primaries = ""
            def_columns = [col.string for col in self.columns]

        def_columns = functools.reduce(lambda x, y: x + ', ' + y, def_columns)

        return "CREATE TABLE IF NOT EXISTS {0} ({1}{2})".format(self.name, def_columns, def_primaries)

    def get(self, column, value, only_column: str=None, fetch=1):
        if only_column is None:
            selection = "*"
        else:
            selection = only_column

        self._c.execute(f"SELECT {selection} FROM {self.name} WHERE {column}=:value", {"value": value})

        if fetch == 1:
            return self._tup_to_dict(self._c.fetchone())
        elif fetch == 'all' or fetch == '*':
            return self._tuplist_to_dictlist(self._c.fetchall())
        else:
            return self._tuplist_to_dictlist(self._c.fetchmany(fetch))

    def get_all(self, only_column: str=None):
        if only_column is None:
            selection = "*"
        else:
            selection = only_column

        self._c.execute(f"SELECT {selection} FROM {self.name}")

        return self._tuplist_to_dictlist(self._c.fetchall())

    def insert(self, values: dict):
        cols_str = functools.reduce(lambda x, y: f"{x}, {y}", map(lambda x: '?', self.columns))

        with self._conn:
            self._c.execute(f"INSERT INTO {self.name} VALUES ({cols_str})", self._dict_to_tup(values))
        return values

    def update(self, column, value, new_values: dict):
        with self._conn:
            self._c.execute(
                "UPDATE {0} SET {1} WHERE {2}={3}".format(
                    self.name,
                    functools.reduce(lambda x, y: f"{x},{y}", map(lambda col: f"{col}=:{col}", new_values)),
                    column,
                    value
                ),
                new_values
            )
        return new_values

    def delete(self, column, value):
        with self._conn:
            self._c.execute(f"DELETE FROM {self.name} WHERE {column}=:value", {'value': value})

    def _tup_to_dict(self, tup: tuple):
        if tup is None:
            return None
        if len(tup) == 1:
            return tup[0]

        dic = {}
        for i in range(len(tup)):
            dic[self.columns[i].name] = tup[i]
        return dic

    def _tuplist_to_dictlist(self, tuplist):
        return list(map(lambda x: self._tup_to_dict(x), tuplist))

    def _dict_to_tup(self, dic):
        lst = []
        for col in self.columns:
            lst.append(dic.get(col.name, None))
        return tuple(lst)
