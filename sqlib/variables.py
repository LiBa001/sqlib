import sqlite3

TEXT = "TEXT"
INTEGER = "INTEGER"
REAL = "REAL"
NONE = "NONE"
NUMERIC = "NUMERIC"

AFFINITIES = [TEXT, INTEGER, REAL, NONE, NUMERIC]

CONFIG = {'connection': sqlite3.connect(':memory:', check_same_thread=False)}
