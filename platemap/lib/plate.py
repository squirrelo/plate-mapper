# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from .base import PMObject


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
        """
        raise NotImplementedError()

    @staticmethod
    def delete(cls, barcode):
        r"""Delete a plate from the system

        Parameters
        ----------
        barcode : str
            The plate barcode
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        list of Sample objects
            Samples on the plate, ordered by row.
            Sample at [0, 0], followed by [0, 1], [0, 2], etc.

        """
        raise NotImplementedError()

    # -------- functions ----------------
    def to_html(self):
        raise NotImplementedError()
