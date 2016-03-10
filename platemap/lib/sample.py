# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import platemap as pm


class Sample(pm.base.PMObject):
    _table = 'sample'

    @staticmethod
    def types():
        """Returns list of all sample types for samples in DB

        Returns
        -------
        list of str
            All sample types in the DB
        """
        sql = """SELECT DISTINCT sample_type
                 FROM barcodes.sample
                 ORDER BY sample_type"""
        with pm.sql.TRN:
            pm.sql.TRN.add(sql)
            return pm.sql.TRN.execute_fetchflatten()

    @staticmethod
    def locations():
        """Returns list of all sample locations for samples in DB

        Returns
        -------
        list of str
            All sample locations in the DB
        """
        sql = """SELECT DISTINCT sample_location
                 FROM barcodes.sample
                 ORDER BY sample_location"""
        with pm.sql.TRN:
            pm.sql.TRN.add(sql)
            return pm.sql.TRN.execute_fetchflatten()

    @classmethod
    def from_file(cls, file, sample_type, sample_location, sample_set, person,
                  projects=None, sep='\t'):
        """Loads sample name and barcode from file, suplementing with info

        Parameters
        ----------
        fp : Open file or stringIO
            File containing the sample names and, optionally, barcodes
        sample_type : str
            What the samples are (stool, etc)
        sample_location : str
            Where the samples are physically located/stored
        sample_set: str
            What sample set the samples belong to
        person  : Person object
            The person initially logging the samples
        projects : list of str, optional
            What projects the samples are part of. Default None
        sep : str, optional
            Seperator used between the name and barcodes. Default tab

        Returns
        -------
        int
            Number of samples added

        Notes
        -----
        File format is a header line first, with first column sample name and,
        if barcodes exist, the column is named 'barcode'.
        One sample per line.
        """
        # check if we are given barcodes or not and set accordingly
        barcodes = False
        barcode_pos = 1
        header = file.readline().strip().split(sep)
        if len(header) > 1 and 'barcode'in header:
            barcodes = True
            barcode_pos = header.index('barcode')

        # This just wraps create for each sample so we get all the checks
        # from create but can add multiple samples at a time
        count = 0
        for line in file:
            line = line.strip()
            info = line.split(sep) if barcodes else [line, None]
            cls.create(info[0], sample_type, sample_location, sample_set,
                       person, projects=None, barcode=info[barcode_pos])
            count += 1
        return count

    @classmethod
    def search(cls, name=None, biomass_remaining=None, sample_type=None,
               barcode=None, project=None, primer_set=None, protocol=None):
        """Searches over all given parameters for matching samples

        Parameters
        ----------
        name : str
            Sample name to search for
        biomass_remaining : bool, optional
            Whether physical sample remains
        sample_type : str, optional
            What sample type to look for (stool, etc)
        barcode : str, optional
            barcode to get
        project : str, optional
            project to search over
        primer_set : str, optional
            What primers were used for sample amplification
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
        if all([x is None for x in [name, biomass_remaining, sample_type,
                                    barcode, project, primer_set, protocol]]):
            raise pm.exceptions.DeveloperError(
                'Must pass at least one parameter')

        joins = []
        wheres = []
        sql_args = []
        sql = 'SELECT sample_id FROM barcodes.sample'
        if name is not None:
            wheres.append('sample = %s')
            sql_args.append(name)
        if biomass_remaining is not None:
            wheres.append('biomass_remaining = %s')
            sql_args.append(biomass_remaining)
        if sample_type is not None:
            wheres.append('sample_type = %s')
            sql_args.append(sample_type)
        if barcode is not None:
            wheres.append('barcode = %s')
            sql_args.append(barcode)
        if project is not None:
            joins.append('JOIN barcodes.project_samples USING (sample_id)')
            joins.append('JOIN barcodes.project USING (project_id)')
            wheres.append('project = %s')
            sql_args.append(project)
        # TODO: add primer set and protocol searches

        with pm.sql.TRN:
            sql_join = ' '.join(joins)
            sql_where = ' AND '.join(wheres)
            full_sql = '%s %s WHERE %s' % (sql, sql_join, sql_where)
            pm.sql.TRN.add(full_sql, sql_args)
            return [cls(s) for s in
                    pm.sql.TRN.execute_fetchflatten()]

    @classmethod
    def create(cls, name, sample_type, sample_location, sample_set,
               person, projects=None, barcode=None):
        """Creates a new sample in the database

        Parameters
        ----------
        name : str
            Common name of the sample
        sample_type : str
            What the sample is (stool, etc)
        sample_location : str
            Where th esample is physically located/stored
        sample_set: str
            What sample set the sample belongs to
        person  : Person object
            The person initially logging the sample
        projects : list of str, optional
            What projects the sample is part of
        barcode : str, optional
            If barcoded, the barcode added

        Returns
        -------
        Sample object
            The new sample

        Raises
        ------
        ValueError
            If a barcode and sample set are given, and the barcode does not
            match the pre-assigned sample set.
        AssignError
            If a barcode is given without pre-assignment, but is already
            used elsewhere
        """
        test_barcode_sql = """SELECT barcode, sample_set_id
                              FROM barcodes.sample_set_barcodes
                              WHERE barcode = %s
                           """
        rem_barcode_sql = """DELETE FROM barcodes.sample_set_barcodes
                             WHERE barcode = %s AND sample_set_id = %s
                          """
        sample_sql = """INSERT INTO barcodes.sample
                        (sample, barcode, sample_type, sample_location,
                         sample_set_id, created_by, last_scanned_by)
                        VALUES (%s,%s,%s,%s,%s,%s, %s)
                        RETURNING sample_id
                     """
        project_sql = """INSERT INTO barcodes.project_samples
                         (sample_id, project_id)
                         VALUES (%s,%s)"""
        barcode_sql = """UPDATE barcodes.barcode
                         SET assigned_on = NOW()
                         WHERE barcode = %s
                      """
        with pm.sql.TRN:
            if cls.exists(name, sample_set):
                raise pm.exceptions.DuplicateError(name, 'sample')

            sample_set_id = pm.util.convert_to_id(sample_set, 'sample_set')
            if barcode is not None:
                pm.sql.TRN.add(test_barcode_sql, [barcode])
                res = pm.sql.TRN.execute_fetchindex()
                if res:
                    # Make sure barcode matches the pre-assigned sample set
                    barcode, db_sample_set = res[0]
                    if sample_set_id != db_sample_set:
                        raise ValueError('Barcode does not match pre-assigned '
                                         'sample set!')
                    else:
                        # Remove from pre-assigned table since barcode is now
                        # attached to a sample
                        pm.sql.TRN.add(rem_barcode_sql,
                                       [barcode, sample_set_id])
                elif pm.util.check_barcode_assigned(barcode):
                    raise pm.exceptions.AssignError(
                        'Barcode %s already assigned!' % barcode)
                pm.sql.TRN.add(barcode_sql, [barcode])

            pm.sql.TRN.add(sample_sql, [
                name, barcode, sample_type, sample_location, sample_set_id,
                person.id, person.id])
            sample_id = pm.sql.TRN.execute_fetchlast()

            if projects is not None:
                pids = [(sample_id, pm.util.convert_to_id(p, 'project'))
                        for p in projects]
                pm.sql.TRN.add(project_sql, pids, many=True)

        return cls(sample_id)

    @staticmethod
    def exists(name, sample_set):
        sql = """SELECT EXISTS(
              SELECT *
              FROM barcodes.sample
              WHERE sample = %s
                  AND sample_set_id = %s)
              """
        with pm.sql.TRN:
            try:
                sample_set_id = pm.util.convert_to_id(sample_set, 'sample_set')
            except LookupError:
                # sample_set given does not exist
                return False
            pm.sql.TRN.add(sql, [name, sample_set_id])
            return pm.sql.TRN.execute_fetchlast()

    @staticmethod
    def delete(id_):
        raise NotImplementedError()

    # ----------Properties---------------
    @property
    def name(self):
        return self._get_property('sample')

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
        with pm.sql.TRN:
            if pm.util.check_barcode_assigned(barcode):
                raise ValueError("Barcode %s already assigned" % barcode)
            if self.barcode is not None:
                raise pm.exceptions.AssignError(
                    'Barcode already assigned to this sample')
            pm.sql.TRN.add(sample_sql, [barcode, self.id])
            pm.sql.TRN.add(barcode_sql, [barcode])
            pm.sql.TRN.execute()

    @property
    def sample_set(self):
        """Returns sample set this sample belongs to.

           Returns
           -------
           str
               Sample set the sample belongs to.
        """
        sql = """SELECT sample_set
                 FROM barcodes.sample
                 JOIN barcodes.sample_set USING (sample_set_id)
                 WHERE sample_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.sql.TRN.execute_fetchlast()

    @property
    def projects(self):
        """Returns list of projects this sample is associated with

        Returns
        -------
        list of str
            Projects the sample is associated with
        """
        sql = """SELECT project
                 FROM barcodes.sample
                 LEFT JOIN barcodes.project_sample_sets USING (sample_set_id)
                 LEFT JOIN barcodes.project USING (project_id)
                 WHERE sample_id = %s
                 UNION
                 SELECT project
                 FROM barcodes.project_samples
                 LEFT JOIN barcodes.project USING (project_id)
                 WHERE sample_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id, self.id])
            projects = pm.sql.TRN.execute_fetchflatten()
            return None if not projects else projects

    @property
    def sample_type(self):
        return self._get_property('sample_type')

    @property
    def location(self):
        return self._get_property('sample_location')

    @property
    def biomass_remaining(self):
        return self._get_property('biomass_remaining')

    @property
    def created_on(self):
        return self._get_property('created_on')

    @property
    def created_by(self):
        sql = """SELECT person_id
                 FROM barcodes.sample S
                 JOIN barcodes.person P ON (S.created_by = P.person_id)
                 WHERE sample_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.person.Person(pm.sql.TRN.execute_fetchlast())

    @property
    def last_scanned(self):
        return self._get_property('last_scanned')

    @property
    def last_scanned_by(self):
        sql = """SELECT person_id
                 FROM barcodes.sample S
                 JOIN barcodes.person P ON (S.last_scanned_by = P.person_id)
                 WHERE sample_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.person.Person(pm.sql.TRN.execute_fetchlast())

    @property
    def plates(self):
        sql = """SELECT plate_id
                 FROM barcodes.plates_samples
                 WHERE sample_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return [pm.plate.Plate(p) for p in
                    pm.sql.TRN.execute_fetchflatten()]

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
        sql = """INSERT INTO barcodes.project_samples (project_id, sample_id)
                 VALUES (%s, %s)
              """
        with pm.sql.TRN:
            projects = self.projects
            if projects is not None and project in self.projects:
                return
            pid = pm.util.convert_to_id(project, 'project')
            pm.sql.TRN.add(sql, [pid, self.id])
            pm.sql.TRN.execute()

    def remove_project(self, project):
        sql = """DELETE FROM barcodes.project_samples
                 WHERE project_id = %s AND sample_id = %s
              """
        with pm.sql.TRN:
            pid = pm.util.convert_to_id(project, 'project')
            pm.sql.TRN.add(sql, [pid, self.id])
            pm.sql.TRN.execute()
