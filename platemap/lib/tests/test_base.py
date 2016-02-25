# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import TestCase, main

import platemap as pm


@pm.util.rollback_tests()
class QiitaBaseTest(TestCase):
    """Tests that the base class functions act correctly"""

    def setUp(self):
        # We need an actual subclass in order to test the equality functions
        self.tester = pm.sample.Sample(1)

    def test_init_base_error(self):
        """Raises an error when instantiating a base class directly"""
        with self.assertRaises(pm.exceptions.DeveloperError):
            pm.base.PMObject(1)

    def test_init_error_inexistent(self):
        """Raises an error when instantiating an object that does not exists"""
        with self.assertRaises(pm.exceptions.UnknownIDError):
            pm.sample.Sample(20)

    def test_check_subclass(self):
        """Nothing happens if check_subclass called from a subclass"""
        self.tester._check_subclass()

    def test_check_subclass_error(self):
        """check_subclass raises an error if called from a base class"""
        # Checked through the __init__ call
        with self.assertRaises(pm.exceptions.DeveloperError):
            pm.base.PMObject(1)

    def test_check_id(self):
        """Correctly checks if an id exists on the database"""
        self.assertTrue(self.tester._check_id(1))
        self.assertFalse(self.tester._check_id(100))

    def test_equal_self(self):
        """Equality works with the same object"""
        self.assertEqual(self.tester, self.tester)

    def test_equal(self):
        """Equality works with two objects pointing to the same instance"""
        new = pm.sample.Sample(1)
        self.assertEqual(self.tester, new)

    def test_not_equal(self):
        """Not equals works with object of the same type"""
        s2 = pm.sample.Sample(2)
        self.assertNotEqual(self.tester, s2)

    def test_not_equal_type(self):
        """Not equals works with object of different type"""
        new = pm.person.Person(1)
        self.assertNotEqual(self.tester, new)

if __name__ == '__main__':
    main()
