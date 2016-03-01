# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from .exceptions import DeveloperError, UnknownIDError
from .sql_connection import TRN


class PMObject(object):
    r"""Base class for any plate mapper object

    Parameters
    ----------
    id_: int, long, str, or unicode
        The object id on the storage system

    Attributes
    ----------
    id

    Methods
    -------
    create
    delete
    exists
    _check_subclass
    _check_id
    __eq__
    __neq__

    Raises
    ------
    DeveloperError
        If trying to instantiate the base class directly
    """

    _table = None

    @classmethod
    def create(cls):
        r"""Creates a new object with a new id on the storage system

        Raises
        ------
        NotImplementedError
            If the method is not overwritten by a subclass
        """
        raise NotImplementedError()

    @classmethod
    def delete(cls, id_):
        r"""Deletes the object `id_` from the storage system

        Parameters
        ----------
        id_ : object
            The object identifier

        Raises
        ------
        NotImplementedError
            If the method is not overwritten by a subclass
        """
        raise NotImplementedError()

    @classmethod
    def exists(cls):
        r"""Checks if a given object info is already present on the DB

        Raises
        ------
        NotImplementedError
            If the method is not overwritten by a subclass
        """
        raise NotImplementedError()

    @classmethod
    def _check_subclass(cls):
        r"""Check that we are not calling a function that needs to access the
        database from the base class

        Raises
        ------
        DeveloperError
            If its called directly from a base class
        """
        if cls._table is None:
            raise DeveloperError(
                "Could not instantiate an object of the base class")

    def _check_id(self, id_):
        r"""Check that the provided ID actually exists on the database

        Parameters
        ----------
        id_ : object
            The ID to test

        Notes
        -----
        This function does not work for the User class. The problem is
        that the User sql layout doesn't follow the same conventions done in
        the other classes. However, still defining here as there is only one
        subclass that doesn't follow this convention and it can override this.
        """
        with TRN:
            sql = """SELECT EXISTS(
                        SELECT * FROM barcodes.{0}
                        WHERE {0}_id=%s)""".format(self._table)
            TRN.add(sql, [id_])
            return TRN.execute_fetchlast()

    def __init__(self, id_):
        r"""Initializes the object

        Parameters
        ----------
        id_: int, str
            the object identifier

        Raises
        ------
        UnknownIDError
            If `id_` does not correspond to any object
        """
        # Most IDs in the database are numerical, but some (e.g., IDs used for
        # the User object) are strings. Moreover, some integer IDs are passed
        # as strings (e.g., '5'). Therefore, explicit type-checking is needed
        # here to accommodate these possibilities.
        if not isinstance(id_, (int, str)):
            raise TypeError("id_ must be a numerical or text type (not %s) "
                            "when instantiating "
                            "%s" % (id_.__class__.__name__,
                                    self.__class__.__name__))

        with TRN:
            self._check_subclass()
            if not self._check_id(id_):
                raise UnknownIDError(id_, self._table)

        self._id = id_

    def __eq__(self, other):
        r"""Self and other are equal based on type and database id"""
        if type(self) != type(other):
            return False
        if other._id != self._id:
            return False
        return True

    def __ne__(self, other):
        r"""Self and other are not equal based on type and database id"""
        return not self.__eq__(other)

    def __hash__(self):
        r"""The hash of an object is based on the id"""
        return hash(str(self.id))

    def _get_property(self, column):
        sql = "SELECT {0} FROM barcodes.{1} WHERE {1}_id = %s".format(
            column, self._table)
        with TRN:
            TRN.add(sql, [self.id])
            return TRN.execute_fetchlast()

    def _set_property(self, column, value):
        sql = """UPDATE barcodes.{0}
                 SET {1} = %s
                 WHERE {0}_id = %s""".format(self._table, column)
        with TRN:
            TRN.add(sql, [value, self.id])

    @property
    def id(self):
        r"""The object id on the storage system"""
        return self._id
