# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import platemap as pm


class ProtocolBase(pm.base.PMObject):
    _table = 'protocol_settings'
    _subtable = None

    @staticmethod
    def _create_protocol(person, sample=None, plate=None):
        """Creates a new protocol.

        Parameters
        ----------
        person : Person object
            Person who ran the protocol
        sample : Sample object, optional
            The sample the protocol was run on
        plate: Plate object, optional
            The plate the protocol was run on

        Returns
        -------
        int
            The id of the protocol settings

        Raises
        ------
        DeveloperError
            Neither sample nor plate provided
            Both sample and plate provided

        Notes
        -----
        Must supply either sample or plate, not both. Also must supply at least
        one of them.

        This is meant to be called as a helper to child classes
        """
        sql = """INSERT INTO barcodes.protocol_settings
                 (sample_id, plate_id, created_by)
                 VALUES (%s, %s, %s)
                 RETURNING protocol_settings_id
              """
        with pm.sql.TRN:
            if sample is None and plate is None:
                raise pm.exceptions.DeveloperError(
                    'Must supply a sample or plate!')
            if sample is not None and plate is not None:
                raise pm.exceptions.DeveloperError(
                    'Must supply sample or plate, not both!')

            sid = sample.id if sample is not None else None
            pid = plate.id if plate is not None else None
            pm.sql.TRN.add(sql, [sid, pid, person.id])
            return pm.sql.TRN.execute_fetchlast()

    def _get_subproperty(self, column):
        if self._subtable is None:
            raise pm.exceptions.DeveloperError('No subtable given!')

        sql = """Select {0}
                 FROM barcodes.{1}
                 WHERE protocol_settings_id = %s""".format(
            column, self._subtable)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.sql.TRN.execute_fetchlast()

    @property
    def sample(self):
        sid = self._get_property('sample_id')
        return pm.sample.Sample(sid) if sid is not None else None

    @property
    def plate(self):
        pid = self._get_property('plate_id')
        return pm.plate.Plate(pid) if pid is not None else None

    @property
    def created_on(self):
        return self._get_property('created_on')

    @property
    def created_by(self):
        return pm.person.Person(self._get_property('created_by'))

    def summary(self):
        """Returns dict of settings for object

        Returns
        -------
        dict of objects
            Values for each property, as {property: value, ...}

        Raises
        ------
        DeveloperError
            Called using base class and not subclass
        """
        if self._subtable is None:
            raise pm.exceptions.DeveloperError('Must be called on subclass!')

        sql = """SELECT *
                 FROM barcodes.protocol_settings
                 JOIN barcodes.{0} USING (protocol_settings_id)
                 WHERE protocol_settings_id = %s
              """.format(self._subtable)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            info = dict(pm.sql.TRN.execute_fetchindex()[0])

            # Clean person, plate, and sample ids to their objects
            info['created_by'] = pm.person.Person(info['created_by'])
            if info['sample_id'] is not None:
                info['plate'] = None
                del info['plate_id']
                info['sample'] = pm.sample.Sample(info['sample_id'])
                del info['sample_id']
            else:
                info['plate'] = pm.plate.Plate(info['plate_id'])
                del info['plate_id']
                info['sample'] = None
                del info['sample_id']
            return info


class ExtractionProtocol(ProtocolBase):
    _subtable = 'extraction_settings'

    def _check_id(self, id_):
        r"""Check that the provided ID actually exists on the subtable

        Parameters
        ----------
        id_ : object
            The ID to test
        """
        sql = """SELECT EXISTS(
                   SELECT * FROM barcodes.{0}
                   WHERE protocol_settings_id=%s)""".format(self._subtable)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [id_])
            return pm.sql.TRN.execute_fetchlast()

    @classmethod
    def create(cls, person, extractionkit_lot, extraction_robot,
               tm1000_8_tool, sample=None, plate=None):
        r"""Creates new settings for an extraction protocol run

        Parameters
        ----------
        person : Person object
            Person doing the run and logging in system
        sample : Sample object
            Sample the protocol is being run on
        plate : Plate object
            Plate the protocol is being run on
        extractionkit_lot : str
            Lot used for extraction
        extraction_robot : str
            Specific robot identifier used for extraction
        tm1000_8_tool : str
            Specific tool identifier used for extraction

        Returns
        -------
        ExtractionProtocol object
            New ExtractionProtocol
        """
        sql = """INSERT INTO barcodes.extraction_settings
                 (protocol_settings_id, extractionkit_lot, extraction_robot,
                  tm1000_8_tool)
                 VALUES (%s, %s, %s, %s)
              """
        with pm.sql.TRN:
            protocol_id = cls._create_protocol(person, sample, plate)
            pm.sql.TRN.add(sql, [protocol_id, extractionkit_lot,
                                 extraction_robot, tm1000_8_tool])
            return cls(protocol_id)

    @property
    def extractionkit_lot(self):
        return self._get_subproperty('extractionkit_lot')

    @property
    def extraction_robot(self):
        return self._get_subproperty('extraction_robot')

    @property
    def tm1000_8_tool(self):
        return self._get_subproperty('tm1000_8_tool')


class PCRProtocol(ProtocolBase):
    _subtable = 'pcr_settings'

    def _check_id(self, id_):
        r"""Check that the provided ID actually exists on the subtable

        Parameters
        ----------
        id_ : object
            The ID to test
        """
        sql = """SELECT EXISTS(
                   SELECT * FROM barcodes.{0}
                   WHERE protocol_settings_id=%s)""".format(self._subtable)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [id_])
            return pm.sql.TRN.execute_fetchlast()

    @classmethod
    def create(cls, person, extraction_protocol, primer_lot,
               mastermix_lot, water_lot, processing_robot, tm300_8_tool,
               tm50_8_tool, sample=None, plate=None):
        r"""Creates new settings for a PCR protocol run

        """
        sql = """INSERT INTO barcodes.pcr_settings
                 (protocol_settings_id, extraction_protocol_settings_id,
                  primer_lot, mastermix_lot, water_lot, processing_robot,
                  tm300_8_tool, tm50_8_tool)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
              """
        with pm.sql.TRN:
            protocol_id = cls._create_protocol(person, sample, plate)
            pm.sql.TRN.add(sql, [
                protocol_id, extraction_protocol.id, primer_lot, mastermix_lot,
                water_lot, processing_robot, tm300_8_tool, tm50_8_tool])
            return cls(protocol_id)

    @property
    def extraction_protocol(self):
        return ExtractionProtocol(
            self._get_subproperty('extraction_protocol_settings_id'))

    @property
    def primer_lot(self):
        return self._get_subproperty('primer_lot')

    @property
    def mastermix_lot(self):
        return self._get_subproperty('mastermix_lot')

    @property
    def water_lot(self):
        return self._get_subproperty('water_lot')

    @property
    def processing_robot(self):
        return self._get_subproperty('processing_robot')

    @property
    def tm300_8_tool(self):
        return self._get_subproperty('tm300_8_tool')

    @property
    def tm50_8_tool(self):
        return self._get_subproperty('tm50_8_tool')

    def summary(self):
        """See parent class for docstring"""
        summary = super(PCRProtocol, self).summary()
        summary['extraction_protocol'] = ExtractionProtocol(
            summary['extraction_protocol_settings_id'])
        del summary['extraction_protocol_settings_id']
        return summary

    def metadata_summary(self):
        """Returns dict of full settings for PCR and Extraction

        Returns
        -------
        dict of dict of objects
            Values for each sample, as {sample: {property: value, ...}, ...}
        """
        sql1 = """SELECT *
                 FROM (SELECT protocol_settings_id, plate_id
                       FROM barcodes.protocol_settings
                       WHERE sample_id IS NULL) AS prot
                 JOIN barcodes.plates_samples USING (plate_id)
                 JOIN barcodes.sample USING (sample_id)
                 JOIN barcodes.pcr_settings ps USING (
                  protocol_settings_id)
                 JOIN barcodes.extraction_settings es ON (
                  ps.extraction_protocol_settings_id = es.protocol_settings_id)
                 WHERE ps.protocol_settings_id = %s
              """
        sql2 = """SELECT *
                 FROM (SELECT protocol_settings_id, sample_id
                       FROM barcodes.protocol_settings
                       WHERE sample_id IS NOT NULL) AS prot
                 LEFT JOIN barcodes.sample USING (sample_id)
                 LEFT JOIN barcodes.pcr_settings ps USING (
                  protocol_settings_id)
                 LEFT JOIN barcodes.extraction_settings es ON (
                  ps.extraction_protocol_settings_id = es.protocol_settings_id)
                 WHERE ps.protocol_settings_id = %s
              """
        with pm.sql.TRN:
            # Get the plate based and sample based protocol run info
            pm.sql.TRN.add(sql1, [self.id])
            rows = pm.sql.TRN.execute_fetchindex()
            pm.sql.TRN.add(sql2, [self.id])
            rows.extend(pm.sql.TRN.execute_fetchindex())
            info = {}
            for row in rows:
                row = dict(row)
                sample = row['sample']
                info[sample] = {}
                del row['sample']

                # Replace empty barcode with string
                if row['barcode'] is None:
                    row['barcode'] = ''

                # Convert plate info if needed
                if 'plate_id' in row:
                    # 65 for ASCII capital A
                    row['plate_well'] = '%s%d' % (chr(65 + row['plate_row']),
                                                  row['plate_col'] + 1)
                    del row['plate_row']
                    del row['plate_col']
                else:
                    row['plate_id'] = ''
                    row['plate_well'] = ''

                # Remove non-metadata housekeeping information
                for key in ['protocol_settings_id', 'created_on', 'created_by',
                            'sample_id', 'extraction_protocol_settings_id',
                            'sample_location', 'last_scanned',
                            'last_scanned_by', 'sample_set_id']:
                    del row[key]
                info[sample] = row
            return info
