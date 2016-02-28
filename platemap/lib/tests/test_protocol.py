from unittest import TestCase, main
from datetime import datetime

import platemap as pm


@pm.util.rollback_tests()
class TestProtocolBase(TestCase):
    def setUp(self):
        self.base1 = pm.protocol.ProtocolBase(1)
        self.base2 = pm.protocol.ProtocolBase(2)

    def test_create_protocol_sample(self):
        obs = pm.protocol.ProtocolBase._create_protocol(
            pm.person.Person(3), pm.sample.Sample(3))
        obs = pm.protocol.ProtocolBase(obs)

        self.assertEqual(obs.sample, pm.sample.Sample(3))
        self.assertEqual(obs.plate, None)
        self.assertEqual(obs.created_by, pm.person.Person(3))

    def test_create_protocol_plate(self):
        obs = pm.protocol.ProtocolBase._create_protocol(
            pm.person.Person(3), plate=pm.plate.Plate('000000003'))
        obs = pm.protocol.ProtocolBase(obs)

        self.assertEqual(obs.sample, None)
        self.assertEqual(obs.plate, pm.plate.Plate('000000003'))
        self.assertEqual(obs.created_by, pm.person.Person(3))

    def test_create_protocol_no_sample_plate(self):
        with self.assertRaises(pm.exceptions.DeveloperError):
            pm.protocol.ProtocolBase._create_protocol(pm.person.Person(1))

    def test_create_protocol_both_sample_plate(self):
        with self.assertRaises(pm.exceptions.DeveloperError):
            pm.protocol.ProtocolBase._create_protocol(
                pm.person.Person(1), pm.sample.Sample(1),
                pm.plate.Plate('000000003'))

    def test_get_subproperty(self):
        with self.assertRaises(pm.exceptions.DeveloperError):
            self.base1._get_subproperty('sample')

    def test_sample(self):
            self.assertEqual(self.base1.sample, pm.sample.Sample(1))
            self.assertEqual(self.base2.sample, None)

    def test_plate(self):
        self.assertEqual(self.base1.plate, None)
        self.assertEqual(self.base2.plate, pm.plate.Plate('000000003'))

    def test_created_on(self):
            self.assertEqual(self.base1.created_on, datetime(2016, 2, 28))

    def test_created_by(self):
            self.assertEqual(self.base1.created_by, pm.person.Person(1))

    def test_summary(self):
        with self.assertRaises(pm.exceptions.DeveloperError):
            self.base1.summary()


@pm.util.rollback_tests()
class TestExtractionProtocol(TestCase):
    def setUp(self):
        self.extract_protocol1 = pm.protocol.ExtractionProtocol(1)
        self.extract_protocol2 = pm.protocol.ExtractionProtocol(2)

    def test_instantiate_wrong_subclass(self):
        pm.protocol.ExtractionProtocol(4)

    def test_create(self):
        raise NotImplementedError()

    def test_exists(self):
        raise NotImplementedError()

    def test_extractionkit_lot(self):
        raise NotImplementedError()

    def test_extraction_robot(self):
        raise NotImplementedError()

    def test_tm1000_8_tool(self):
        raise NotImplementedError()

    def test_sample(self):
            obs = self.extract_protocol1.sample
            self.assertEqual(obs, pm.sample.Sample(1))

            obs = self.extract_protocol2.sample
            self.assertEqual(obs, None)

    def test_plate(self):
            obs = self.extract_protocol1.plate
            self.assertEqual(obs, None)

            obs = self.extract_protocol2.plate
            self.assertEqual(obs, pm.plate.Plate('000000003'))

    def test_created_on(self):
            obs = self.extract_protocol1.created_on
            self.assertEqual(obs, datetime(2016, 2, 28))

    def test_created_by(self):
            obs = self.extract_protocol1.created_by
            self.assertEqual(obs, pm.person.Person(1))

    def test_summary(self):
        raise NotImplementedError()


@pm.util.rollback_tests()
class TestPCRProtocol(TestCase):
    def setUp(self):
        self.pcr_protocol3 = pm.protocol.PCRProtocol(3)
        self.pcr_protocol4 = pm.protocol.PCRProtocol(4)

    def test_instantiate_wrong_subclass(self):
        pm.protocol.PCRProtocol(1)

    def test_create(self):
        raise NotImplementedError()

    def test_exists(self):
        raise NotImplementedError()

    def test_extraction_protocol(self):
        raise NotImplementedError()

    def test_primer_lot(self):
        raise NotImplementedError()

    def test_mastermix_lot(self):
        raise NotImplementedError()

    def test_water_lot(self):
        raise NotImplementedError()

    def test_processing_robot(self):
        raise NotImplementedError()

    def test_tm300_8_tool(self):
        raise NotImplementedError()

    def test_tm50_8_tool(self):
        raise NotImplementedError()

    def test_sample(self):
            obs = self.extract_protocol1.sample
            self.assertEqual(obs, pm.sample.Sample(1))

            obs = self.extract_protocol2.sample
            self.assertEqual(obs, None)

    def test_plate(self):
            obs = self.extract_protocol1.plate
            self.assertEqual(obs, None)

            obs = self.extract_protocol2.plate
            self.assertEqual(obs, pm.plate.Plate('000000003'))

    def test_created_on(self):
            obs = self.extract_protocol1.created_on
            self.assertEqual(obs, datetime(2016, 2, 28))

    def test_created_by(self):
            obs = self.extract_protocol1.created_by
            self.assertEqual(obs, pm.person.Person(1))

    def test_summary(self):
        raise NotImplementedError()


if __name__ == "__main__":
    main()
