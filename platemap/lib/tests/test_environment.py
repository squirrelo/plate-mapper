# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import TestCase, main

import platemap as pm


class TestEnvironment(TestCase):
    def tearDown(self):
        pm.environment.rebuilt_test_env()

    def test_make_database_exists(self):
        with self.assertRaises(OSError):
            pm.environment.make_database()

    def test_make_environment(self):
        pm.environment._drop_env()
        pm.environment.make_environment()
        obs = pm.webhelp.get_primer_sets()
        self.assertEqual(obs, [])

    def test_make_environment_test(self):
        pm.environment._drop_env()
        pm.environment.make_environment(True)
        obs = pm.webhelp.get_primer_sets()
        self.assertEqual(obs, [[1, 'Primer Set 1'], [2, 'Primer Set 2']])

    def test_rebuilt_test_env(self):
        pm.environment.rebuilt_test_env()
        obs = pm.webhelp.get_primer_sets()
        self.assertEqual(obs, [[1, 'Primer Set 1'], [2, 'Primer Set 2']])

    def test_drop_env(self):
        pm.environment._drop_env()
        with self.assertRaises(ValueError) as e:
            pm.webhelp.get_primer_sets()
            self.assertIn('relation "barcodes.primer_set" does not exist',
                          e.message)


if __name__ == '__main__':
    main()
