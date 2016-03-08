# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import main

from platemap.tests_website.tornado_test_base import TestHandlerBase
import platemap as pm


@pm.lib.util.rollback_tests()
class TestGeneratePrepTemplate(TestHandlerBase):
    def test_get(self):
        obs = self.get('/run/gen_prep/1')
        self.assertEqual(obs.code, 200)
        self.assertEqual(obs.headers['Content-type'],
                         'text/html; charset=UTF-8,application/octet-stream')
        self.assertEqual(obs.headers['Content-Transfer-Encoding'], 'binary')
        self.assertEqual(obs.headers['Accept-Ranges'], 'bytes')
        self.assertEqual(obs.headers['Content-Encoding'], 'none')
        self.assertEqual(obs.headers['Content-Disposition'],
                         'attachment; filename=prep_metadata.txt')
        self.assertEqual(obs.body.decode(
            'utf-8'), self.meta)

    meta = (
        'sample_name\tlinker\tprimer\tpcr_primers\ttarget_gene\t'
        'target_subfragment\tbarcode\tsample_barcode\tbiomass_remaining\t'
        'center_name\texperiment_design_description\textraction_robot\t'
        'extractionkit_lot\tinstrument_model\tmastermix_lot\tplate_id\t'
        'plate_well\tplatform\tprimer_lot\tprocessing_robot\trun_center\t'
        'run_date\trun_prefix\tsequencing_method\ttm1000_8_tool\ttm300_8_tool'
        '\ttm50_8_tool\twater_lot\nSample 1.A\tCT\tAAAAAAAACCCCTTTTTT\t'
        'FWD:AAAAAAAACCCCTTTTTT;REV:GGGGGGGGAAAAAAAACC\t16S\tV4\tCCTCGCATGACC'
        '\t000000001\tTrue\tUCSDMI\tINSERT HERE\texrb001\texkl001\t'
        'Illumina HiSeq 2500\tmm001\t\t\tIllumina\tpr002\tprrb001\tUCSDMI\t'
        '2016-03-02 01:26:00\tFinalized_Run\tsequencing by synthesis\ttm18001'
        '\ttm38001\ttm58001\twat001\nSample 1.B\tCT\tAAAAAAAACCCCTTTTTT\t'
        'FWD:AAAAAAAACCCCTTTTTT;REV:GGGGGGGGAAAAAAAACC\t16S\tV4\tAATACAGACCTG'
        '\t000000001\tTrue\tUCSDMI\tINSERT HERE\texrb002\texkl002\t'
        'Illumina HiSeq 2500\tmm002\t000000003\tB2\tIllumina\tpr001\tprrb002\t'
        'UCSDMI\t2016-03-02 01:26:00\tFinalized_Run\tsequencing by synthesis\t'
        'tm18002\ttm38002\ttm58002\twat002\nSample 2\tCT\tAAAAAAAACCCCTTTTTT\t'
        'FWD:AAAAAAAACCCCTTTTTT;REV:GGGGGGGGAAAAAAAACC\t16S\tV4\tGGACAAGTGCGA'
        '\t000000002\tFalse\tUCSDMI\tINSERT HERE\texrb002\texkl002\t'
        'Illumina HiSeq 2500\tmm002\t000000003\tB3\tIllumina\tpr001\tprrb002\t'
        'UCSDMI\t2016-03-02 01:26:00\tFinalized_Run\tsequencing by synthesis\t'
        'tm18002\ttm38002\ttm58002\twat002\nSample 3\tCT\tAAAAAAAACCCCTTTTTT\t'
        'FWD:AAAAAAAACCCCTTTTTT;REV:GGGGGGGGAAAAAAAACC\t16S\tV4\tACGTATTCGAAG'
        '\t\tFalse\tUCSDMI\tINSERT HERE\texrb002\texkl002\tIllumina HiSeq 2500'
        '\tmm002\t000000003\tC4\tIllumina\tpr001\tprrb002\tUCSDMI\t'
        '2016-03-02 01:26:00\tFinalized_Run\tsequencing by synthesis\ttm18002'
        '\ttm38002\ttm58002\twat002')


@pm.lib.util.rollback_tests()
class TestRunPageHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/run/view/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<option value="1">Finalized Run</option>',
                      obs.body.decode('utf-8'))

    def test_post_create(self):
        obs = self.post('/run/view/', {'action': 'create',
                                       'name': 'newtestrun',
                                       'instrument': 'Illumina MiSeq'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfuly created run "newtestrun"',
                      obs.body.decode('utf-8'))

    def test_post_create_error(self):
        obs = self.post('/run/view/', {'action': 'create',
                                       'name': 'Finalized Run',
                                       'instrument': 'Illumina MiSeq'})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with name \'Finalized Run\' already exists '
                      'in table \'run\'', obs.body.decode('utf-8'))

    def test_post_finalize(self):
        obs = self.post('/run/view/', {'action': 'finalize',
                                       'run': 2})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfuly finalized run "Non-finalized Run"',
                      obs.body.decode('utf-8'))
        self.assertTrue(pm.run.Run(2).finalized)

    def test_post_finalize_error(self):
        obs = self.post('/run/view/', {'action': 'finalize',
                                       'run': 5})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with ID \'5\' does not exist in table '
                      '\'run\'', obs.body.decode('utf-8'))

    def test_post_unknown_action(self):
        obs = self.post('/run/view/', {'action': 'UNKNOWN THING'})
        self.assertEqual(obs.code, 400)


@pm.lib.util.rollback_tests()
class TestRenderRunHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/run/render/1')
        self.assertEqual(obs.code, 200)
        self.assertIn('<input type="submit" value="Download Prep Metadata">',
                      obs.body.decode('utf-8'))
        self.assertNotIn('<input type="submit" value="Finalize Run">',
                         obs.body.decode('utf-8'))

    def test_get_not_finalized(self):
        obs = self.get('/run/render/2')
        self.assertEqual(obs.code, 200)
        self.assertNotIn('<input type="submit" value="Download Prep '
                         'Metadata">', obs.body.decode('utf-8'))
        self.assertIn('<input type="submit" value="Finalize Run">',
                      obs.body.decode('utf-8'))


@pm.lib.util.rollback_tests()
class TestPoolPageHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/pool/view/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<option value="1">Finalized Pool</option>',
                      obs.body.decode('utf-8'))

    def test_get_pool_id(self):
        obs = self.get('/pool/view/?pool_id=1')
        self.assertEqual(obs.code, 200)
        self.assertIn('<option value="1">Finalized Pool</option>',
                      obs.body.decode('utf-8'))

    def test_post_create(self):
        obs = self.post('/pool/view/', {'action': 'create',
                                        'name': 'newtestpool',
                                        'run': 2})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfuly created pool "newtestpool"',
                      obs.body.decode('utf-8'))

    def test_post_create_error(self):
        obs = self.post('/pool/view/', {'action': 'create',
                                        'name': 'Finalized Pool',
                                        'run': 1})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with name \'name\' already exists in table '
                      '\'pool\'', obs.body.decode('utf-8'))

    def test_post_finalize(self):
        obs = self.post('/pool/view/', {'action': 'finalize',
                                        'pool': 2})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfuly finalized pool "Non-finalized Pool"',
                      obs.body.decode('utf-8'))
        self.assertTrue(pm.run.Pool(2).finalized)

    def test_post_finalize_error(self):
        obs = self.post('/pool/view/', {'action': 'finalize',
                                        'pool': 5})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with ID \'5\' does not exist in table '
                      '\'pool\'', obs.body.decode('utf-8'))

    def test_post_add(self):
        obs = self.post('/pool/view/', {'action': 'add',
                                        'pool': 2,
                                        'protocol': 4})
        self.assertEqual(obs.code, 200)
        self.assertIn('Test plate 1', obs.body.decode('utf-8'))

    def test_post_add_error(self):
        obs = self.post('/pool/view/', {'action': 'add',
                                        'pool': 2,
                                        'protocol': 200})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with ID \'200\' does not exist in table '
                      '\'protocol_settings\'', obs.body.decode('utf-8'))

    def test_post_unknown_action(self):
        obs = self.post('/pool/view/', {'action': 'UNKNOWN THING'})
        self.assertEqual(obs.code, 400)


@pm.lib.util.rollback_tests()
class TestPoolHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/pool/render/2')
        self.assertEqual(obs.code, 200)
        self.assertIn('<td>Test plate 1<br/>000000003<br/><br/>Primer Set 1'
                      '<br/>pr001<br/>2016-02-28 00:00:00</td>',
                      obs.body.decode('utf-8'))
        self.assertIn('<input type="submit" value="Finalize Pool">',
                      obs.body.decode('utf-8'))

if __name__ == '__main__':
    main()
