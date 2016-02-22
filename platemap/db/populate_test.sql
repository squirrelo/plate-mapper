INSERT INTO barcodes.barcode (barcode, obsolete, create_timestamp) VALUES
('000000001', 'N', '2016-02-22 8:52:00'), ('000000002', 'N', '2016-02-22 8:53:00'), ('000000003', 'N', '2016-02-22 8:54:00'),
('000000004', 'N', '2016-02-22 8:55:00'), ('000000005', 'N', '2016-02-22 8:56:00'), ('000000006', 'N', '2016-02-22 8:57:00'),
('000000007', 'N', '2016-02-22 8:58:00'), ('000000008', 'N', '2016-02-22 8:59:00'), ('000000009', 'N', '2016-02-22 9:00:00'),
('000000010', 'N', '2016-02-22 9:01:00');

INSERT INTO barcodes.people (name, email, address, affiliation, phone) VALUES
('First test person', 'test@foo.bar', '123 fake street', 'UCSD', '111-111-1111'),
('Second test person', 'someone@foo.bar', NULL, NULL, NULL),
('Third test person', 'anotherone@foo.bar', NULL, 'UCLA', NULL);

INSERT INTO barcodes.samples (external_name, barcode, sample_type, sample_location, created_on, created_by, last_scanned, last_scanned_by) VALUES
('Sample 1', '000000001', 'stool', 'the freezer', '2016-02-22 8:52:00', 1, '2016-02-22 8:52:00', 1),
('Sample 2', '000000002', 'stool', 'the freezer', '2016-02-22 8:53:00', 1, '2016-02-22 8:53:00', 1),
('Sample 3', NULL, 'skin', 'the freezer', '2016-02-22 8:54:00', 1, '2016-02-22 8:54:00', 1),
('Sample 4', NULL, 'oral', 'the freezer', '2016-02-22 8:55:00', 1, '2016-02-22 8:55:00', 1);

INSERT INTO barcodes.project (project, description, pi, contact_person, created_on) VALUES
('Project 1', 'First test project', 1, 2, '2016-02-22 8:52:00'),
('Project 2', 'Second test project', 1, 2, '2016-02-22 8:53:00'),
('Project 3', 'Third test project', 3, 2, '2016-02-22 8:54:00');

INSERT INTO barcodes.sample_set (sample_set, created_on, created_by) VALUES
('Sample Set 1', '2016-02-22 8:52:00', 1), ('Sample Set 2', '2016-02-22 8:53:00', 1);

INSERT INTO barcodes.project_sample_set (sample_set_id, project_id) VALUES (1, 1), (2, 1), (2, 2);

INSERT INTO barcodes.project_barcode (project_id, barcode) VALUES (3, '000000010'), (3, '000000009');

INSERT INTO barcodes.sample_set_sample (sample_id, sample_set_id) VALUES (1, 1), (2, 1), (3, 1), (4, 2);



