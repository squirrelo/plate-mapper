# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from functools import wraps

from .sql_connection import TRN


def convert_to_id(value, table, text_col=None):
    """Converts a string value to its corresponding table identifier

    Parameters
    ----------
    value : str
        The string value to convert
    table : str
        The table that has the conversion
    text_col : str, optional
        Column holding the string value. Defaults to same as table name.

    Returns
    -------
    int
        The id correspinding to the string

    Raises
    ------
    LookupError
        The passed string has no associated id
    """
    text_col = table if text_col is None else text_col
    with TRN:
        sql = "SELECT {0}_id FROM qiita.{0} WHERE {1} = %s".format(
            table, text_col)
        TRN.add(sql, [value])
        _id = TRN.execute_fetchindex()
        if not _id:
            raise LookupError(
                "%s not valid for table %s" % (value, table))
        # If there was a result it was a single row and and single value,
        # hence access to [0][0]
        return _id[0][0]


def convert_from_id(value, table):
    """Converts an id value to its corresponding string value

    Parameters
    ----------
    value : int
        The id value to convert
    table : str
        The table that has the conversion

    Returns
    -------
    str
        The string correspinding to the id

    Raises
    ------
    LookupError
        The passed id has no associated string
    """
    with TRN:
        sql = "SELECT {0} FROM qiita.{0} WHERE {0}_id = %s".format(table)
        TRN.add(sql, [value])
        string = TRN.execute_fetchindex()
        if not string:
            raise LookupError(
                "%s not valid for table %s" % (value, table))
        # If there was a result it was a single row and and single value,
        # hence access to [0][0]
        return string[0][0]


def get_count(table):
    """Counts the number of rows in a table

    Parameters
    ----------
    table : str
        The name of the table of which to count the rows

    Returns
    -------
    int
    """
    with TRN:
        sql = "SELECT count(1) FROM %s" % table
        TRN.add(sql)
        return TRN.execute_fetchlast()


def check_barcode_assigned(barcode):
    """Checks if barcode is already assigned

    Parameters
    ----------
    barcode : str
        Barcode to check

    Returns
    -------
    bool
        Barcode is already assigned (True) or not (False)

    Raises
    ------
    ValueError
        Barcode does not exist in database
    """
    sql = """SELECT barcode, assigned_on
        FROM barcodes.barcode
        WHERE barcode = %s
        """
    with TRN:
        TRN.add(sql)
        barcode_info = TRN.execute_fetchindex()
        if barcode_info is None:
            raise ValueError('Barcode %s does not exist in the DB' % barcode)
        # Check if assigned on date is set or not
        return False if barcode_info['assigned_on'] is None else True


def rollback_transaction(f):
    """Decorator to roll back work done in a transaction. Useful for testing"""
    @wraps(f)
    def inner(*args, **kwargs):
        with TRN:
            f(*args, **kwargs)
            TRN.rollback()
    return inner