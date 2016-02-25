# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from passlib.hash import bcrypt

import platemap as pm


class Person(pm.base.PMObject):
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
        with pm.sql.TRN:
            if cls.exists(email):
                raise pm.exceptions.DuplicateError(email, 'person')

            pm.sql.TRN.add(sql, [name, email.lower(), address, affiliation,
                                 phone])
            person_id = pm.sql.TRN.execute_fetchlast()
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
                 SELECT * FROM barcodes.person WHERE LOWER(email) = %s)
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [email.lower()])
            return pm.sql.TRN.execute_fetchlast()

    def _get_property_person(self, column):
        sql = "Select {} from barcodes.person WHERE person_id = %s".format(
            column)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.sql.TRN.execute_fetchlast()

    def _set_property_person(self, column, value):
        sql = "UPDATE barcodes.person SET {} = %s WHERE person_id = %s".format(
            column)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [value, self.id])

    @property
    def name(self):
        return self._get_property_person('name')

    @name.setter
    def name(self, name):
        self._set_property_person('name', name)

    @property
    def email(self):
        return self._get_property_person('email')

    @email.setter
    def email(self, email):
        self._set_property_person('email', email)

    @property
    def address(self):
        return self._get_property_person('address')

    @address.setter
    def address(self, address):
        self._set_property_person('address', address)

    @property
    def affiliation(self):
        return self._get_property_person('affiliation')

    @affiliation.setter
    def affiliation(self, affiliation):
        self._set_property_person('affiliation', affiliation)

    @property
    def phone(self):
        return self._get_property_person('phone')

    @phone.setter
    def phone(self, phone):
        self._set_property_person('phone', phone)


class User(pm.base.PMObject):
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

        Raises
        ------
        DuplicateError
            Email or username already exist
        """
        person_sql = """INSERT INTO barcodes.person
                        (name, email, address, affiliation, phone)
                        VALUES (%s,%s,%s,%s,%s) RETURNING person_id
                     """
        user_sql = """INSERT INTO barcodes.user
                      (user_id, pass, access, person_id)
                      VALUES (%s,%s,%s, %s) RETURNING user_id
                     """
        access_sql = """SELECT SUM(access_value)
                        FROM barcodes.access_controls
                        WHERE access_level IN %s"""
        with pm.sql.TRN:
            if cls.exists(username, email):
                if Person.exists(email):
                    raise pm.exceptions.DuplicateError(email, 'person')
                else:
                    raise pm.exceptions.DuplicateError(username, 'user')

            pm.sql.TRN.add(person_sql, [name, email.lower(), address,
                           affiliation, phone])
            person_id = pm.sql.TRN.execute_fetchlast()

            # Convert list of access to integer sum for bit shift access checks
            if access is None:
                # 1 == Basic access
                access_int = 1
            else:
                pm.sql.TRN.add(access_sql, [tuple(access)])
                # Add 1 so don't have to specify basic access
                access_int = 1 + pm.sql.TRN.execute_fetchlast()
            encrypt_pass = bcrypt.encrypt(password)
            pm.sql.TRN.add(user_sql, [username, encrypt_pass, access_int,
                           person_id])
            user_id = pm.sql.TRN.execute_fetchlast()
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
                 SELECT * FROM barcodes.user
                 WHERE user_id = %s)
              """
        with pm.sql.TRN:
            if Person.exists(email):
                return True

            pm.sql.TRN.add(sql, [username])
            return pm.sql.TRN.execute_fetchlast()

    def _get_property_user(self, column):
        sql = "Select {} from barcodes.user WHERE user_id = %s".format(column)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.sql.TRN.execute_fetchlast()

    @property
    def person(self):
        """Gets associated Person object

        Returns
        -------
        Person object
            The person object associated with the user
        """
        return Person(self._get_property_user('person_id'))

    @property
    def access(self):
        return self._get_property_user('access')

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
        sql = "SELECT pass FROM barcodes.user WHERE user_id = %s"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            row = pm.sql.TRN.execute_fetchindex()
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
        sql = """SELECT (access & (
                    SELECT access_value
                    FROM barcodes.access_controls
                    WHERE access_level = %s)
                 ) != 0
                 FROM barcodes.user
                 WHERE user_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [action, self.id])
            return pm.sql.TRN.execute_fetchlast()

    def add_access(self, actions):
        """Adds ability for user to do action

        Parameters
        ----------
        action : list of str
            actions to add access for
        """
        sql = """UPDATE barcodes.user SET access = access + (
                     SELECT SUM(access_value)
                     FROM barcodes.access_controls
                     WHERE access_level IN %s)
                 WHERE user_id = %s
              """
        with pm.sql.TRN:
            # Only add actions the user does not already have access to
            add = [a for a in actions if not self.check_access(a)]
            if add:
                pm.sql.TRN.add(sql, [tuple(add), self.id])

    def remove_access(self, actions):
        """Removes ability for user to do action

        Parameters
        ----------
        action : lsit of str
            action to remove access for
        """
        sql = """UPDATE barcodes.user SET access = access - (
                     SELECT SUM(access_value)
                     FROM barcodes.access_controls
                     WHERE access_level IN %s)
                 WHERE user_id = %s
              """
        with pm.sql.TRN:
            # Make sure only removing actions the user has access to
            remove = [a for a in actions if self.check_access(a)]
            if remove:
                pm.sql.TRN.add(sql, [tuple(remove), self.id])
