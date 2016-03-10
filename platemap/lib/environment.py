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
        c.execute('SELECT datname FROM pg_database')
        dbs = c.fetchall()

        # It's a list of tuples, so just create the tuple to check if exist
        if (pm_config.database,) in dbs:
            raise EnvironmentError(
                "Database %s already present on the system" %
                pm_config.database)

        # Create the database
        c.execute('CREATE DATABASE %s' % pm_config.database)
    connection.close()


def make_environment(test=False):
    """Sets up the database with the schema and optionally test information

    Parameters
    ----------
    test : bool, optional
        Whether the environment will be set up as test or not. Default False
    """
    with TRN:
        print('Creating schema')
        with open(join(dirname(abspath(__file__)), '..', 'db',
                       'platemapper.sql')) as f:
            TRN.add(f.read())
        print('Initializing schema')
        with open(join(dirname(abspath(__file__)), '..', 'db',
                       'initialize.sql')) as f:
            TRN.add(f.read())
        if test:
            print('Populating test data')
            with open(join(dirname(abspath(__file__)), '..', 'db',
                      'populate_test.sql')) as f:
                TRN.add(f.read())


def rebuilt_test_env():
    """Deletes the schema and rebuilds the test database"""
    with TRN:
        print('Dropping barcodes schema')
        TRN.add('DROP SCHEMA IF EXISTS barcodes CASCADE')
        print('Rebuilding test environment')
        make_environment(test=True)
