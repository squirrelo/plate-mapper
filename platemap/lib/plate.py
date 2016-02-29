# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import platemap as pm


class Plate(pm.base.PMObject):
    _table = 'plate'

    @classmethod
    def plates(cls, finalized=False):
        """Returns all plates available in the system

        Parameters
        ----------
        finalized: bool, optional
            Whether to only grab finalized plates. Default False.

        Returns
        -------
        list of Plate objects
            All plates in the system
        """
        sql = "SELECT plate_id FROM barcodes.plate"
        if finalized:
            sql += " WHERE finalized = TRUE"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql)
            return [cls(p) for p in pm.sql.TRN.execute_fetchflatten()]

    @classmethod
    def create(cls, barcode, name, person, rows, cols):
        r"""Creates a new plate object

        Parameters
        ----------
        barcode : str
            The barcode assigned to the plate
        name : str
            Identifying name for the plate
        person : Person object
            The person creating the plate
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
        DeveloperError
            Barcode already assigned to something else
        """
        plate_sql = """INSERT INTO barcodes.plate
                       (plate_id, plate, rows, cols, person_id)
                       VALUES (%s, %s, %s, %s, %s)
                    """
        barcode_sql = """UPDATE barcodes.barcode
                         SET assigned_on = NOW()
                         WHERE barcode = %s
                      """
        with pm.sql.TRN:
            if cls.exists(barcode):
                raise pm.exceptions.DuplicateError(barcode, 'plate')
            if pm.util.check_barcode_assigned(barcode):
                raise pm.exceptions.DeveloperError(
                    'Barcode %s already assigned!' % barcode)

            pm.sql.TRN.add(plate_sql, [barcode, name, rows, cols, person.id])
            pm.sql.TRN.add(barcode_sql, [barcode])
            pm.sql.TRN.execute()
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
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [barcode])
            return pm.sql.TRN.execute_fetchlast()

    def _check_finalized(self):
        """Locks down changes to plate if already finalized

        Raises
        ------
        EditError
            Trying to change values of a finalized plate
        """
        if self.finalized:
            raise pm.exceptions.EditError(self.id)

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

        Raises
        ------
        IndexError
            Position given is outside of plate

        Notes
        -----
        Passed a tuple, so called as sample = plate[row, col]
        """
        sql = """SELECT sample_id
                 FROM barcodes.plates_samples
                 WHERE plate_id = %s AND plate_row = %s and plate_col = %s
              """
        with pm.sql.TRN:
            row, col = pos[0], pos[1]
            rows, cols = self.shape
            if row < 0 or row >= rows or col < 0 or col >= cols:
                raise IndexError('Position %d, %d not on plate' % (row, col))

            pm.sql.TRN.add(sql, [self.id, row, col])
            sid = pm.sql.TRN.execute_fetchlast()
            return None if sid is None else pm.sample.Sample(sid)

    def __setitem__(self, pos, value):
        """
        Adds the sample at a given position on the plate

        Parameters
        ----------
        pos : tuple of int
            The plate well to add sample at
        value : Sample object or None
            The sample to add, or None to remove sample from position

        Raises
        ------
        IndexError
            Position given is outside of plate

        Notes
        -----
        Passed a tuple, so called as plate[row, col] = Sample()
        """
        # Need to get around postgres not having upsert in postgres < 9.5
        # So do this slightly hacky workaround
        # http://www.the-art-of-web.com/sql/upsert/
        upsert_sql = """WITH upsert AS (
                            UPDATE barcodes.plates_samples
                            SET sample_id = %s
                            WHERE plate_id = %s AND plate_row = %s
                                AND plate_col = %s
                            RETURNING *)
                        INSERT INTO barcodes.plates_samples
                        (sample_id, plate_id, plate_row, plate_col)
                        SELECT %s, %s, %s, %s WHERE NOT EXISTS (
                            SELECT * FROM upsert)
              """
        delete_sql = """DELETE FROM barcodes.plates_samples
                        WHERE plate_id = %s AND plate_row = %s
                            AND plate_col = %s"""

        with pm.sql.TRN:
            self._check_finalized()
            row, col = pos[0], pos[1]
            rows, cols = self.shape
            if row < 0 or row >= rows or col < 0 or col >= cols:
                raise IndexError('Position %d, %d not on plate' % (row, col))

            if value is not None:
                pm.sql.TRN.add(upsert_sql, [value.id, self.id, row, col,
                                            value.id, self.id, row, col])
            else:
                pm.sql.TRN.add(delete_sql, [self.id, row, col])

    def _get_property(self, column):
        sql = "Select {} from barcodes.plate WHERE plate_id = %s".format(
            column)
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return pm.sql.TRN.execute_fetchlast()

    @property
    def name(self):
        """Name of the plate

        Returns
        -------
        str
            Name of the plate
        """
        return self._get_property('plate')

    @property
    def finalized(self):
        """Finalized status of the plate

        Returns
        -------
        bool
            If the plate is finalized (True) or not (False)
        """
        return self._get_property('finalized')

    @property
    def shape(self):
        """Shaple of the plate

        Returns
        -------
        tuple of int
            Plate dimensions in the form (rows, cols)
        """
        sql = "SELECT rows, cols FROM barcodes.plate WHERE plate_id = %s"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return tuple(pm.sql.TRN.execute_fetchindex()[0])

    @property
    def samples(self):
        """List of samples in the plate, ordered by row down the plate

        Returns
        -------
        list of Sample objects
            Samples on the plate, ordered by row.
            Sample at [0, 0], followed by [0, 1], [0, 2], etc.
        """
        sql = """SELECT sample_id
                 FROM barcodes.plates_samples
                 WHERE plate_id = %s
                 ORDER BY plate_row, plate_col
              """
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
            return [pm.sample.Sample(s) for s in
                    pm.sql.TRN.execute_fetchflatten()]

    @property
    def platemap(self):
        """Samples on the plate, mapped as list of lists

        Returns
        -------
        list of list of Sample objects or None
            Samples on the plate, with None if no sample at the position
        """
        sql = """SELECT plate_row::varchar || plate_col::varchar, sample_id
                 FROM barcodes.plates_samples
                 WHERE plate_id = %s
                 ORDER BY plate_row, plate_col
              """
        with pm.sql.TRN:
            rows, cols = self.shape
            pm.sql.TRN.add(sql, [self.id])
            # Turn the returned rows into a dict keyed to the combined
            # rowcol created by the sql query
            samples = dict(pm.sql.TRN.execute_fetchindex())
            ret = []
            # Loop over each sample and add None of no sample in position
            for r in range(rows):
                ret.append([])
                for c in range(cols):
                    samp = samples.get('%d%d' % (r, c), None)
                    ret[r].append(pm.sample.Sample(samp)
                                  if samp is not None else None)
            return ret

    # -------- functions ----------------
    def to_html(self):
        """Builds an HTML table representation of the plate

        Returns
        -------
        str
            HTML representation of the plate

        Notes
        -----
        The class `plate` is added to the table for css styling.
        """

        samples = self.platemap
        rows, cols = self.shape
        table = ['<table class="plate"><tr><th></th>']
        # Add column header
        for col in range(1, cols + 1):
            table.append('<th>%d</th>' % col)
        table.append('</tr>')
        for row in range(rows):
            table.append('<tr><th>%s</th>' % chr(65 + row))
            for col in range(cols):
                samp = samples[row][col]
                table.append('<td>%s</td>' %
                             samp.name if samp is not None else '<td></td>')
            table.append('</tr>')
        table.append('</table>')
        return ''.join(table)

    def finalize(self):
        """Finalizes plate by flagging it in the DB"""
        sql = "UPDATE barcodes.plate SET finalized = 'T' WHERE plate_id = %s"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql, [self.id])
