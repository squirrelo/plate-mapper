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
        if num_barcodes is not None:
            barcodes = pm.util.get_barcodes(num_barcodes)

        project_sql = """INSERT INTO barcodes.project
                         (project, pi, description, contact_person)
                         VALUES (%s, %s, %s, %s)
                         RETURNING project_id
                      """
        project_bc_sql = """INSERT INTO barcodes.project_barcodes
                            (project_id, barcode)
                            values (%s, %s)
                         """
        sample_set_sql = """INSERT INTO barcodes.sample_set
                            (sample_set, created_by)
                            VALUES (%s, %s)
                            RETURNING sample_set_id
                        """
        proj_sample_set_sql = """INSERT INTO barcodes.project_sample_sets
                                 (project_id, sample_set_id)
                                 VALUES (%s, %s)
                              """
        with pm.sql.TRN:
            pm.sql.TRN.add(project_sql, [project, pi, description,
                                         contact_person])
            project_id = pm.sql.TRN.execute_fetchlast()

            if num_barcodes is not None:
                pm.sql.TRN.add(project_bc_sql,
                               [(project_id, b) for b in barcodes], many=True)

            pm.sql.TRN.add(sample_set_sql, [sample_set, person.id])
            sample_set_id = pm.sql.TRN.execute_fetchlast()
            pm.sql.TRN.add(proj_sample_set_sql, [project_id, sample_set_id])

        return cls(project_id)

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

    # --------- properties -------------------
    @property
    def name(self):
        return self._get_property('project')

    @property
    def description(self):
        return self._get_property('description')

    @property
    def samples(self):
        sql = """SELECT sample_id
                 FROM barcodes.project_samples
                 WHERE project_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return [pm.sample.Sample(s) for s in
                    pm.sql.TRN.execute_fetchflatten()]

    @property
    def sample_sets(self):
        sql = """SELECT sample_set
                 FROM barcodes.project_sample_sets
                 JOIN barcodes.sample_set USING (sample_set_id)
                 WHERE project_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.sql.TRN.execute_fetchflatten()

    @property
    def pi(self):
        return self._get_property('pi')

    @pi.setter
    def pi(self, value):
        self._set_property('pi', value)

    @property
    def contact(self):
        return self._get_property('contact_person')

    @contact.setter
    def contact(self, value):
        self._set_property('contact_person', value)

    # ---------- functions ------------------
    def add_samples(self, samples):
        """Add samples not part of the initial sample set to the project

        Parameters
        ----------
        samples : list of Sample objects
            Samples to add to the project
        """
        sql = """INSERT INTO barcodes.project_samples
                 (project_id, sample_id)
                 VALUES (%s, %s)
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [(self.id, s.id) for s in samples], many=True)

    def remove_samples(self, samples):
        """Remove samples from the project

        Parameters
        ----------
        samples : list of Sample objects
            Samples to remove from the project
        """
        sql = """DELETE FROM barcodes.project_samples
                 WHERE project_id = %s AND sample_id IN %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id, tuple(s.id for s in samples)])

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
        sql1 = """INSERT INTO barcodes.sample_set
                  (sample_set, created_by) VALUES (%s, %s)
                  RETURNING sample_set_id
               """
        sql2 = """INSERT INTO barcodes.project_sample_sets
                  (project_id, sample_set_id)
                  VALUES (%s, %s)
               """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql1, [sample_set, person.id])
            sample_set_id = pm.sql.TRN.execute_fetchlast()
            pm.sql.TRN.add(sql2, [self.id, sample_set_id])

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
        check_sql = """SELECT count(*)
                       FROM barcodes.project_sample_sets
                       WHERE project_id = %s AND sample_set_id NOT IN (
                           SELECT sample_set_id
                           FROM barcodes.sample_set
                           WHERE sample_set = %s)
                    """
        remove_sql = """DELETE FROM barcodes.project_sample_sets
                        WHERE project_id = %s AND sample_set_id IN (
                           SELECT sample_set_id
                           FROM barcodes.sample_set
                           WHERE sample_set = %s)
                     """
        with pm.sql.TRN:
            pm.sql.TRN.add(check_sql, [self.id, sample_set])
            if pm.sql.TRN.execute_fetchlast() == 0:
                raise pm.exceptions.EditError('Can not remove all sample sets '
                                              'attached to a project')
            pm.sql.TRN.add(remove_sql, [self.id, sample_set])

    def assign_barcodes(self, num_barcodes):
        """Assigns barcodes to the project

        Parameters
        ----------
        num_barcodes : str
            Number of barcodes to assign to the project
        """
        sql = """INSERT INTO barcodes.project_barcodes (project_id, barcode)
                 VALUES (%s, %s)
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [(self.id, b) for b in
                                 pm.util.get_barcodes(num_barcodes)],
                           many=True)

    def clear_barcodes(self):
        """Clears all remaining unused barcodes from the project"""
        sql = """DELETE FROM barcodes.project_barcodes
                 WHERE barcode NOT IN (SELECT barcode FROM barcodes.sample
                                       WHERE barcode IS NOT NULL)
                 AND project_id = %s"""
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
