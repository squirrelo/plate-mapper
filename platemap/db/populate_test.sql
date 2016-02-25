UPDATE barcodes.settings SET test = 'T';

INSERT INTO barcodes.barcode (barcode, obsolete, create_timestamp, assigned_on) VALUES
('000000001', 'N', '2016-02-22 8:52:00', '2016-02-22 8:52:00'), ('000000002', 'N', '2016-02-22 8:53:00','2016-02-22 8:53:00'), ('000000003', 'N', '2016-02-22 8:54:00', '2016-02-22 8:53:00'),
('000000004', 'N', '2016-02-22 8:55:00', '2016-02-22 8:55:00'), ('000000005', 'N', '2016-02-22 8:56:00', NULL), ('000000006', 'N', '2016-02-22 8:57:00', NULL),
('000000007', 'N', '2016-02-22 8:58:00', NULL), ('000000008', 'N', '2016-02-22 8:59:00', NULL), ('000000009', 'N', '2016-02-22 9:00:00', NULL),
('000000010', 'N', '2016-02-22 9:01:00', NULL);

INSERT INTO barcodes.person (name, email, address, affiliation, phone) VALUES
('First test person', 'test@foo.bar', '123 fake street', 'UCSD', '111-111-1111'),
('Second test person', 'someone@foo.bar', NULL, NULL, NULL),
('Third test person', 'anotherone@foo.bar', NULL, 'UCLA', NULL);

--hashed password is 'password'
INSERT INTO barcodes.user (user_id, pass, person_id, access, created_on) VALUES
('User1', '$2a$12$yG/DzvN0eFk5cambflZkEuMBBDz9PsoMnpKVqZbUaOdFwS2PgedrS', 1, 7, '2016-02-24 8:52:00');

INSERT INTO barcodes.project (project, description, pi, contact_person, created_on) VALUES
('Project 1', 'First test project', 1, 2, '2016-02-22 8:52:00'),
('Project 2', 'Second test project', 1, 2, '2016-02-22 8:53:00'),
('Project 3', 'Third test project', 3, 2, '2016-02-22 8:54:00');

INSERT INTO barcodes.sample_set (sample_set, created_on, created_by) VALUES ('Sample Set 1', '2016-02-22 8:52:00', 1), ('Sample Set 2', '2016-02-22 8:53:00', 1);

INSERT INTO barcodes.sample (sample, barcode, sample_type, sample_location, created_on, created_by, last_scanned, last_scanned_by, sample_set_id, biomass_remaining) VALUES
('Sample 1', '000000001', 'stool', 'the freezer', '2016-02-22 8:52:00', 1, '2016-02-22 8:52:00', 1, 1, 'T'),
('Sample 2', '000000002', 'stool', 'the freezer', '2016-02-22 8:53:00', 1, '2016-02-22 8:53:00', 1, 1, 'F'),
('Sample 3', NULL, 'skin', 'the other freezer', '2016-02-22 8:54:00', 1, '2016-02-22 8:54:00', 1, 1, 'F'),
('Sample 4', NULL, 'oral', 'the freezer', '2016-02-22 8:55:00', 1, '2016-02-22 8:55:00', 1, 2, 'T');

INSERT INTO barcodes.plate (plate_id, plate, created_on, finalized, person_id, rows, cols) VALUES
('000000003', 'Test plate 1', '2016-02-22 8:55:00', 'F', 1, 8, 12);

INSERT INTO barcodes.plates_samples (plate_id, sample_id, plate_row, plate_col) VALUES
('000000003', 1, 1, 1), ('000000003', 2, 1, 2), ('000000003', 3, 2, 3);

INSERT INTO barcodes.project_samples (sample_id, project_id) VALUES (1, 1), (2, 1), (2, 2);

INSERT INTO barcodes.project_barcodes (project_id, barcode) VALUES (1, '000000001'), (1, '000000002'), (3, '000000004');
