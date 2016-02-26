# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import TestCase, main

import platemap as pm


@pm.util.rollback_tests()
class TestPerson(TestCase):
    def setUp(self):
        self.person1 = pm.person.Person(1)
        self.person2 = pm.person.Person(2)

    def test_create_minimal(self):
        obs = pm.person.Person.create('New Person', 'new@foo.bar')

        self.assertEqual(obs.name, 'New Person')
        self.assertEqual(obs.email, 'new@foo.bar')
        self.assertEqual(obs.address, None)
        self.assertEqual(obs.affiliation, None)
        self.assertEqual(obs.phone, None)

    def test_create_full(self):
        obs = pm.person.Person.create(
            'New Person', 'new@foo.bar', '111 fake street', 'UCSD', '112-2222')

        self.assertEqual(obs.name, 'New Person')
        self.assertEqual(obs.email, 'new@foo.bar')
        self.assertEqual(obs.address, '111 fake street')
        self.assertEqual(obs.affiliation, 'UCSD')
        self.assertEqual(obs.phone, '112-2222')

    def test_create_exists(self):
        with self.assertRaises(pm.exceptions.DuplicateError):
            pm.person.Person.create('New Person', 'test@foo.bar')

    def test_delete(self):
        pass

    def test_exists(self):
        obs = pm.person.Person.exists('test@foo.bar')
        self.assertTrue(obs)

        # Make sure it's case independent
        obs = pm.person.Person.exists('TEST@foo.bar')
        self.assertTrue(obs)

    def test_exists_no_exist(self):
        obs = pm.person.Person.exists('NO@EXISTS.com')
        self.assertFalse(obs)

    def test_get_name(self):
        self.assertEqual(self.person1.name, 'First test person')

    def test_set_name(self):
        self.person1.name = 'Changed name'
        self.assertEqual(self.person1.name, 'Changed name')

    def test_get_email(self):
        self.assertEqual(self.person1.email, 'test@foo.bar')

    def test_set_email(self):
        self.person1.email = 'changed@new.com'
        self.assertEqual(self.person1.email, 'changed@new.com')

    def test_get_address(self):
        self.assertEqual(self.person1.address, '123 fake street')
        self.assertEqual(self.person2.address, None)

    def test_set_address(self):
        self.person1.address = '123 changed street'
        self.assertEqual(self.person1.address, '123 changed street')

    def test_get_affiliation(self):
        self.assertEqual(self.person1.affiliation, 'UCSD')
        self.assertEqual(self.person2.affiliation, None)

    def test_set_affiliation(self):
        self.person1.affiliation = 'Changed University'
        self.assertEqual(self.person1.affiliation, 'Changed University')

    def test_get_phone(self):
        self.assertEqual(self.person1.phone, '111-111-1111')
        self.assertEqual(self.person2.phone, None)

    def test_set_phone(self):
        self.person1.phone = '222-3333'
        self.assertEqual(self.person1.phone, '222-3333')


@pm.util.rollback_tests()
class TestUser(TestCase):
    def setUp(self):
        self.user1 = pm.person.User('User1')

    def test_create_minimal(self):
        obs = pm.person.User.create('NewUser', 'newpass', 'New Person',
                                    'new@foo.bar')

        self.assertEqual(obs.id, 'NewUser')
        self.assertEqual(obs.access, 1)
        self.assertTrue(obs.authenticate('newpass'))

        person = obs.person
        self.assertEqual(person.name, 'New Person')
        self.assertEqual(person.email, 'new@foo.bar')
        self.assertEqual(person.address, None)
        self.assertEqual(person.affiliation, None)
        self.assertEqual(person.phone, None)

    def test_create_full(self):
        obs = pm.person.User.create(
            'NewUser', 'newpass', 'New Person', 'new@foo.bar',
            '111 fake street', 'UCSD', '112-2222',
            ['Create samples', 'Create protocol runs'])

        self.assertEqual(obs.id, 'NewUser')
        self.assertEqual(obs.access, 11)
        self.assertTrue(obs.authenticate('newpass'))

        person = obs.person
        self.assertEqual(person.name, 'New Person')
        self.assertEqual(person.email, 'new@foo.bar')
        self.assertEqual(person.address, '111 fake street')
        self.assertEqual(person.affiliation, 'UCSD')
        self.assertEqual(person.phone, '112-2222')

    def test_create_exists(self):
        with self.assertRaises(pm.exceptions.DuplicateError):
            pm.person.User.create('NewUser', 'newpass', 'New Person',
                                  'test@foo.bar')

        with self.assertRaises(pm.exceptions.DuplicateError):
            pm.person.User.create('User1', 'newpass', 'New Person',
                                  'new@foo.bar')

    def test_delete(self):
        pass

    def test_exists(self):
        self.assertTrue(pm.person.User.exists('User1', 'new@email.com'))
        self.assertTrue(pm.person.User.exists('New User', 'test@foo.bar'))
        self.assertTrue(pm.person.User.exists('New User', 'TEST@foo.BAR'))

    def test_exists_no_exist(self):
        self.assertFalse(pm.person.User.exists('New User', 'new@email.com'))

    def test_person(self):
        self.assertEqual(self.user1.person, pm.person.Person(1))

    def test_authenticate(self):
        self.assertTrue(self.user1.authenticate('password'))

    def test_authenticate_bad_pass(self):
        self.assertFalse(self.user1.authenticate('BADPASS'))

    def test_check_access(self):
        self.assertTrue(self.user1.check_access('Create samples'))

    def test_check_access_no_access(self):
        self.assertFalse(self.user1.check_access('Create runs'))

    def test_add_access(self):
        self.user1.add_access(['Create samples'])
        self.assertEqual(self.user1.access, 7)

        self.user1.add_access(['Generate prep metadata', 'Create runs'])
        self.assertEqual(self.user1.access, 55)

    def test_remove_access(self):
        self.user1.remove_access(['Generate prep metadata'])
        self.assertEqual(self.user1.access, 7)

        self.user1.remove_access(['Generate prep metadata', 'Edit samples'])
        self.assertEqual(self.user1.access, 3)


if __name__ == "__main__":
    main()
