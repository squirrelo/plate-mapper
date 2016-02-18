# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from .base import PMObject
from .util import convert_to_id, check_barcode_assigned
from .sql_connection import TRN
from .exceptions import DeveloperError, DuplicateError, AssignError


class Sample(PMObject):
    @staticmethod
    def search(biomass_remaining=None, sample_type=None, barcode=None,
               project=None, primer_set=None, status=None, protocol=None):
        """Searches over all given parameters for matching samples

        Parameters
        ----------
        biomass_remaining : bool, optional
            Whether physical sample remains
        sample_type : str, optional
            What sampel type to look for (stool, etc)
        barcode : str, optional
            barcode to get
        project : str, optional
            project to search over
        primer_set : str, optional
            What primers were used for sample amplification
        status : str, optional
            What stage of processing this has made it to
        protocol : str
            What protocol was run on the samples

        Returns
        -------
        list of Sample objects
            What samples mach search criteria

        Notes
        -----
        While all parameters are optional, at least one must be passed in

        Raises
        ------
        DeveloperError
            No parameters passed in
        """
        # Make sure at least one argument passed
        if all([x is None for x in [biomass_remaining, sample_type, barcode,
                                    project, primer_set, status, protocol]]):
            raise DeveloperError("Must pass at least one parameter")

    @classmethod
    def create(cls, external_name, sample_type, sample_location, projects,
               person, barcode=None):
        """Creates a new sample in the database

        Parameters
        ----------
        external_name : str
            Common name of the sample
        sample_type : str
            What the sample is (stool, etc)
        sample_location : str
            Where th esample is physically located/stored
        projects : list of str
            What projects the sample is part of
        person  : Person object
            The person initially logging the sample
        barcode : str, optional
            If barcoded, the barcode added

        Returns
        -------
        Sample object
            The new sample
        """
        sample_sql = """INSERT INTO barcodes.samples
                        (external_name, barcode, sample_type, sample_location,
                         created_by, last_scanned_by)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        RETURNING sample_id
                     """
        project_sql = """INSERT INTO barcodes.project_external_name
                         (external_name, project_id)
                         VALUES (%s,%s)"""
        barcode_sql = """UPDATE barcodes.barcode
                         SET assigned_on = NOW()
                         WHERE barcode = %s
                      """
        with TRN:
            if cls.exists(external_name, barcode):
                raise DuplicateError(external_name, 'samples')

            TRN.add(sample_sql, [external_name, barcode, sample_type,
                                 sample_location, person.id, person.id])
            sample_id = TRN.execute_fetchlast()

            pids = [(external_name, convert_to_id(p, 'projects'))
                    for p in projects]
            TRN.add(project_sql, pids, many=True)

            if barcode is not None:
                TRN.add(barcode_sql, [barcode])
            TRN.execute()
            return cls(sample_id)

    @staticmethod
    def exists(external_name, barcode=None):
        pass

    @staticmethod
    def delete(id_):
        pass

    # ----------Properties---------------
    def _get_property(self, column):
        sql = "Select {} from barcodes.samples WHERE sample_id = %s".format(
            column)
        with TRN:
            TRN.add(sql, [self.id])
            return TRN.execute_fetchlast()

    @property
    def name(self):
        return self._get_property('external_name')

    @property
    def barcode(self):
        """Gets barcode assigned to sample, if there is one

        Returns
        -------
        str or None
            Barcode if assigned, else None
        """
        return self._get_property('barcode')

    @barcode.setter
    def barcode(self, barcode):
        """Sets barcode for sample if allowed

        Parameters
        ----------
        barcode : str
            Barcode to assign

        Raises
        ------
        ValueError
            Barcode does not exist in DB
            Barcode already assigned
        AssignError
            Barcode already assigned to this sample
        """
        sample_sql = """UPDATE barcodes.sample
                        SET barcode = %s
                        WHERE sample_id = %s
                     """
        barcode_sql = """UPDATE barcodes.barcode
                         SET assigned_on = NOW()
                         WHERE barcode = %s
                      """
        with TRN:
            if check_barcode_assigned(barcode):
                raise ValueError("Barcode %s already assigned" % barcode)
            if self.barcode is not None:
                raise AssignError('Barcode already assigned to this sample')
            TRN.add(sample_sql, [barcode, self.id])
            TRN.add(barcode_sql, [barcode])
            TRN.execute()

    @property
    def projects(self):
        """Returns list of projects this sample is associated with

        Returns
        -------
        list of str
            Projects the sample is associated with
        """
        sql = """SELECT DISTINCT project
                 FROM barcodes.samples
                 LEFT JOIN barcodes.project_sample USING (sample_id)
                 LEFT JOIN barcodes.projects USING (project_id)
                 WHERE sample_id = %s
              """
        with TRN:
            TRN.add(sql, [self.id])
            return TRN.execute_fetchflatten()

    @property
    def sample_type(self):
        return self._get_property('sample_type')

    @property
    def sample_location(self):
        return self._get_property('sample_location')

    @property
    def biomass_remaining(self):
        return self._get_property('biomass_remaining')

    @property
    def created_on(self):
        return self._get_property('created_on')

    @property
    def created_by(self):
        return self._get_property('created_by')

    @property
    def last_scanned(self):
        return self._get_property('last_scanned')

    @property
    def last_scanned_by(self):
        return self._get_property('last_scanned_by')

    @property
    def plates(self):
        sql = """SELECT plate_barcode
                 FROM barcodes.plates_samples
                 WHERE sample_id = %s
              """
        with TRN:
            TRN.add(sql, [self.id])
            return TRN.execute_fetchflatten()

    @property
    def protocols(self):
        raise NotImplementedError()

    @property
    def pools(self):
        raise NotImplementedError()

    @property
    def runs(self):
        raise NotImplementedError()

    # ---------------Functions---------------
    def add_project(self, project):
        sql = """INSERT INTO barcodes.project_sample (project_id, sample_id)
                 VALUES (%s, %s)
              """
        with TRN:
            if project in self.projects:
                return
            pid = convert_to_id(project, 'barcodes.project')
            TRN.add(sql, [pid, self.id])
            TRN.execute()

    def remove_project(self, project):
        sql = """DELETE FROM barcodes.project_sample
                 WHERE project_id = %s AND sample_id = %s
              """
        with TRN:
            pid = convert_to_id(project, 'barcodes.project')
            TRN.add(sql, [pid, self.id])
            TRN.execute()
