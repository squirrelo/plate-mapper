from unittest import TestCase, main
from platemap.lib.util import rollback_transaction
from platemap.lib.sample import Sample


class TestSample(TestCase):
    @rollback_transaction
    def test_search(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_create(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_exists(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_delete(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_name(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_barcode(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_add_barcode(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_projects(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_sample_type(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_sample_location(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_biomass_remaining(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_created_on(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_created_by(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_last_scanned(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_last_scanned_by(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_plates(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_protocols(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_pools(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_runs(self):
        raise NotImplementedError()


if __name__ == "__main__":
    main()
