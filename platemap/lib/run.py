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
    def runs(cls, finalized=False):
        """Gets all runs in the database

        Parameters
        ----------
        finalized : bool, optional
            Whether to only get finalized runs or not. Default False (get all)

        Returns
        -------
        list of Run objects
            Run objects in the database
        """
        sql = "SELECT run_id FROM barcodes.run"
        if finalized:
            sql += " WHERE finalized = 'T'"
        sql += " ORDER BY run"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql)
            return [cls(r) for r in pm.sql.TRN.execute_fetchflatten()]

    @classmethod
    def create(cls, name, person, instrument):
        """Creates a new run on the system

        Parameters
        ----------
        name : str
            The name for the run
        person : Person object
            The person creating the run
        instrument : str
            Instrument model used to perform the run

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
        sql = """INSERT INTO barcodes.run (run, created_by, instrument_id)
                 VALUES (%s, %s, %s)
                 RETURNING run_id"""
        with pm.sql.TRN:
            instrument_id = pm.util.convert_to_id(instrument, 'instrument',
                                                  'instrument_model')
            pm.sql.TRN.add(sql, [name, person.id, instrument_id])
            return cls(pm.sql.TRN.execute_fetchlast())

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
        sql = "SELECT EXISTS(SELECT * FROM barcodes.run WHERE run = %s)"
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
        return self._get_property('run')

    @property
    def finalized_on(self):
        return self._get_property('finalized_on')

    @property
    def instrument(self):
        sql = """SELECT I.*
                 FROM barcodes.instrument I
                 JOIN barcodes.run USING (instrument_id)
                 WHERE run_id = %s"""
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return dict(pm.sql.TRN.execute_fetchindex()[0])

    @property
    def pools(self):
        sql = "SELECT pool_id FROM barcodes.run_pools WHERE run_id = %s"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return [Pool(p) for p in pm.sql.TRN.execute_fetchflatten()]

    @property
    def finalized(self):
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

    def add_pool(self, pool):
        """Adds a pool to the run

        Parameters
        ----------
        pool : Pool object
            The pool to add to the run
        """
        if pool in self.pools:
            return

        sql = """INSERT INTO barcodes.run_pools (run_id, pool_id)
                 VALUES (%s, %s)"""
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id, pool.id])

    def remove_pool(self, pool):
        """Removes a pool from the run

        Parameters
        ----------
        pool : Pool object
            The pool to remove from the run
        """
        sql = """DELETE FROM barcodes.run_pools
                 WHERE run_id = %s AND pool_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id, pool.id])

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

        primer_lot_sql = """SELECT
                           linker, fwd_primer, rev_primer, barcodes,
                           target_gene, target_subfragment
                           FROM barcodes.primer_set_lots
                           JOIN barcodes.primer_set USING (primer_set_id)
                           WHERE primer_lot = %s
                         """
        protocols_sql = """SELECT protocol_settings_id
                           FROM barcodes.pcr_settings
                           RIGHT JOIN barcodes.pool_samples
                               USING (protocol_settings_id)
                           LEFT JOIN barcodes.pool USING (pool_id)
                           RIGHT JOIN barcodes.run_pools USING (pool_id)
                           WHERE run_id = %s
                        """
        invariant = {'run_center': 'UCSDMI',
                     'center_name': 'UCSDMI',
                     'experiment_design_description': 'INSERT HERE',
                     'run_prefix': self.name.replace(' ', '_'),
                     'run_date': self.finalized_on}
        invariant.update(self.instrument)
        del invariant['instrument_id']

        metadata = {}
        duplicates = {}
        primer_lots_info = {}
        primer_lots_barcodes = {}
        with pm.sql.TRN:
            pm.sql.TRN.add(protocols_sql, [self.id])
            for pid in pm.sql.TRN.execute_fetchflatten():
                protocol = pm.protocol.PCRProtocol(pid)
                protocol_meta = protocol.metadata_summary()
                meta_keys = set(protocol_meta.keys())

                # take care of duplicate sample names that already exist
                sample_overlap = meta_keys.intersection(duplicates.keys())
                if len(sample_overlap) > 0:
                    for sample in sample_overlap:
                        # Add letter to end and delete existing sample name
                        new = '.'.join(sample, chr(sample_overlap[sample]))
                        protocol_meta[new] = protocol_meta[sample]
                        del protocol_meta[sample]
                        sample_overlap[sample] += 1

                # take care of newly overlapping samples
                sample_overlap = meta_keys.intersection(metadata.keys())
                if len(sample_overlap) > 0:
                    for sample in sample_overlap:
                        # Log as new overlap, then add letter to end and delete
                        # existing sample names.
                        metadata[sample + '.A'] = metadata[sample]
                        del metadata[sample]
                        protocol_meta[sample + '.B'] = protocol_meta[sample]
                        del protocol_meta[sample]
                        # 67 for ASCII capital C conversion using chr above
                        duplicates[sample] = 67
                # Add invariant info to all samples and add to metadta dict
                for key in protocol_meta.keys():
                    protocol_meta[key].update(invariant)
                    del protocol_meta[key]['sample_type']
                metadata.update(protocol_meta)

            # At this point we have the varying metadata dict built
            # so build the full dict with primer, instrument, and barcode info
            ret = []
            headers = sorted(next(iter(metadata.values())).keys())
            for sample in sorted(metadata.keys()):
                meta = metadata[sample]
                # Get primer info if not already grabbed
                primer_lot = meta['primer_lot']
                if primer_lot not in primer_lots_info:
                    pm.sql.TRN.add(primer_lot_sql, [primer_lot])
                    info = dict(pm.sql.TRN.execute_fetchindex()[0])
                    primer_lots_barcodes[primer_lot] = info['barcodes']
                    del info['barcodes']
                    primer_lots_info[primer_lot] = info

                # build static ordered info
                fwd = primer_lots_info[primer_lot]['fwd_primer']
                rev = primer_lots_info[primer_lot]['rev_primer']
                row = [sample, primer_lots_info[primer_lot]['linker'],
                       fwd, 'FWD:%s;REV:%s' % (fwd, rev),
                       primer_lots_info[primer_lot]['target_gene'],
                       primer_lots_info[primer_lot]['target_subfragment']]
                if meta['plate_well']:
                    row.append(
                        primer_lots_barcodes[primer_lot][meta['plate_well']])
                else:
                    row.append(primer_lots_barcodes[primer_lot]['barcode'])

                # Build rest of info, ordered correctly
                for h in headers:
                    row.append(meta[h])
                ret.append('\t'.join(map(str, row)))

            # add static header names and create file using joins
            headers[headers.index('barcode')] = 'sample_barcode'
            headers = '\t'.join(['sample_name', 'linker', 'primer',
                                 'pcr_primers', 'target_gene',
                                 'target_subfragment', 'barcode'] + headers)
            return '\n'.join([headers] + ret)


class Pool(pm.base.PMObject):
    _table = 'pool'

    @classmethod
    def pools(cls, finalized=False):
        """Gets all pools in the database

        Parameters
        ----------
        finalized : bool, optional
            Whether to only get finalized pools or not. Default False (get all)

        Returns
        -------
        list of Pool objects
            Pool objects in the database
        """
        sql = "SELECT pool_id FROM barcodes.pool"
        if finalized:
            sql += " WHERE finalized = 'T'"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql)
            return [cls(p) for p in pm.sql.TRN.execute_fetchflatten()]

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
        EditError
            The run is already finalized
        """
        if cls.exists(name, run):
            raise pm.exceptions.DuplicateError('name', 'pool')
        if run.finalized:
            raise pm.exceptions.EditError(run.name)

        pool_sql = """INSERT INTO barcodes.pool (pool, created_by)
                      VALUES (%s, %s) RETURNING pool_id
                   """
        run_sql = """INSERT INTO barcodes.run_pools (run_id, pool_id)
                     VALUES (%s, %s)
                  """

        with pm.sql.TRN:
            pm.sql.TRN.add(pool_sql, [name, person.id])
            pool_id = pm.sql.TRN.execute_fetchlast()
            pm.sql.TRN.add(run_sql, [run.id, pool_id])

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
        sql = """SELECT EXISTS(
                     SELECT *
                     FROM barcodes.pool
                     JOIN barcodes.run_pools USING (pool_id)
                     WHERE pool = %s AND run_id = %s)"""
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [name, run.id])
            return pm.sql.TRN.execute_fetchlast()

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
    def runs(self):
        sql = "SELECT run_id FROM barcodes.run_pools WHERE pool_id = %s"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return [Run(r) for r in pm.sql.TRN.execute_fetchflatten()]

    @property
    def protocols(self):
        sql = """SELECT protocol_settings_id
                 FROM barcodes.pool_samples
                 WHERE pool_id = %s"""
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return [pm.protocol.PCRProtocol(p) for p in
                    pm.sql.TRN.execute_fetchflatten()]

    @property
    def finalized(self):
        return self._get_property('finalized')

    @property
    def finalized_on(self):
        return self._get_property('finalized_on')

    def finalize(self, person):
        """Finalize the run so no more pools can be added

        Parameters
        ----------
        person : Person object
            Person finalizing the pool
        """
        sql = """UPDATE barcodes.pool
                 SET finalized = TRUE, finalized_by = %s
                 WHERE pool_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [person.id, self.id])

    def add_protocol(self, pcr_protocol):
        """Adds a PCR protocol run to the pool

        Parameters
        ----------
        pcr_protocol : PCRProtocol object
            The protocol to add to the run

        Raises
        ------
        EditError
            Pool object is finalized so can't edit
        """
        if self.finalized:
            raise pm.exceptions.EditError('Pool %s already finalized!' %
                                          self.name)
        if pcr_protocol in self.protocols:
            return

        sql = """INSERT INTO barcodes.pool_samples
                 (pool_id, protocol_settings_id)
                 VALUES (%s, %s)
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id, pcr_protocol.id])

    def remove_protocol(self, pcr_protocol):
        """Adds a PCR protocol run to the pool

        Parameters
        ----------
        pcr_protocol : PCRProtocol object
            The pcr_protocol to remove from the run

        Raises
        ------
        EditError
            Pool object is finalized so can't edit
        """
        if self.finalized:
            raise pm.exceptions.EditError('Pool %s already finalized!' %
                                          self.name)

        sql = """DELETE FROM barcodes.pool_samples
                 WHERE pool_id =%s AND protocol_settings_id = %s
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id, pcr_protocol.id])
