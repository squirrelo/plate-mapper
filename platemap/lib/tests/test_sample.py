from unittest import TestCase, main
from platemap.lib.util import rollback_transaction
from platemap.lib.sample import Sample
from platemap.lib.exceptions import DeveloperError


class TestSample(TestCase):
    @rollback_transaction
    def test_search(self):
        obs = Sample.search(biomass_remaining=True)
        exp = [Sample(1), Sample(2), Sample(3), Sample(4)]
        self.assertEqual(obs, exp)

        obs = Sample.search(sample_type='stool')
        exp = [Sample(1), Sample(2)]
        self.assertEqual(obs, exp)

        obs = Sample.search(barcode='000000002')
        exp = [Sample(2)]
        self.assertEqual(obs, exp)

        obs = Sample.search(barcode='000000010')
        exp = []
        self.assertEqual(obs, exp)

        # TODO: finish these tests as objects are made
        # Sample.search(project=)
        # Sample.search(primer_set=)
        # Sample.search(protocol=)

    @rollback_transaction
    def test_search_no_parameters(self):
        with self.assertRaises(DeveloperError):
            Sample.search()

    @rollback_transaction
    def test_create(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_exists(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_exists_no_exists(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_delete(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_delete_no_exists(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_name(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_barcode(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_barcode_none(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_add_barcode(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_add_barcode_already_used_barcode(self):
        raise NotImplementedError()

    @rollback_transaction
    def test_add_barcode_already_assigned_to_sample(self):
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
        pass

    @rollback_transaction
    def test_protocols(self):
        pass

    @rollback_transaction
    def test_pools(self):
        pass

    @rollback_transaction
    def test_runs(self):
        pass


if __name__ == "__main__":
    main()
