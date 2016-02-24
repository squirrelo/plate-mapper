from unittest import TestCase, main

import platemap.lib


@platemap.lib.util.rollback_tests()
class TestPerson(TestCase):
    def setUp(self):
        self.person1 = platemap.lib.Person(1)
        self.person2 = platemap.lib.Person(2)

    def test_create_minimal(self):
        obs = platemap.lib.Person.create('New Person', 'new@foo.bar')

        self.assertEqual(obs.name, 'New Person')
        self.assertEqual(obs.email, 'new@foo.bar')
        self.assertEqual(obs.address, None)
        self.assertEqual(obs.affiliation, None)
        self.assertEqual(obs.phone, None)

    def test_create_full(self):
        obs = platemap.lib.Person.create(
            'New Person', 'new@foo.bar', '111 fake street', 'UCSD', '112-2222')

        self.assertEqual(obs.name, 'New Person')
        self.assertEqual(obs.email, 'new@foo.bar')
        self.assertEqual(obs.address, '111 fake street')
        self.assertEqual(obs.affiliation, 'UCSD')
        self.assertEqual(obs.phone, '112-2222')

    def test_delete(self):
        pass

    def test_exists(self):
        obs = platemap.lib.Person.exists('test@foo.bar')
        self.assertTrue(obs)

        # Make sure it's case independent
        obs = platemap.lib.Person.exists('TEST@foo.bar')
        self.assertTrue(obs)

    def test_exists_no_exist(self):
        obs = platemap.lib.Person.exists('NO@EXISTS.com')
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


@platemap.lib.util.rollback_tests()
class TestUser(TestCase):
    def setUp(self):
        self.user1 = platemap.lib.User('User1')

    def test_create_minimal(self):
        obs = platemap.lib.User.create('NewUser', 'newpass', 'New Person',
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
        obs = platemap.lib.User.create(
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

    def test_delete(self):
        pass

    def test_exists(self):
        self.assertTrue(platemap.lib.User.exists('User1', 'new@email.com'))
        self.assertTrue(platemap.lib.User.exists('New User', 'test@foo.bar'))
        self.assertTrue(platemap.lib.User.exists('New User', 'TEST@foo.BAR'))

    def test_exists_no_exist(self):
        self.assertFalse(platemap.lib.User.exists('New User', 'new@email.com'))

    def test_person(self):
        self.assertEqual(self.user1.person, platemap.lib.Person(1))

    def test_authenticate(self):
        self.assertTrue(self.user1.authenticate('password'))

    def test_authenticate_bad_pass(self):
        self.assertFalse(self.user1.authenticate('BADPASS'))

    def test_check_access(self):
        pass

    def test_check_access_no_access(self):
        pass

    def test_add_access(self):
        pass

    def test_remove_access(self):
        pass


if __name__ == "__main__":
    main()
