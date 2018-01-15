from .column import Column
from . import tools
from .variables import CONFIG
from .errors import DatabaseError
import logging

logger = logging.getLogger('sqlib')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class Table:
    """ Represents an sqlite3 table. """
    def __init__(self, name):
        self._name = None
        self.name = name

        self._conn = CONFIG['connection']
        self._c = self._conn.cursor()

        self._c.execute(f"PRAGMA TABLE_INFO ({self.name})")
        table_info = self._c.fetchall()

        if not table_info:
            raise DatabaseError(f"Given table (\"{name}\") doesn't exist.")

        self._columns = list(map(
            lambda x: Column(x[1], x[2], not_null=tools.bit_to_bool(x[3]), default=x[4], primary_key=tools.bit_to_bool(x[5])),
            table_info
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
        return tools.get_table_create_string(self.name, *self.columns)

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
        cols = list(map(
                lambda x: x.name,
                filter(lambda x: x.default is None or values.get(x.name, None) is not None, self.columns)
        ))
        qm_str = tools.concat(list(map(lambda x: '?', cols)))

        cols_str = tools.concat(cols)

        with self._conn:
            if not cols:
                logger.info("Inserting only default values.")
                self._c.execute(f"INSERT INTO {self.name} DEFAULT VALUES")
            else:
                self._c.execute(f"INSERT INTO {self.name} ({cols_str}) VALUES ({qm_str})", self._dict_to_tup(values))
        return values

    def update(self, column, value, new_values: dict):
        with self._conn:
            self._c.execute(
                "UPDATE {0} SET {1} WHERE {2}={3}".format(
                    self.name,
                    tools.concat(map(lambda col: f"{col}=:{col}", new_values)),
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
            if col.default is None:
                lst.append(dic.get(col.name, None))

            elif dic.get(col.name) is not None:
                lst.append(dic[col.name])

        return tuple(lst)
