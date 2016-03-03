# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import main

from platemap.tests_website.tornado_test_base import TestHandlerBase
from platemap.lib.util import rollback_tests


@rollback_tests()
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
            'utf-8'), 'sample_name\tlinker\tfwd_primer\trev_primer\tbarcode\t'
            'sample_barcode\tbiomass_remaining\textraction_robot\t'
            'extractionkit_lot\tmastermix_lot\tplate_id\tplate_well\t'
            'primer_lot\tprocessing_robot\tsample_type\ttm1000_8_tool\t'
            'tm300_8_tool\ttm50_8_tool\twater_lot\nSample 1.A\tCT\t'
            'AAAAAAAACCCCTTTTTT\tGGGGGGGGAAAAAAAACC\tCCTCGCATGACC\t000000001\t'
            'True\texrb001\texkl001\tmm001\t\t\tpr002\tprrb001\tstool\ttm18001'
            '\ttm38001\ttm58001\twat001\nSample 1.B\tCT\tAAAAAAAACCCCTTTTTT\t'
            'GGGGGGGGAAAAAAAACC\tAATACAGACCTG\t000000001\tTrue\texrb002\t'
            'exkl002\tmm002\t000000003\tB2\tpr001\tprrb002\tstool\ttm18002\t'
            'tm38002\ttm58002\twat002\nSample 2\tCT\tAAAAAAAACCCCTTTTTT\t'
            'GGGGGGGGAAAAAAAACC\tGGACAAGTGCGA\t000000002\tFalse\texrb002\t'
            'exkl002\tmm002\t000000003\tB3\tpr001\tprrb002\tstool\ttm18002\t'
            'tm38002\ttm58002\twat002\nSample 3\tCT\tAAAAAAAACCCCTTTTTT\t'
            'GGGGGGGGAAAAAAAACC\tACGTATTCGAAG\t\tFalse\texrb002\texkl002\t'
            'mm002\t000000003\tC4\tpr001\tprrb002\tskin\ttm18002\ttm38002\t'
            'tm58002\twat002')


@rollback_tests()
class TestRunPageHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/run/view/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<option value="1">Finalized Run</option>',
                      obs.body.decode('utf-8'))

    def test_post_create(self):
        obs = self.post('/run/view/', {'action': 'create',
                                       'name': 'newtestrun'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfuly created run "newtestrun"',
                      obs.body.decode('utf-8'))

    def test_post_create_error(self):
        obs = self.post('/run/view/', {'action': 'create',
                                       'name': 'Finalized Run'})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with name \'Finalized Run\' already exists '
                      'in table \'run\'', obs.body.decode('utf-8'))

    def test_post_finalize(self):
        obs = self.post('/run/view/', {'action': 'finalize',
                                       'run': 2})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfuly finalized run "Non-finalized Run"',
                      obs.body.decode('utf-8'))

    def test_post_finalize_error(self):
        obs = self.post('/run/view/', {'action': 'finalize',
                                       'run': 5})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with ID \'5\' does not exist in table '
                      '\'run\'', obs.body.decode('utf-8'))

    def test_post_unknown_action(self):
        obs = self.post('/run/view/', {'action': 'UNKNOWN THING'})
        self.assertEqual(obs.code, 400)


@rollback_tests()
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


@rollback_tests()
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

    def test_post_finalize_error(self):
        obs = self.post('/pool/view/', {'action': 'finalize',
                                        'pool': 5})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with ID \'5\' does not exist in table '
                      '\'pool\'', obs.body.decode('utf-8'))

    def test_post_unknown_action(self):
        obs = self.post('/pool/view/', {'action': 'UNKNOWN THING'})
        self.assertEqual(obs.code, 400)

if __name__ == '__main__':
    main()
