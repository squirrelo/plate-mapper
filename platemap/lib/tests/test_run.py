from unittest import TestCase, main
import platemap as pm


@pm.util.rollback_tests()
class TestRun(TestCase):
    def setUp(self):
        self.run1 = pm.run.Run(1)
        self.run2 = pm.run.Run(2)

    def test_runs(self):
        obs = pm.run.Run.runs()
        exp = [pm.run.Run(1), pm.run.Run(2)]
        self.assertEqual(obs, exp)

    def test_runs_finalized(self):
        obs = pm.run.Run.runs(finalized=True)
        exp = [pm.run.Run(1)]
        self.assertEqual(obs, exp)

    def test_create(self):
        self.assertFalse(pm.run.Run.exists('NewTestRun'))
        pm.run.Run.create('NewTestRun', pm.person.Person(2))
        self.assertTrue(pm.run.Run.exists('NewTestRun'))

    def test_create_exists(self):
        with self.assertRaises(pm.exceptions.DuplicateError):
            pm.run.Run.create('Finalized Run', pm.person.Person(2))

    def test_exists(self):
        self.assertFalse(pm.run.Run.exists('NewTestRun'))
        self.assertTrue(pm.run.Run.exists('Non-finalized Run'))

    def test_delete(self):
        pass

    def test_name(self):
        self.assertEqual(self.run1.name, 'Finalized Run')

    def test_pools(self):
        obs = self.run1.pools
        exp = [pm.run.Pool(1)]
        self.assertEqual(obs, exp)

    def test_finalized(self):
        self.assertTrue(self.run1.finalized)
        self.assertFalse(self.run2.finalized)

    def test_finalize(self):
        self.assertFalse(self.run2.finalized)
        self.run2.finalize(pm.person.Person(1))
        self.assertTrue(self.run2.finalized)

    def test_generate_prep_metadata(self):
        self.maxDiff = None
        obs = self.run1.generate_prep_metadata()
        self.assertEqual(obs, self.meta)

    def test_generate_prep_metadata_not_finalized(self):
        with self.assertRaises(pm.exceptions.DeveloperError):
            self.run2.generate_prep_metadata()

    meta = ("sample_name\tlinker\tfwd_primer\trev_primer\tbarcode\t"
            "sample_barcode\tbiomass_remaining\textraction_robot\t"
            "extractionkit_lot\tmastermix_lot\tplate_id\tplate_well\t"
            "primer_lot\t""processing_robot\tsample_type\ttm1000_8_tool\t"
            "tm300_8_tool\ttm50_8_tool\twater_lot\nSample 1.A\tCT\t"
            "AAAAAAAACCCCTTTTTT\tGGGGGGGGAAAAAAAACC\tCCTCGCATGACC\t000000001\t"
            "True\texrb001\texkl001\tmm001\t\t\tpr002\tprrb001\tstool\ttm18001"
            "\ttm38001\ttm58001\twat001\nSample 1.B\tCT\tAAAAAAAACCCCTTTTTT\t"
            "GGGGGGGGAAAAAAAACC\tAATACAGACCTG\t000000001\tTrue\texrb002\t"
            "exkl002\tmm002\t000000003\tB2\tpr001\tprrb002\tstool\ttm18002\t"
            "tm38002\ttm58002\twat002\nSample 2\tCT\tAAAAAAAACCCCTTTTTT\t"
            "GGGGGGGGAAAAAAAACC\tGGACAAGTGCGA\t000000002\tFalse\texrb002\t"
            "exkl002\tmm002\t000000003\tB3\tpr001\tprrb002\tstool\ttm18002\t"
            "tm38002\ttm58002\twat002\nSample 3\tCT\tAAAAAAAACCCCTTTTTT\t"
            "GGGGGGGGAAAAAAAACC\tACGTATTCGAAG\t\tFalse\texrb002\texkl002\t"
            "mm002\t000000003\tC4\tpr001\tprrb002\tskin\ttm18002\ttm38002\t"
            "tm58002\twat002")


@pm.util.rollback_tests()
class TestPool(TestCase):
    def setUp(self):
        self.pool1 = pm.run.Pool(1)
        self.pool2 = pm.run.Pool(2)

    def test_pools(self):
        obs = pm.run.Pool.pools()
        exp = [pm.run.Pool(1), pm.run.Pool(2)]
        self.assertEqual(obs, exp)

    def test_pools_finalized(self):
        obs = pm.run.Pool.pools(finalized=True)
        exp = [pm.run.Pool(1)]
        self.assertEqual(obs, exp)

    def test_create(self):
        self.assertFalse(pm.run.Pool.exists('NewTestPool', pm.run.Run(2)))
        pm.run.Pool.create('NewTestPool', pm.run.Run(2), pm.person.Person(2))
        self.assertTrue(pm.run.Pool.exists('NewTestPool', pm.run.Run(2)))

    def test_create_exists(self):
        with self.assertRaises(pm.exceptions.DuplicateError):
            pm.run.Pool.create('Finalized Pool', pm.run.Run(1),
                               pm.person.Person(2))

    def test_create_finalized_run(self):
        with self.assertRaises(pm.exceptions.EditError):
            pm.run.Pool.create('NewTestPool', pm.run.Run(1),
                               pm.person.Person(2))

    def test_exists(self):
        self.assertTrue(pm.run.Pool.exists('Finalized Pool', pm.run.Run(1)))
        self.assertFalse(pm.run.Pool.exists('Finalized Pool', pm.run.Run(2)))
        self.assertFalse(pm.run.Pool.exists('NOEXIST', pm.run.Run(1)))

    def test_delete(self):
        pass

    def test_name(self):
        self.assertEqual(self.pool1.name, 'Finalized Pool')

    def test_run(self):
        self.assertEqual(self.pool1.run, pm.run.Run(1))

    def test_finalized(self):
        self.assertTrue(self.pool1.finalized)
        self.assertFalse(self.pool2.finalized)

    def test_finalize(self):
        self.assertFalse(self.pool2.finalized)
        self.pool2.finalize(pm.person.Person(1))
        self.assertTrue(self.pool2.finalized)

    def test_add_protocol(self):
        self.assertEqual(self.pool2.protocols, [pm.protocol.PCRProtocol(3)])
        self.pool2.add_protocol(pm.protocol.PCRProtocol(4))
        self.assertEqual(self.pool2.protocols, [pm.protocol.PCRProtocol(3),
                                                pm.protocol.PCRProtocol(4)])

    def test_add_protocol_finalized(self):
        self.assertTrue(self.pool1.finalized)
        with self.assertRaises(pm.exceptions.EditError):
            self.pool1.add_protocol(pm.protocol.PCRProtocol(4))

    def test_remove_protocol(self):
        self.assertEqual(self.pool2.protocols, [pm.protocol.PCRProtocol(3)])
        self.pool2.remove_protocol(pm.protocol.PCRProtocol(3))
        self.assertEqual(self.pool2.protocols, [])

    def test_remove_protocol_finalized(self):
        self.assertTrue(self.pool1.finalized)
        with self.assertRaises(pm.exceptions.EditError):
            self.pool1.remove_protocol(pm.protocol.PCRProtocol(4))


if __name__ == "__main__":
    main()
