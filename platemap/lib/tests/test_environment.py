# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import TestCase, main

from psycopg2 import connect, ProgrammingError

from platemap.lib.config_manager import pm_config
import platemap as pm


def _wipe_db(db_name):
    connection = connect(user=pm_config.user,
                         password=pm_config.password,
                         host=pm_config.host,
                         port=pm_config.port)
    connection.autocommit = True
    # drop the database
    with connection.cursor() as c:
        c.execute('DROP DATABASE %s' % db_name)
    connection.commit()
    connection.close()


class TestEnvironment(TestCase):
    db = pm_config.database

    def setUp(self):
        self.test_db = 'pmtestDB48903257834920'
        pm_config.database = self.test_db

    def tearDown(self):
        _wipe_db(self.test_db)
        pm_config.database = self.db

    def test_make_database(self):
        pm.environment.make_database()
        obs = pm.webhelp.get_primer_sets()
        self.assertEqual(obs, [])

    def test_make_database_exists(self):
        pm.environment.make_database()
        with self.assertRaises(ProgrammingError):
            pm.environment.make_database()

    def test_make_environment(self):
        pm.environment.make_database()
        pm.environment.make_environment()
        obs = pm.webhelp.get_primer_sets()
        self.assertEqual(obs, [])

    def test_make_environment_test(self):
        pm.environment.make_database()
        pm.environment.make_environment(True)
        obs = pm.webhelp.get_primer_sets()
        self.assertEqual(obs, [[1, 'Primer Set 1'], [2, 'Primer Set 2']])

    def test_rebuilt_test_env(self):
        pm.environment.make_database()
        pm.environment.rebuilt_test_env()


if __name__ == '__main__':
    main()
