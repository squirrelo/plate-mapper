# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import platemap as pm


def get_extraction_plates():
    """Return the information for plates attached to extractions

    Returns
    -------
    list of tuple of str
        The plate info, in the form
        [(plate_barcode, plate_name, extraction_id, extracton_date), ...]
    """
    sql = """SELECT plate_id, plate, protocol_settings_id, ps.created_on
             FROM barcodes.extraction_settings
             LEFT JOIN barcodes.protocol_settings ps
                USING (protocol_settings_id)
             LEFT JOIN barcodes.plate USING (plate_id)
             WHERE plate_id IS NOT NULL
             ORDER BY created_on DESC
          """
    with pm.sql.TRN:
        pm.sql.TRN.add(sql)
        return pm.sql.TRN.execute_fetchindex()
