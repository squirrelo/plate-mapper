# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from .base import PMObject
from .sql_connection import TRN
from .exceptions import DuplicateError
from .sample import Sample


class Plate(PMObject):
    _table = 'plate'

    @classmethod
    def create(cls, barcode, name, rows, cols):
        r"""Creates a new plate object

        Parameters
        ----------
        barcode : str
            The barcode assigned to the plate
        name : str
            Identifying name for the plate
        rows : int
            Number of rows on the plate
        cols : int
            Number of columns in the plate

        Returns
        -------
        Plate object
            New plate object

        Raises
        ------
        DuplicateError
            Plate with given barcode already exists
        """
        sql = """INSERT INTO barcodes.plate (plate_id, plate, rows, cols)
                 VALUES (%s, %s, %s, %s)
              """
        with TRN:
            if cls.exists(barcode):
                raise DuplicateError(barcode, 'plate')
            TRN.add(sql, [barcode, name, rows, cols])
            TRN.execute()
            return cls(barcode)

    @staticmethod
    def delete(cls, barcode):
        r"""Delete a plate from the system

        Parameters
        ----------
        barcode : str
            The plate barcode
        """
        raise NotImplementedError()

    @staticmethod
    def exists(barcode):
        r"""Checks if a plate already exists

        Parameters
        ----------
        barcode : str
            Barcode for plate

        Returns
        -------
        bool
            Whether plate already exists (True) or not (False)
        """
        sql = "SELECT EXISTS(SELECT * FROM barcodes.plate WHERE plate_id = %s)"
        with TRN:
            TRN.add(sql, [barcode])
            return TRN.execute_fetchlast()

    def __getitem__(self, pos):
        """
        Returns the sample at a given position on the plate

        Parameters
        ----------
        pos : tuple of int
            The plate well to get sample for

        Returns
        -------
        Sample object or None
            Sample at the positon, or None if no sample.

        Notes
        -----
        Passed a tuple, so called as sample = plate[row, col]
        """
        sql = """SELECT sample_id
                 FROM barcodes.plates_samples
                 WHERE plate_id = %s AND plate_row = %s and plate_col = %s
              """
        with TRN:
            row, col = pos[0], pos[1]
            TRN.add(sql, [self.id, row, col])
            sid = TRN.execute_fetchlast()
            return None if sid is None else Sample(sid)

    def __setitem__(self, pos, value):
        """
        Adds the sample at a given position on the plate

        Parameters
        ----------
        pos : tuple of int
            The plate well to add sample at
        value : Sample object or None
            The sample to add, or None to remove sample from position

        Notes
        -----
        Passed a tuple, so called as plate[row, col] = Sample()
        """
        sql = """UPDATE barcodes.plates_samples
                 SET SAMPLE_ID = %s
                 WHERE plate_id = %s AND plate_row = %s and plate_col = %s
              """
        with TRN:
            row, col = pos[0], pos[1]
            TRN.add(sql, [value.id, self.id, row, col])

    @property
    def name(self):
        """Name of the plate

        Returns
        -------
        str
            Name of the plate
        """
        raise NotImplementedError()

    @property
    def finalized(self):
        """Finalized status of the plate

        Returns
        -------
        bool
            If the plate is finalized (True) or not (False)
        """
        raise NotImplementedError()

    @property
    def samples(self):
        """List of samples in the plate, ordered by row down the plate

        Returns
        -------
        list of Sample objects or None
            Samples on the plate, ordered by row.
            Sample at [0, 0], followed by [0, 1], [0, 2], etc.
            If no sample exists for the well, None is added to the list
        """
        raise NotImplementedError()

    # -------- functions ----------------
    def to_html(self):
        raise NotImplementedError()
