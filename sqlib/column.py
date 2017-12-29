from .variables import *
from . import errors


class Column:
    """ Represents an sqlite3 column."""

    def __init__(self, name: str, affinity: str, not_null=False, primary_key=False, unique=False, default=None):
        self.name = name

        self._affinity = None
        self.affinity = affinity

        self.NOT_NULL = not_null
        self.PRIMARY_KEY = primary_key
        self.UNIQUE = unique

        self._DEFAULT = None
        self.default = default

    @property
    def affinity(self):
        return self._affinity

    @affinity.setter
    def affinity(self, value):
        if value in AFFINITIES:
            self._affinity = value
        else:
            raise errors.AffinityNotFoundError

    @property
    def default(self):
        return self._DEFAULT

    @default.setter
    def default(self, value):
        if type(value) == str and self.affinity != TEXT:
            raise errors.DefaultValueError
        else:
            self._DEFAULT = value

    @property
    def string(self):
        sqlite_str = f"{self.name} {self.affinity}"

        if self.NOT_NULL:
            sqlite_str += " NOT NULL"

        if self.PRIMARY_KEY:
            sqlite_str += " PRIMARY KEY"

        if self.UNIQUE:
            sqlite_str += " UNIQUE"

        if self.default is not None:
            if type(self.default) == str:
                qm = "'"
            else:
                qm = ""

            sqlite_str += f" DEFAULT {qm}{self.default}{qm}"

        return sqlite_str
