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


def check_create_primer_lot(primer_set_id, lot, person):
    """Checks if a primer lot exists and, if not, creates it

    Parameters
    ----------
    primer_set_id: int
        Primer set to create new lot for
    lot : str
        Lot identifier
    person : Person object
        Person doing the check/create
    """
    check_sql = """SELECT EXISTS(
                   SELECT *
                   FROM barcodes.primer_set_lots
                   WHERE primer_lot = %s AND primer_set_id = %s)
                """
    add_sql = """INSERT INTO barcodes.primer_set_lots
                 (primer_set_id, primer_lot, person_id)
                 VALUES (%s, %s, %s)
              """
    with pm.sql.TRN:
        pm.sql.TRN.add(check_sql, [lot, primer_set_id])
        if pm.sql.TRN.execute_fetchlast():
            # Lot already exists so don't need to do anything else
            return
        pm.sql.TRN.add(add_sql, [primer_set_id, lot, person.id])


def get_primer_sets():
    """Returns all primer sets in the database

    Returns
    -------
    list of list of [int, str]
        list of list of the primer set id and name
    """
    sql = "SELECT primer_set_id, primer_set FROM barcodes.primer_set"
    with pm.sql.TRN:
        pm.sql.TRN.add(sql)
        return pm.sql.TRN.execute_fetchindex()


def get_lots_for_primer_set(primer_set_id):
    """Returns all primer sets in the database

    Parameter
    ---------
    primer_set_id : int
        ID of the primer set to look for lots from

    Returns
    -------
    list of str
        list of primer lots
    """
    sql = """SELECT primer_lot
             FROM barcodes.primer_set_lots
             WHERE primer_set_id = %s
          """
    with pm.sql.TRN:
        pm.sql.TRN.add(sql, [primer_set_id])
        return pm.sql.TRN.execute_fetchflatten()


def get_instruments():
    """Returns list of instrument models in the database

    Returns
    -------
    list of str
        Instruments in the database
    """
    sql = """SELECT instrument_model
             FROM barcodes.instrument
             ORDER BY instrument_model"""
    with pm.sql.TRN:
        pm.sql.TRN.add(sql)
        return pm.sql.TRN.execute_fetchflatten()


def get_finalized_pcr_protocols():
    """Returns a list of finalized PCR protocols

    Returns
    -------
    list of list of (int, str)
        List of list of protocol id and formatted protocol info
    """
    sql = """SELECT protocol_settings_id,
             plate || ' - ' || plate_id || ' - ' || created_on
             FROM barcodes.pcr_settings
             JOIN barcodes.protocol_settings USING (protocol_settings_id)
             LEFT JOIN (SELECT plate_id, plate FROM barcodes.plate) AS P
                 USING (plate_id)
             WHERE plate_id IS NOT NULL
          """
    with pm.sql.TRN:
        pm.sql.TRN.add(sql)
        return pm.sql.TRN.execute_fetchindex()
