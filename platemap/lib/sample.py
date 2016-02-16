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
            if exists(external_name, barcode):
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

    @staticmethod
    def delete(id_):

    # ----------Properties---------------
    @property
    def name(self):

    @property
    def barcode(self):
        """Gets barcode assigned to sample, if there is one

        Returns
        -------
        str or None
            Barcode if assigned, else None
        """
        sql = "Select barcode from barcodes.samples WHERE sample_id = %s"
        with TRN:
            TRN.add(sql, [self.id])
            return TRN.execute_fetchlast()


    @property.setter()
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

    @property
    def sample_type(self):

    @property
    def sample_location(self):

    @property
    def biomass_remaining(self):

    @property
    def created_on(self):

    @property
    def created_by(self):

    @property
    def last_scanned(self):

    @property
    def last_scanned_by(self):

    @property
    def plates(self):
        raise NotImplementedError()

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

def remove_project(self, project):

