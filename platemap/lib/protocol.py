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

        Notes
        -----
        Must supply either sample or plate, not both. Also must supply at least
        one of them.

        This is meant to be called as a helper to child classes
        """
        if sample is None and plate is None:
            raise ValueError('Must supply a sample or plate!')
        if sample is not None and plate is not None:
            raise ValueError('Must supply either sample or plate, not both!')
        raise NotImplementedError()

    def _get_property(self, column):
        sql = """Select {0}
                 FROM barcodes.{1}
                 WHERE protocol_settings_id = %s""".format(
            column, self._subtable)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.sql.TRN.execute_fetchlast()

    @property
    def sample(self):
        raise NotImplementedError()

    @property
    def plate(self):
        raise NotImplementedError()

    @property
    def created_on(self):
        raise NotImplementedError()

    @property
    def created_by(self):
        raise NotImplementedError()


class ExtractionProtocol(ProtocolBase):
    _subtable = 'extraction_settings'

    @classmethod
    def create(cls, person, sample, plate, extractionkit_lot, extraction_robot,
               tm1000_8_tool):
        r"""Creates new settings for an extraction protocol run

        """
        protocol_id = cls._create_protocol(person, sample, plate)
        raise NotImplementedError()
        return cls(protocol_id)

    @staticmethod
    def exists():
        r"""Checks if a given run already exists in the system

        """
        raise NotImplementedError()

    @property
    def extractionkit_lot(self):
        raise NotImplementedError()

    @property
    def extraction_robot(self):
        raise NotImplementedError()

    @property
    def tm1000_8_tool(self):
        raise NotImplementedError()

    def summary(self):
        """Returns dict of settings for object

        Returns
        -------
        dict of objects
            Values for each property, as {property: value, ...}
        """
        raise NotImplementedError()


class PCRProtocol(ProtocolBase):
    _subtable = 'pcr_settings'

    @classmethod
    def create(cls, person, sample, plate, extraction_protocol, primer_lot,
               mastermix_lot, water_lot, processing_robot, tm300_8_tool,
               tm50_8_tool):
        r"""Creates new settings for a PCR protocol run

        """
        protocol_id = cls._create_protocol(person, sample, plate)
        raise NotImplementedError()
        return cls(protocol_id)

    @staticmethod
    def exists():
        r"""Checks if a given run already exists in the system

        """
        raise NotImplementedError()

    @property
    def extraction_protocol(self):
        raise NotImplementedError()

    @property
    def primer_lot(self):
        raise NotImplementedError()

    @property
    def mastermix_lot(self):
        raise NotImplementedError()

    @property
    def water_lot(self):
        raise NotImplementedError()

    @property
    def processing_robot(self):
        raise NotImplementedError()

    @property
    def tm300_8_tool(self):
        raise NotImplementedError()

    @property
    def tm50_8_tool(self):
        raise NotImplementedError()

    def summary(self):
        """Returns dict of settings for object

        Returns
        -------
        dict of objects
            Values for each property, as {property: value, ...}
        """
        raise NotImplementedError()
