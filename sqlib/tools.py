from .column import Column
import functools


def bit_to_bool(bit: int):
    if bit == 0:
        return False
    elif bit == 1:
        return True


def get_table_create_string(table_name, *columns: Column) -> str:
    primaries = [column for column in columns if column.PRIMARY_KEY is True]

    if len(primaries) > 1:
        def_primaries = f", PRIMARY KEY ({functools.reduce(lambda x, y: x.name+', '+y.name, primaries)})"

        def_columns = []
        for column in columns:
            if column in primaries:
                def_columns.append(column.string.replace(" PRIMARY KEY", ""))
            else:
                def_columns.append(column.string)

    else:
        def_primaries = ""
        def_columns = [col.string for col in columns]

    def_columns = functools.reduce(lambda x, y: x + ', ' + y, def_columns)

    return "CREATE TABLE {0} ({1}{2})".format(table_name, def_columns, def_primaries)


def concat(iterable, separator=', ') -> str:
    if not iterable:
        return ""

    return functools.reduce(lambda x, y: f"{x}{separator}{y}", iterable)
