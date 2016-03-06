--Always initialize to production environment
INSERT INTO barcodes.settings (test) VALUES ('F');

--Add access control hierarchy
INSERT INTO barcodes.access_controls (access_level, access_value) VALUES
('Basic access', 1), ('Override', 2), ('Admin', 4);
