# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import platemap as pm


class Project(pm.base.PMObject):
    _table = 'project'

    @classmethod
    def create(cls, project, description, person, pi, contact_person,
               sample_set, num_barcodes=None):
        """Creates a project and the initial sample set

        Parameters
        ----------
        project : str
            Name of the project
        description : str
            Description of the project and its goals
        person : Person object
            The person creating the project
        pi : str
            PI name
        contact_person : str
            Contact person in PI lab
        sample_set : str
            Name of the initial sample set
        num_barcodes : int, optional
            Number of barcodes to assign to the project

        Returns
        -------
        Project object
            New project

        Raises
        ------
        DuplicateError
            Project with same name already exists
        """
        if cls.exists(project):
            raise pm.exceptions.DuplicateError(project, 'project')

        project_sql = """INSERT INTO barcodes.project
                         (project, pi, contact_person)
                         VALUES (%s, %s, %s)
                         PRETURNING project_id
                      """
        project_bc_sql = """INSERT INTO barcodes.project_barcodes
                            (project_id, barcode)
                            values (%s, %s)
                         """
        sample_set_sql = """INSERT INTO barcodes.sample_set
                            (sample_set, created_by)
                            VALUES (%s, %s)
                        """
        with pm.sql.TRN:
            pm.sql.TRN.add(project_sql, [project, pi, contact_person])
            project_id = pm.sql.TRN.execute_fetchlast()
            pm.sql.TRN.add(sample_set_sql, [sample_set, person.id])

            if num_barcodes is not None:
                barcodes = pm.util.get_barcodes(num_barcodes)
                pm.sql.TRN.add(project_bc_sql,
                               [(project_id, b) for b in barcodes], many=True)

    @staticmethod
    def exists(project_name):
        """Checks whether a project already exists in the database

        Parameters
        ----------
        project_name : str
            Project to check if exists

        Returns
        -------
        bool
            Whether project exists (True) or not (False)
        """
        sql = """SELECT EXISTS(
                 SELECT * FROM barcodes.project WHERE project = %s)
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [project_name])
            return pm.sql.TRN.execute_fetchlast()

    @staticmethod
    def delete():
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def samples(self):
        raise NotImplementedError()

    @property
    def sample_sets(self):
        raise NotImplementedError()

    @property
    def pi(self):
        raise NotImplementedError()

    @pi.setter
    def pi(self, value):
        raise NotImplementedError()

    @property
    def contact(self):
        raise NotImplementedError()

    @contact.setter
    def contact(self, value):
        raise NotImplementedError()

    # ---------- functions ------------------
    def add_sample_set(self, sample_set, person):
        """Adds a new sample set to the project

        Parameters
        ----------
        sample_set : str
            The name of the new sample set
        person : Person object
            The person adding the new sample set

        Raises
        ------
        DuplicateError
            Sample set already exists
        """

    def remove_sample_set(self, sample_set):
        """Remove a sample set to the project

        Parameters
        ----------
        sample_set : str
            The name of the sample set to remove

        Raises
        ------
        EditError
            Trying to delete a sample set with samples attached
        """

    def assign_barcodes(self, num_barcodes):
        """Assigns barcodes to the project

        Parameters
        ----------
        num_barcodes : str
            Number of barcodes to assign to the project
        """

    def clear_barcodes(self):
        """Clears all remaining unused barcodes from the project"""
