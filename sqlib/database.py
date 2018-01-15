from .column import Column
from .table import Table
from .tools import get_table_create_string
from .variables import CONFIG
import sqlite3


def create_table(name: str, *columns: Column):
    c = CONFIG['connection'].cursor()

    with CONFIG['connection']:
        c.execute(get_table_create_string(name, *columns))

    return Table(name)


def connect(database=":memory:"):
    CONFIG['connection'] = sqlite3.connect(database, check_same_thread=False)
    return CONFIG['connection']
