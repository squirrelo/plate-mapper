# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
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
        sql = "SELECT {0}_id FROM barcodes.{0} WHERE {1} = %s".format(
            table, text_col)
        TRN.add(sql, [value])
        _id = TRN.execute_fetchindex()
        if not _id:
            raise LookupError(
                "%s not valid for table %s" % (value, table))
        # If there was a result it was a single row and and single value,
        # hence access to [0][0]
        return _id[0][0]


def convert_from_id(value, table, id_col=None):
    """Converts an id value to its corresponding string value

    Parameters
    ----------
    value : int
        The id value to convert
    table : str
        The table that has the conversion
    id_col : str, optional
        Column holding the id value. Defaults to [table]_id.

    Returns
    -------
    str
        The string correspinding to the id

    Raises
    ------
    LookupError
        The passed id has no associated string
    """
    id_col = table + '_id' if id_col is None else id_col
    with TRN:
        sql = "SELECT {0} FROM barcodes.{0} WHERE {1} = %s".format(
            table, id_col)
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
        sql = "SELECT count(1) FROM barcodes.%s" % table
        TRN.add(sql)
        return TRN.execute_fetchlast()


def check_barcode_assigned(barcode):
    """Checks if barcode is already assigned to sample or project

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
    sql = """SELECT barcode, assigned_on, sample_set_id
        FROM barcodes.barcode
        LEFT JOIN barcodes.sample_set_barcodes USING (barcode)
        WHERE barcode = %s
        """
    with TRN:
        TRN.add(sql, [barcode])
        barcode_info = TRN.execute_fetchindex()
        if not barcode_info:
            raise ValueError('Barcode %s does not exist in the DB' % barcode)
        # Check if barcode retrieved has set assigned on date or not
        if barcode_info[0]['assigned_on'] is None and \
                barcode_info[0]['sample_set_id'] is None:
            return False
        return True


def get_barcodes(num_barcodes):
    """Gets a list of unassigned barcodes

    Parameters
    ----------
    num_barcodes : int
        Number of barcodes to return

    Returns
    -------
    list of str
        Barcodes

    Raises
    ------
    ValueError
        Number of barcodes requested excededs number of unassigned barcodes
    """
    sql = """SELECT DISTINCT barcode
             FROM barcodes.barcode
             LEFT JOIN barcodes.sample_set_barcodes USING (barcode)
             WHERE assigned_on IS NULL AND sample_set_id IS NULL
             ORDER BY barcode ASC LIMIT %s
          """
    with TRN:
        TRN.add(sql, [num_barcodes])
        barcodes = TRN.execute_fetchflatten()
        if len(barcodes) != num_barcodes:
            raise ValueError('%d barcodes requested, only %d available' %
                             (num_barcodes, len(barcodes)))
        return barcodes


def rollback_tests():
    """Decorator for rolling back tests as they finish"""
    def class_modifier(cls):
        with TRN:
            # First, we check that we are not in a production environment
            TRN.add("SELECT test FROM barcodes.settings")
            test_db = TRN.execute_fetchlast()
            if not test_db:
                raise RuntimeError("Working in a production environment. Not "
                                   "executing the tests to keep the production"
                                   " database safe.")

        # Now alter TRN so that it rolls back in test classes
        class DecoratedClass(cls):
            def setUp(self):
                # Add one extra context so we can rollback in tearDown
                TRN._contexts_entered = 1
                super(DecoratedClass, self).setUp()

            def tearDown(self):
                super(DecoratedClass, self).tearDown()
                TRN.rollback()
                TRN.__exit__(None, None, None)
        return DecoratedClass
    return class_modifier
