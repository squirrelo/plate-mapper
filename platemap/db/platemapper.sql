CREATE SCHEMA barcodes;

CREATE TABLE barcodes.access_controls ( 
	access_level         varchar(10)  NOT NULL,
	access_value         integer  NOT NULL,
	CONSTRAINT pk_access_controls PRIMARY KEY ( access_level )
 );

COMMENT ON TABLE barcodes.access_controls IS 'Track access levels for bitwise comparisons';

CREATE TABLE barcodes.barcode ( 
	barcode              varchar(9)  NOT NULL,
	obsolete             varchar(1)  ,
	assigned_on          timestamp  ,
	create_timestamp     timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT barcode_pkey PRIMARY KEY ( barcode )
 );

COMMENT ON COLUMN barcodes.barcode.assigned_on IS 'date barcode assigned to a project';

COMMENT ON COLUMN barcodes.barcode.create_timestamp IS 'Date barcode created on the system';

CREATE TABLE barcodes.barcode_exceptions ( 
	barcode              varchar(100)  NOT NULL,
	CONSTRAINT pk_barcode_exceptions PRIMARY KEY ( barcode ),
	CONSTRAINT fk_barcode_exceptions FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )    
 );

CREATE TABLE barcodes.people ( 
	person_id            bigserial  NOT NULL,
	name                 varchar(100)  NOT NULL,
	email                varchar  NOT NULL,
	address              varchar(100)  ,
	affiliation          varchar  ,
	phone                varchar(20)  ,
	CONSTRAINT pk_people PRIMARY KEY ( person_id )
 );

CREATE TABLE barcodes.plates ( 
	plate_barcode        varchar  NOT NULL,
	plate_name           varchar(100)  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	person_id            bigint  NOT NULL,
	CONSTRAINT idx_plates UNIQUE ( plate_barcode ) ,
	CONSTRAINT pk_plates PRIMARY KEY ( plate_barcode ),
	CONSTRAINT fk_plates FOREIGN KEY ( plate_barcode ) REFERENCES barcodes.barcode( barcode )    ,
	CONSTRAINT fk_plates_0 FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    
 );

CREATE INDEX idx_plates_0 ON barcodes.plates ( person_id );

COMMENT ON COLUMN barcodes.plates.person_id IS 'Who plated the samples';

CREATE TABLE barcodes.primers ( 
	primer_id            bigserial  NOT NULL,
	primer_name          varchar  ,
	company              varchar  NOT NULL,
	linker               varchar  NOT NULL,
	fwd_primer           varchar  NOT NULL,
	rev_primer           varchar  NOT NULL,
	barcodes             json  NOT NULL,
	CONSTRAINT pk_primers PRIMARY KEY ( primer_id )
 );

CREATE TABLE barcodes.primers_lots ( 
	primer_id            bigint  NOT NULL,
	lot                  varchar  ,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	person_id            bigint  NOT NULL,
	CONSTRAINT pk_primers_lots UNIQUE ( lot ) ,
	CONSTRAINT fk_primers_lots FOREIGN KEY ( primer_id ) REFERENCES barcodes.primers( primer_id )    ,
	CONSTRAINT fk_primers_lots_0 FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    
 );

CREATE INDEX idx_primers_lots ON barcodes.primers_lots ( primer_id );

CREATE INDEX idx_primers_lots_0 ON barcodes.primers_lots ( person_id );

CREATE TABLE barcodes.project ( 
	project_id           bigserial  NOT NULL,
	project              varchar(1000)  NOT NULL,
	description          varchar  ,
	pi                   bigint  ,
	contact_person       bigint  ,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT project_pkey PRIMARY KEY ( project_id )
 );

COMMENT ON COLUMN barcodes.project.pi IS 'primary investigator on the study';

CREATE TABLE barcodes.run ( 
	run_id               bigserial  NOT NULL,
	name                 varchar(100)  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	created_by           bigint  NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	finalized_on         timestamp  ,
	finalized_by         bigint  ,
	CONSTRAINT idx_run_0 UNIQUE ( name ) ,
	CONSTRAINT pk_run PRIMARY KEY ( run_id ),
	CONSTRAINT fk_run FOREIGN KEY ( finalized_by ) REFERENCES barcodes.people( person_id )    
 );

CREATE INDEX idx_run ON barcodes.run ( finalized_by );

COMMENT ON TABLE barcodes.run IS 'Full run, equivalent to a multi-lane sequencing run';

CREATE TABLE barcodes.samples ( 
	sample_id            bigserial  NOT NULL,
	external_name        varchar(100)  NOT NULL,
	barcode              varchar  ,
	project_id           bigint  NOT NULL,
	sample_type          varchar  NOT NULL,
	sample_location      varchar  ,
	biomass_remaining    bool DEFAULT 'T' NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	created_by           bigint  NOT NULL,
	last_scanned         timestamp DEFAULT current_timestamp NOT NULL,
	last_scanned_by      bigint  NOT NULL,
	CONSTRAINT pk_samples PRIMARY KEY ( sample_id ),
	CONSTRAINT pk_samples_0 UNIQUE ( external_name ) ,
	CONSTRAINT fk_samples FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )    ,
	CONSTRAINT fk_samples_1 FOREIGN KEY ( last_scanned_by ) REFERENCES barcodes.people( person_id )    ,
	CONSTRAINT fk_samples_2 FOREIGN KEY ( created_by ) REFERENCES barcodes.people( person_id )    ,
	CONSTRAINT fk_samples_0 FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id )    
 );

CREATE INDEX idx_samples ON barcodes.samples ( barcode );

CREATE INDEX idx_samples_0 ON barcodes.samples ( project_id );

CREATE INDEX idx_samples_1 ON barcodes.samples ( last_scanned_by );

CREATE INDEX idx_samples_2 ON barcodes.samples ( created_by );

COMMENT ON COLUMN barcodes.samples.sample_type IS 'The type of sample collected (stool, soil, etc)';

COMMENT ON COLUMN barcodes.samples.sample_location IS 'Physical location of sample tube';

COMMENT ON COLUMN barcodes.samples.last_scanned_by IS 'Pereson who last scanned the barcode';

CREATE TABLE barcodes.users ( 
	username             varchar  NOT NULL,
	pass                 varchar(36)  NOT NULL,
	person_id            integer  NOT NULL,
	"access"             integer  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT pk_users PRIMARY KEY ( username ),
	CONSTRAINT fk_users FOREIGN KEY ( person_id ) REFERENCES barcodes.people( person_id )    
 );

CREATE INDEX idx_users ON barcodes.users ( person_id );

COMMENT ON COLUMN barcodes.users."access" IS 'What access the user is allowed';

CREATE TABLE barcodes.plates_samples ( 
	plate_barcode        varchar  NOT NULL,
	sample_id            bigint  NOT NULL,
	well                 varchar(3)  NOT NULL,
	CONSTRAINT idx_plate_samples PRIMARY KEY ( plate_barcode, sample_id ),
	CONSTRAINT fk_plate_samples FOREIGN KEY ( sample_id ) REFERENCES barcodes.samples( sample_id )    ,
	CONSTRAINT fk_plate_samples_0 FOREIGN KEY ( plate_barcode ) REFERENCES barcodes.plates( plate_barcode )    
 );

CREATE INDEX idx_plate_samples_0 ON barcodes.plates_samples ( sample_id );

CREATE INDEX idx_plate_samples_1 ON barcodes.plates_samples ( plate_barcode );

CREATE TABLE barcodes.pool ( 
	pool_id              bigserial  NOT NULL,
	run_id               bigint  ,
	name                 varchar(100)  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	created_by           bigint  NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	finalized_on         timestamp  ,
	finalized_by         bigint  NOT NULL,
	CONSTRAINT idx_pool_2 UNIQUE ( name ) ,
	CONSTRAINT pk_pool PRIMARY KEY ( pool_id ),
	CONSTRAINT fk_pool FOREIGN KEY ( run_id ) REFERENCES barcodes.run( run_id )    ,
	CONSTRAINT fk_pool_0 FOREIGN KEY ( created_by ) REFERENCES barcodes.people( person_id )    ,
	CONSTRAINT fk_pool_1 FOREIGN KEY ( finalized_by ) REFERENCES barcodes.people( person_id )    
 );

CREATE INDEX idx_pool ON barcodes.pool ( run_id );

CREATE INDEX idx_pool_0 ON barcodes.pool ( created_by );

CREATE INDEX idx_pool_1 ON barcodes.pool ( finalized_by );

COMMENT ON TABLE barcodes.pool IS 'Pool of samples, equivalent to a single lane for sequencing';

CREATE TABLE barcodes.project_sample ( 
	sample_id            bigint  NOT NULL,
	project_id           bigint  NOT NULL,
	external_name        varchar(100)  NOT NULL,
	CONSTRAINT project_barcode_pkey PRIMARY KEY ( project_id, external_name ),
	CONSTRAINT pk_project_sample UNIQUE ( sample_id ) ,
	CONSTRAINT fk_pb_to_project FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id )    ,
	CONSTRAINT fk_project_external_name FOREIGN KEY ( external_name ) REFERENCES barcodes.samples( external_name )    ,
	CONSTRAINT fk_project_sample FOREIGN KEY ( sample_id ) REFERENCES barcodes.samples( sample_id )    
 );

CREATE INDEX idx_project_external_name ON barcodes.project_sample ( external_name );

CREATE TABLE barcodes.protocol_settings ( 
	protocol_settings_id bigserial  NOT NULL,
	protocol_id          integer  ,
	sample_id            bigint  ,
	plate_barcode        varchar  ,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	created_by           bigint  NOT NULL,
	CONSTRAINT pk_protocol_runs PRIMARY KEY ( protocol_settings_id ),
	CONSTRAINT fk_protocol_runs FOREIGN KEY ( created_by ) REFERENCES barcodes.people( person_id )    ,
	CONSTRAINT fk_protocol_runs_1 FOREIGN KEY ( plate_barcode ) REFERENCES barcodes.plates( plate_barcode )    ,
	CONSTRAINT fk_protocol_runs_2 FOREIGN KEY ( sample_id ) REFERENCES barcodes.samples( sample_id )    
 );

CREATE INDEX idx_protocol_runs ON barcodes.protocol_settings ( created_by );

CREATE INDEX idx_protocol_runs_1 ON barcodes.protocol_settings ( plate_barcode );

CREATE INDEX idx_protocol_runs_2 ON barcodes.protocol_settings ( sample_id );

CREATE TABLE barcodes.extraction_settings ( 
	extractionkit_lot    varchar(40)  NOT NULL,
	extraction_robot     varchar(40)  NOT NULL,
	tm1000_8_tool        varchar(40)  NOT NULL,
	CONSTRAINT fk_extraction_settings FOREIGN KEY (  ) REFERENCES barcodes.protocol_settings(  )    
 );

CREATE TABLE barcodes.pcr_settings ( 
	protocol_settings_id bigint  NOT NULL,
	extraction_protocol_settings_id bigint  ,
	primer_lot           varchar  NOT NULL,
	mastermix_lot        varchar(40)  NOT NULL,
	water_lot            varchar(40)  NOT NULL,
	processing_robot     varchar(40)  NOT NULL,
	tm300_8_tool         varchar(40)  NOT NULL,
	tm50_8_tool          varchar(40)  NOT NULL,
	CONSTRAINT pk_hardcode_settings UNIQUE ( protocol_settings_id ) ,
	CONSTRAINT pk_hardcode_settings_0 PRIMARY KEY ( protocol_settings_id ),
	CONSTRAINT fk_hardcode_settings FOREIGN KEY ( primer_lot ) REFERENCES barcodes.primers_lots( lot )    ,
	CONSTRAINT fk_hardcode_settings_0 FOREIGN KEY ( protocol_settings_id ) REFERENCES barcodes.protocol_settings( protocol_settings_id )    ,
	CONSTRAINT fk_pcr_settings FOREIGN KEY ( extraction_protocol_settings_id ) REFERENCES barcodes.protocol_settings( protocol_settings_id )    
 );

CREATE INDEX idx_hardcode_settings ON barcodes.pcr_settings ( primer_lot );

CREATE INDEX idx_pcr_settings ON barcodes.pcr_settings ( extraction_protocol_settings_id );

CREATE TABLE barcodes.pool_samples ( 
	pool_id              bigint  NOT NULL,
	protocol_settings_id bigint  NOT NULL,
	volume               varchar  ,
	CONSTRAINT fk_pool_samples FOREIGN KEY ( pool_id ) REFERENCES barcodes.pool( pool_id )    ,
	CONSTRAINT fk_pool_samples_0 FOREIGN KEY ( protocol_settings_id ) REFERENCES barcodes.protocol_settings( protocol_settings_id )    
 );

CREATE INDEX idx_pool_samples ON barcodes.pool_samples ( pool_id );

CREATE INDEX idx_pool_samples_0 ON barcodes.pool_samples ( protocol_settings_id );

COMMENT ON COLUMN barcodes.pool_samples.volume IS 'Volume used from each plate/sample for final pool';
