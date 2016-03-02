# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import platemap as pm


class Run(pm.base.PMObject):
    _table = 'run'

    @classmethod
    def create(cls, name, person):
        """Creates a new pool on the system

        Parameters
        ----------
        name : str
            The name for the run
        person : Person object
            The person creating the run

        Returns
        -------
        Run object
            The new Run

        Raises
        ------
        DuplicateError
            A run with that name already exists
        """
        if cls.exists(name):
            raise pm.exceptions.DuplicateError(name, 'run')
        sql = "INSERT INTO barcodes.run (run, created_by) VALUES (%s, %s)"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [name, person.id])

    @staticmethod
    def exists(name):
        """Checks if a run already exists

        Parameters
        ----------
        name : str
            Name of the run

        Returns
        -------
        bool
            Whether the run already exists (True) or not (False)
        """
        sql = "SELECT EXISTS(SELECT * FROM barcodes.run WHERE name = %s"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [name])
            return pm.sql.TRN.execute_fetchlast()

    @staticmethod
    def delete(id_):
        """Removes a run from the database

        Raises
        ------
        EditError
            The run is already finalized
        """
        raise NotImplementedError()

    @property
    def name(self):
        return self._get_property('pool')

    @property
    def pools(self):
        sql = "SELECT pool_id FROM barcodes.pool WHERE run_id = %s"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return [Pool(p) for p in pm.sql.TRN.execute_fetchflatten()]

    @property
    def finalized(self, person):
        return self._get_property('finalized')

    def finalize(self, person):
        """Finalize the run so no more pools can be added

        Parameters
        ----------
        person : Person object
            Person finalizing the run
        """
        sql = """UPDATE barcodes.run
                 SET finalized = TRUE, finalized_on = NOW(), finalized_by = %s
                 WHERE run_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [person.id, self.id])

    def generate_prep_metadata(self):
        """Creates the prep metadata file for the run

        Returns
        -------
        str
            The contents of the prep metadata file

        Raises
        ------
        DevelperError
            Trying to generate a prep template on a non-finalized run
        """
        if not self.finalized:
            raise pm.exceptions.DeveloperError('Generating prep metadata for '
                                               'non-finalized run!')


class Pool(pm.base.PMObject):
    _table = 'pool'

    @classmethod
    def create(cls, name, run, person):
        """Creates a new pool on the system

        Parameters
        ----------
        name : str
            The name for the pool
        run : Run object
            The run to add the pool to
        person : Person object
            The person creating the pool

        Returns
        -------
        Pool object
            The new Pool

        Raises
        ------
        DuplicateError
            The pool already exists for a given Run
        """
        if cls.exists(name, run):
            raise pm.exceptions.DuplicateError('name', 'pool')
        sql = """INSERT INTO barcodes.pool (run_id, pool, created_by)
                 VALUES (%s, %s, %s)
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [run.id, name, person.id])

    @staticmethod
    def exists(name, run):
        """Checks if a pool already exists

        Parameters
        ----------
        name : str
            Name of the pool
        run : Run object
            The run the pool is being attached to


        Returns
        -------
        bool
            Whether the pool already exists (True) or not (False)
        """

    @staticmethod
    def delete(id_):
        """Removes a run from the database

        Raises
        ------
        EditError
            The run is already finalized or attached to a finalized Run
        """
        raise NotImplementedError()

    @property
    def name(self):
        return self._get_property('pool')

    @property
    def run(self):
        return Run(self._get_property('run'))

    @property
    def finalized(self):
        return self._get_property('finalized')

    def finalize(self):
        """Finalize the run so no more pools can be added"""

    def add_protocol(self, pool):
        """Adds a PCR protocol run to the pool

        Parameters
        ----------
        pool : Pool object
            The pool to add to the run

        Raises
        ------
        DeveloperError
            Trying to add a pool that is not finalized
        """
        if not pool.finalized:
            raise pm.exceptions.DeveloperError('Adding non-finalized pool!')

    def remove_protocol(self, pool):
        """Adds a PCR protocol run to the pool

        Parameters
        ----------
        pool : Pool object
            The pool to remove from the run
        """
