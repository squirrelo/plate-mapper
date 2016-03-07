UPDATE barcodes.settings SET test = 'T';

INSERT INTO barcodes.barcode (barcode, obsolete, create_timestamp, assigned_on) VALUES
('000000001', 'N', '2016-02-22 8:52:00', '2016-02-22 8:52:00'), ('000000002', 'N', '2016-02-22 8:53:00','2016-02-22 8:53:00'), ('000000003', 'N', '2016-02-22 8:54:00', '2016-02-22 8:53:00'),
('000000004', 'N', '2016-02-22 8:55:00', NULL), ('000000005', 'N', '2016-02-22 8:56:00', NULL), ('000000006', 'N', '2016-02-22 8:57:00', NULL),
('000000007', 'N', '2016-02-22 8:58:00', NULL), ('000000008', 'N', '2016-02-22 8:59:00', NULL), ('000000009', 'N', '2016-02-22 9:00:00', NULL),
('000000010', 'N', '2016-02-22 9:01:00', NULL);

INSERT INTO barcodes.person (name, email, address, affiliation, phone) VALUES
('First test person', 'test@foo.bar', '123 fake street', 'UCSD', '111-111-1111'),
('Second test person', 'someone@foo.bar', NULL, NULL, NULL),
('Third test person', 'anotherone@foo.bar', NULL, 'UCLA', NULL);

--hashed password is 'password'
INSERT INTO barcodes.user (user_id, pass, person_id, access, created_on) VALUES
('User1', '$2a$12$yG/DzvN0eFk5cambflZkEuMBBDz9PsoMnpKVqZbUaOdFwS2PgedrS', 1, 7, '2016-02-24 8:52:00'),
('User2', '$2a$12$yG/DzvN0eFk5cambflZkEuMBBDz9PsoMnpKVqZbUaOdFwS2PgedrS', 1, 1, '2016-02-24 8:52:00');

INSERT INTO barcodes.project (project, description, pi, contact_person, created_on) VALUES
('Project 1', 'First test project', 'PI1', 'contact1', '2016-02-22 8:52:00'),
('Project 2', 'Second test project', 'PI2', 'contact2', '2016-02-22 8:53:00'),
('Project 3', 'Third test project', 'PI3', 'contact3', '2016-02-22 8:54:00');

INSERT INTO barcodes.sample_set (sample_set, created_on, created_by) VALUES
('Sample Set 1', '2016-02-22 8:52:00', 1),
('Sample Set 2', '2016-02-22 8:53:00', 1),
('Sample Set 3', '2016-02-22 8:54:00', 1);

INSERT INTO barcodes.sample (sample, barcode, sample_type, sample_location, created_on, created_by, last_scanned, last_scanned_by, sample_set_id, biomass_remaining) VALUES
('Sample 1', '000000001', 'stool', 'the freezer', '2016-02-22 8:52:00', 1, '2016-02-22 8:52:00', 1, 1, 'T'),
('Sample 2', '000000002', 'stool', 'the freezer', '2016-02-22 8:53:00', 1, '2016-02-22 8:53:00', 1, 1, 'F'),
('Sample 3', NULL, 'skin', 'the other freezer', '2016-02-22 8:54:00', 1, '2016-02-22 8:54:00', 1, 1, 'F'),
('Sample 4', NULL, 'oral', 'the freezer', '2016-02-22 8:55:00', 1, '2016-02-22 8:55:00', 1, 2, 'T');

INSERT INTO barcodes.project_sample_sets (project_id, sample_set_id) VALUES (1, 1), (2, 2), (3, 3);

INSERT INTO barcodes.project_samples (sample_id, project_id) VALUES (1, 1), (2, 1), (3, 1), (4, 2), (2, 2);

INSERT INTO barcodes.project_barcodes (project_id, barcode) VALUES (1, '000000001'), (1, '000000002'), (3, '000000004');

INSERT INTO barcodes.plate (plate_id, plate, created_on, finalized, person_id, rows, cols) VALUES
('000000003', 'Test plate 1', '2016-02-22 8:55:00', 'F', 1, 8, 12);

INSERT INTO barcodes.plates_samples (plate_id, sample_id, plate_row, plate_col) VALUES
('000000003', 1, 1, 1), ('000000003', 2, 1, 2), ('000000003', 3, 2, 3);

INSERT INTO barcodes.primer_set (primer_set, company, linker, fwd_primer, rev_primer, barcodes, target_gene, target_subfragment) VALUES
('Primer Set 1', 'IDT', 'CT', 'AAAAAAAACCCCTTTTTT', 'GGGGGGGGAAAAAAAACC', '{"A1": "CCTCGCATGACC","A10": "GCGCGGCGTTGC","A11": "GTCGCTTGCACA","A12": "TCCGCCTAGTCG","A2": "GGCGTAACGGCA","A3": "GCGAGGAAGTCC","A4": "CAAATTCGGGAT","A5": "TTGTGTCTCCCT","A6": "CAATGTAGACAC","A7": "AACCACTAACCG","A8": "AACTTTCAGGAG","A9": "CCAGGACAGGAA","B1": "CGCGCAAGTATT","B10": "AGACTTCTCAGG","B11": "TCTTGCGGAGTC","B12": "CTATCTCCTGTC","B2": "AATACAGACCTG","B3": "GGACAAGTGCGA","B4": "TACGGTCTGGAT","B5": "TTCAGTTCGTTA","B6": "CCGCGTCTCAAC","B7": "CCGAGGTATAAT","B8": "AGATTCGCTCGA","B9": "TTGCCGCTCTGG","C1": "AAGGCGCTCCTT","C10": "AGTTCTCATTAA","C11": "GAGCCATCTGTA","C12": "GATATACCAGTG","C2": "GATCTAATCGAG","C3": "CTGATGTACACG","C4": "ACGTATTCGAAG","C5": "GACGTTAAGAAT","C6": "TGGTGGAGTTTC","C7": "TTAACAAGGCAA","C8": "AACCGCATAAGT","C9": "CCACAACGATCA","D1": "CGCAATGAGGGA","D10": "GTGTCGAGGGCA","D11": "TTCCACACGTGG","D12": "AGAATCCACCAC","D2": "CCGCAGCCGCAG","D3": "TGGAGCCTTGTC","D4": "TTACTTATCCGA","D5": "ATGGGACCTTCA","D6": "TCCGATAATCGG","D7": "AAGTCACACACA","D8": "GAAGTAGCGAGC","D9": "CACCATCTCCGG","E1": "ACGGCGTTATGT","E10": "AGTGTTTCGGAC","E11": "ATTTCCGCTAAT","E12": "CAAACCTATGGC","E2": "GAACCGTGCAGG","E3": "ACGTGCCTTAGA","E4": "AGTTGTAGTCCG","E5": "AGGGACTTCAAT","E6": "CGGCCAGAAGCA","E7": "TGGCAGCGAGCC","E8": "GTGAATGTTCGA","E9": "TATGTTGACGGC","F1": "CATTTGACGACG","F10": "AGTGCAGGAGCC","F11": "GTACTCGAACCA","F12": "ATAGGAATAACC","F2": "ACTAAGTACCCG","F3": "CACCCTTGCGAC","F4": "GATGCCTAATGA","F5": "GTACGTCACTGA","F6": "TCGCTACAGATG","F7": "CCGGCTTATGTG","F8": "ATAGTCCTTTAA","F9": "TCGAGCCGATCT","G1": "GCTGCGTATACC","G10": "GTTGCTGAGTCC","G11": "ACACCGCACAAT","G12": "CACAACCACAAC","G2": "CTCAGCGGGACG","G3": "ATGCCTCGTAAG","G4": "TTAGTTTGTCAC","G6": "ATTATGATTATG","G7": "CGAATACTGACA","G8": "TCTTATAACGCT","G9": "TAAGGTCGATAA","H1": "GAGAAGCTTATA","H10": "CGGAGAGACATG","H11": "CAGCCCTACCCA","H12": "TCGTTGGGACTA","H2": "GTTAACTTACTA","H3": "GTTGTTCTGGGA","H4": "AGGGTGACTTTA","H5": "GCCGCCAGGGTC","H6": "GCCACCGCCGGA","H7": "ACACACCCTGAC","H8": "TATAGGCTCCGC","H9": "ATAATTGCCGAG"}', '16S', 'V4'),
('Primer Set 2', 'IDT', 'CT', 'AAAAAAAACCCCTTTTTT', 'GGGGGGGGAAAAAAAACC', '{"barcode":"CCTCGCATGACC"}', '16S', 'V4');

INSERT INTO barcodes.primer_set_lots (primer_set_id, primer_lot, created_on, person_id) VALUES
(1, 'pr001', '02/28/2016', 1),
(2, 'pr002', '02/28/2016', 1);

INSERT INTO barcodes.protocol_settings (protocol_id, sample_id, plate_id, created_on, created_by) VALUES
(1, 1, NULL, '02/28/2016', 1),
(1, NULL,'000000003', '02/28/2016', 2),
(1, 1, NULL, '02/28/2016', 1),
(1, NULL, '000000003', '02/28/2016', 2);

INSERT INTO barcodes.extraction_settings (protocol_settings_id, extractionkit_lot, extraction_robot, tm1000_8_tool) VALUES
(1, 'exkl001', 'exrb001', 'tm18001'),
(2, 'exkl002', 'exrb002', 'tm18002');

INSERT INTO barcodes.pcr_settings (protocol_settings_id, extraction_protocol_settings_id, primer_lot, mastermix_lot, water_lot, processing_robot, tm300_8_tool, tm50_8_tool) VALUES
(3, 1, 'pr002', 'mm001', 'wat001', 'prrb001', 'tm38001', 'tm58001'),
(4, 2, 'pr001', 'mm002', 'wat002', 'prrb002', 'tm38002', 'tm58002');

INSERT INTO barcodes.run (run, created_on, created_by, finalized, finalized_on, finalized_by, instrument_id) VALUES
('Finalized Run', '2016-03-02 1:25:00', 1, 'T', '2016-03-02 1:26:00', 1, 1),
('Non-finalized Run', '2016-03-02 1:27:00', 1, 'F', NULL, NULL, 2);

INSERT INTO barcodes.pool (run_id, pool, created_on, created_by, finalized, finalized_on, finalized_by) VALUES
(1, 'Finalized Pool', '2016-03-02 1:20:00', 2, 'T', '2016-03-02 1:21:00', 2),
(2, 'Non-finalized Pool', '2016-03-02 1:22:00', 2, 'F', NULL, NULL);

INSERT INTO barcodes.pool_samples (pool_id, protocol_settings_id) VALUES (1, 3), (1, 4), (2, 4);
