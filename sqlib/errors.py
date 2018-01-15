class SqlibError(Exception):
    """ Base exception class for sqlib """

    pass


class AffinityNotFoundError(SqlibError):
    """ Exception that's thrown when a non-existing sqlite affinity is given. """

    def __init__(self):
        message = 'Given affinity not found. Use the ones from "variables.py"!'
        super(AffinityNotFoundError, self).__init__(message)


class DefaultValueError(SqlibError):
    """ Exception that's thrown when the default value of a column does not match the affinity. """

    def __init__(self):
        message = 'Default value does not match the affinity of the column.'
        super(DefaultValueError, self).__init__(message)


class DatabaseError(SqlibError):
    """ Exception that's thrown when an operation is in conflict with the sqlite database. """

    def __init__(self, message):
        super(DatabaseError, self).__init__(message)
