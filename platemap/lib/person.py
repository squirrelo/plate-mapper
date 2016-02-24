# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from passlib.hash import bcrypt

from .base import PMObject
from .exceptions import DuplicateError
from .sql_connection import TRN


class Person(PMObject):
    _table = 'person'

    @classmethod
    def create(cls, name, email, address=None, affiliation=None, phone=None):
        r"""Creates a new person in the system

        Parameters
        ----------
        name : str
            Person's name
        email : str
            Person's email
        address : str, optional
            Person's complete address
        affiliation : str
            Person's place of work
        phone : str, optional
            Person's phone number

        Returns
        -------
        Person
            New Person object
        """
        sql = """INSERT INTO barcodes.person
                 (name, email, address, affiliation, phone)
                 VALUES (%s,%s,%s,%s,%s) RETURNING person_id
              """
        with TRN:
            if cls.exists(email):
                raise DuplicateError(email, 'person')

            TRN.add(sql, [name, email, address, affiliation, phone])
            person_id = TRN.execute_fetchlast()
            return cls(person_id)

    @classmethod
    def delete(cls, id_):
        r"""Deletes the person

        Parameters
        ----------
        id_ : int
            The id of person to delete

        Raises
        ------
        DeveloperError
            Person is attached to a User
        """
        raise NotImplementedError()

    @staticmethod
    def exists(email):
        r"""Checks if a person with the email address is already registered

        Parameters
        ----------
        email : str
            Email to check

        Returns
        -------
        bool
            If the person exists (True) or not (False)
        """
        sql = """SELECT EXISTS(
                 SELECT * FROM barcodes.person WHERE email = %s)
              """
        with TRN:
            TRN.add(sql, [email])
            return TRN.execute_fetchlast()

    def _get_property_person(self, column):
        sql = "Select {} from barcodes.person WHERE person_id = %s".format(
            column)
        with TRN:
            TRN.add(sql, [self.id])
            return TRN.execute_fetchlast()

    @property
    def name(self):
        return self._get_property_person('name')

    @name.setter
    def name(self, name):
        return self._name

    @property
    def email(self):
        return self._get_property_person('email')

    @email.setter
    def email(self, email):
        return self._email

    @property
    def address(self):
        return self._get_property_person('address')

    @address.setter
    def address(self, address):
        return self._address

    @property
    def affiliation(self):
        return self._get_property_person('affiliation')

    @affiliation.setter
    def affiliation(self, affiliation):
        return self._affiliation

    @property
    def phone(self):
        return self._get_property_person('phone')

    @phone.setter
    def phone(self, phone):
        return self._phone


class User(PMObject):
    _table = 'user'

    @classmethod
    def create(cls, username, password, name, email, address=None,
               affiliation=None, phone=None, access=None):
        r"""Creates a new person in the system

        Parameters
        ----------
        username : str
            Username for user
        password : str
            Plain text password for user
        name : str
            Person's name
        email : str
            Person's email
        address : str, optional
            Person's complete address
        affiliation : str
            Person's place of work
        phone : str, optional
            Person's phone number
        access : list of str
            What functions user has access to. If not given, basic access only

        Returns
        -------
        User
            New User object
        """
        person_sql = """INSERT INTO barcodes.person
                        (name, email, address, affiliation, phone)
                        VALUES (%s,%s,%s,%s,%s) RETURNING person_id
                     """
        user_sql = """INSERT INTO barcodes.user
                      (username, pass, access, person_id)
                      VALUES (%s,%s,%s, %s) RETURNING user_id
                     """
        access_sql = """SELECT SUM(access_value)
                        FROM barcodes.access_controls
                        WHERE access_level IN %s"""
        with TRN:
            if cls.exists(email):
                raise DuplicateError(email, 'person')

            TRN.add(person_sql, [name, email, address, affiliation, phone])
            person_id = TRN.execute_fetchlast()

            # Convert list of access to integer sum for bit shift access checks
            if access is None:
                access_int = 1
            else:
                TRN.add(access_sql, access)
                access_int = TRN.execute_fetchindex()
            encrypt_pass = bcrypt.encrypt(password)
            TRN.add(user_sql, [username, encrypt_pass, access_int, person_id])
            user_id = TRN.execute_fetchlast()
            return cls(user_id)

    @classmethod
    def delete(cls, id_):
        r"""Deletes the person

        Parameters
        ----------
        id_ : int
            The id of person to delete

        Raises
        ------
        DeveloperError
            Person is attached to a User
        """
        raise NotImplementedError()

    @staticmethod
    def exists(username, email):
        r"""Check if a person with the username or email address already exists

        Parameters
        ----------
        username : str
            Username to check
        email : str
            Email to check

        Returns
        -------
        bool
            If the person exists (True) or not (False)
        """
        sql = """SELECT EXISTS(
                 SELECT count(1) FROM barcodes.username
                 JOIN barcodes.person_id USING (person_id)
                 WHERE username = %s AND email = %s)
              """
        with TRN:
            TRN.add(sql, [username, email])
            return TRN.execute_fetchlast()

    @property
    def person(self):
        """Gets associated Person object

        Returns
        -------
        Person object
            The person object associated with the user
        """
        sql = "SELECT person_id FROM barcodes.user WHERE username = %s"
        with TRN:
            TRN.add(sql, self.id)
            return Person(TRN.execute_fetchlast())

    # ---------- Functions --------------
    def authenticate(self, password):
        """Authenticate a password for the user

        Parameters
        ----------
        password : str
            Plain text password to test against

        Returns
        -------
        bool
            If the password matches (True) or not (False)
        """
        sql = "SELECT pass FROM barcodes.user WHERE username = %s"
        with TRN:
            TRN.add(sql, [self.id])
            row = TRN.execute_fetchindex()
            if not row:
                return False

            results = row[0]
            return bcrypt.verify(password, results['pass'])

    def check_access(self, action):
        """Checks if user has access for action specified

        Parameters
        ----------
        action : str
            action to check access for

        Returns
        -------
        bool
            If the action is allowed (True) or not (False)
        """
        pass

    def add_access(self, action):
        """Adds ability for user to do action

        Parameters
        ----------
        action : str
            action to add access for
        """
        pass

    def remove_access(self, action):
        """Removes ability for user to do action

        Parameters
        ----------
        action : str
            action to remove access for
        """
        pass
