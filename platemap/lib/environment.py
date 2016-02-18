# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from os.path import join, abspath, dirname

from psycopg2 import connect

from platemap.lib.config_manager import pm_config
from platemap.lib.sql_connection import TRN


def _check_db_exists(db, conn_handler):
    """Checks if the database db exists on the postgres server

    Parameters
    ----------
    db : str
        The database
    conn_handler : SQLConnectionHandler
        The connection to the database
    """
    conn_handler.execute('SELECT datname FROM pg_database')
    dbs = conn_handler.fetchall()

    # It's a list of tuples, so just create the tuple to check if exists
    return (db,) in dbs


def make_database():
    """Creates the database on the system"""
    # Connect to the postgres server
    connection = connect(user=pm_config.user,
                         password=pm_config.password,
                         host=pm_config.host,
                         port=pm_config.port)
    connection.autocommit = True

    with connection.cursor() as c:
        # Check that it does not already exists
        if _check_db_exists(pm_config.database, c):
            raise EnvironmentError(
                "Database %s already present on the system" %
                pm_config.database)

        # Create the database
        c.execute('CREATE DATABASE %s' % pm_config.database)

    connection.close()


def make_environment(test=True):
    """Sets up the database with the schema and optionally test information

    Parameters
    ----------
    test : bool, optional
        Whether the environment will be set up as test or not. Default True
    """
    with TRN:
        with open(join(dirname(abspath(__file__)), '..', 'db',
                       'platemapper.sql')) as f:
            TRN.add(f.read())
