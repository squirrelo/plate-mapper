INSERT INTO barcodes.access_controls (access_level, access_value) VALUES
('Basic access', 1), ('Override', 2), ('Admin', 4);

INSERT INTO barcodes.instrument (platform, sequencing_method, instrument_model) VALUES
('Illumina', 'sequencing by synthesis', 'Illumina HiSeq 2500'),
('Illumina', 'sequencing by synthesis', 'Illumina MiSeq'),
('LS454', 'pyrosequencing', '454 GS FLX+'),
('LS454', 'pyrosequencing', '454 GS FLX Titanium');

--Always initialize to production environment
INSERT INTO barcodes.settings (test) VALUES ('F');
