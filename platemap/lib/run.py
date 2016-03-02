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
        run : Run object
            The run to add the pool to
        person : Person object
            The person creating the pool

        Returns
        -------
        Pool object
            The new Pool
        """

    @staticmethod
    def exists(name, run):
        """Checks if a pool already exists for a run

        Parameters
        ----------
        name : str
            Name of the pool
        run : Run object
            The run the pool will be attached to

        Returns
        -------
        bool
            Whether the pool already exists (True) or not (False)
        """

    @staticmethod
    def delete(id_):
        """Removes a pool from the database

        Raises
        ------
        EditError
            The pool is already attached to a finalized Run
        """
        raise NotImplementedError()

    @property
    def name(self):
        return self._get_property('pool')

    @property
    def run(self):
        return Run(self._get_property('run_id'))

    @property
    def finalized(self):
        return self._get_property('finalized')

    def finalize(self):
        """Finalize the pool so no more plates/samples can be added"""

    def add_protocol(self, pcr_run):
        """Adds a PCR protocol run to the pool

        Parameters
        ----------
        pcr_run : PCRProtocol object
            The protocol to add to the pool

        Raises
        ------
        DuplicateError
            If the sequencing barcodes of the protocol match existing protocols
            in the pool
        """

    def remove_protocol(self, pcr_run):
        """Adds a PCR protocol run to the pool

        Parameters
        ----------
        pcr_run : PCRProtocol object
            The protocol to remove from the pool
        """


class Pool(pm.base.PMObject):
    _table = 'pool'

    @classmethod
    def create(cls, name, run, person):
        """Creates a new pool on the system

        Parameters
        ----------
        run : Run object
            The run to add the pool to
        person : Person object
            The person creating the pool

        Returns
        -------
        Pool object
            The new Pool
        """

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

    @staticmethod
    def delete(id_):
        """Removes a run from the database

        Raises
        ------
        EditError
            The run is already attached to a finalized Run
        """
        raise NotImplementedError()

    @property
    def name(self):
        return self._get_property('run')

    @property
    def pools(self):
        sql = "SELECT pool_id FROM barcodes.pool WHERE run_id = %s"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return [Pool(p) for p in pm.sql.TRN.execute_fetchflatten()]

    @property
    def finalized(self):
        return self._get_property('finalized')

    def finalize(self):
        """Finalize the run so no more pools can be added"""

    def add_pool(self, pool):
        """Adds a PCR protocol run to the pool

        Parameters
        ----------
        pool : Pool object
            The pool to add to the run
        """

    def remove_protocol(self, pool):
        """Adds a PCR protocol run to the pool

        Parameters
        ----------
        pool : Pool object
            The pool to remove from the run
        """

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
