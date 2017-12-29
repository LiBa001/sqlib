__author__ = 'Linus Bartsch'
__title__ = 'sqlib'
__license__ = 'MIT'
__version__ = '0.0.1'

from .table import Table
from .column import Column
from .variables import *
from .errors import *

import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
