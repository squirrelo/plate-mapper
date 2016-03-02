CREATE SCHEMA barcodes;

CREATE TABLE barcodes.access_controls ( 
	access_level         varchar(30)  NOT NULL,
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

CREATE TABLE barcodes.person ( 
	person_id            bigserial  NOT NULL,
	name                 varchar(100)  NOT NULL,
	email                varchar  NOT NULL,
	address              varchar(100)  ,
	affiliation          varchar  ,
	phone                varchar(20)  ,
	CONSTRAINT pk_people PRIMARY KEY ( person_id )
 );

CREATE TABLE barcodes.plate ( 
	plate_id             varchar  NOT NULL,
	plate                varchar(100)  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	person_id            bigint  NOT NULL,
	"rows"               smallint  NOT NULL,
	cols                 smallint  NOT NULL,
	CONSTRAINT idx_plates UNIQUE ( plate_id ) ,
	CONSTRAINT pk_plates PRIMARY KEY ( plate_id ),
	CONSTRAINT fk_plates FOREIGN KEY ( plate_id ) REFERENCES barcodes.barcode( barcode )    ,
	CONSTRAINT fk_plates_0 FOREIGN KEY ( person_id ) REFERENCES barcodes.person( person_id )    
 );

CREATE INDEX idx_plates_0 ON barcodes.plate ( person_id );

COMMENT ON COLUMN barcodes.plate.plate_id IS 'The barcode assigned to the plate';

COMMENT ON COLUMN barcodes.plate.plate IS 'Name of the plate';

COMMENT ON COLUMN barcodes.plate.person_id IS 'Who plated the samples';

COMMENT ON COLUMN barcodes.plate."rows" IS 'Number of rows on plate';

COMMENT ON COLUMN barcodes.plate.cols IS 'Number of columns on plate';

CREATE TABLE barcodes.primer_set ( 
	primer_set_id        bigserial  NOT NULL,
	primer_set           varchar  ,
	company              varchar  NOT NULL,
	linker               varchar  NOT NULL,
	fwd_primer           varchar  NOT NULL,
	rev_primer           varchar  NOT NULL,
	barcodes             json  NOT NULL,
	CONSTRAINT pk_primers PRIMARY KEY ( primer_set_id )
 );

COMMENT ON COLUMN barcodes.primer_set.primer_set IS 'Name of the primer set';

CREATE TABLE barcodes.primer_set_lots ( 
	primer_set_id        bigint  NOT NULL,
	primer_lot           varchar  ,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	person_id            bigint  NOT NULL,
	CONSTRAINT pk_primers_lots UNIQUE ( primer_lot ) ,
	CONSTRAINT fk_primers_lots FOREIGN KEY ( primer_set_id ) REFERENCES barcodes.primer_set( primer_set_id )    ,
	CONSTRAINT fk_primers_lots_0 FOREIGN KEY ( person_id ) REFERENCES barcodes.person( person_id )    
 );

CREATE INDEX idx_primers_lots ON barcodes.primer_set_lots ( primer_set_id );

CREATE INDEX idx_primers_lots_0 ON barcodes.primer_set_lots ( person_id );

CREATE TABLE barcodes.project ( 
	project_id           bigserial  NOT NULL,
	project              varchar(1000)  NOT NULL,
	description          varchar  ,
	pi                   varchar  NOT NULL,
	contact_person       varchar  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT project_pkey PRIMARY KEY ( project_id )
 );

COMMENT ON TABLE barcodes.project IS 'Project information';

COMMENT ON COLUMN barcodes.project.pi IS 'primary investigator on the study';

CREATE TABLE barcodes.project_barcodes ( 
	project_id           bigint  NOT NULL,
	barcode              varchar  NOT NULL,
	CONSTRAINT idx_project_barcode_1 PRIMARY KEY ( project_id, barcode ),
	CONSTRAINT fk_project_barcode_0 FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )    ,
	CONSTRAINT fk_project_barcode FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id )    
 );

CREATE INDEX idx_project_barcode ON barcodes.project_barcodes ( project_id );

CREATE INDEX idx_project_barcode_0 ON barcodes.project_barcodes ( barcode );

COMMENT ON TABLE barcodes.project_barcodes IS 'Assign barcodes to projects before they are assigned to samples';

CREATE TABLE barcodes.run ( 
	run_id               bigserial  NOT NULL,
	run                  varchar(100)  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	created_by           bigint  NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	finalized_on         timestamp  ,
	finalized_by         bigint  ,
	CONSTRAINT idx_run_0 UNIQUE ( run ) ,
	CONSTRAINT pk_run PRIMARY KEY ( run_id ),
	CONSTRAINT fk_run FOREIGN KEY ( finalized_by ) REFERENCES barcodes.person( person_id )    
 );

CREATE INDEX idx_run ON barcodes.run ( finalized_by );

COMMENT ON TABLE barcodes.run IS 'Full run, equivalent to a multi-lane sequencing run';

COMMENT ON COLUMN barcodes.run.run IS 'Name of the run';

CREATE TABLE barcodes.sample_set ( 
	sample_set_id        bigserial  NOT NULL,
	sample_set           varchar(100)  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp ,
	created_by           bigint  NOT NULL,
	CONSTRAINT pk_sample_set PRIMARY KEY ( sample_set_id )
 );

COMMENT ON TABLE barcodes.sample_set IS 'Distinct set of samples that must have unique sample names in them';

CREATE TABLE barcodes.settings ( 
	test                 bool DEFAULT 'F' NOT NULL
 );

COMMENT ON COLUMN barcodes.settings.test IS 'Whether test environment or not.';
INSERT INTO barcodes.settings (test) VALUES ('F');

CREATE TABLE barcodes."user" ( 
	user_id              varchar  NOT NULL,
	pass                 varchar(60)  NOT NULL,
	person_id            integer  NOT NULL,
	"access"             integer  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	CONSTRAINT pk_users PRIMARY KEY ( user_id ),
	CONSTRAINT fk_users FOREIGN KEY ( person_id ) REFERENCES barcodes.person( person_id )    
 );

CREATE INDEX idx_users ON barcodes."user" ( person_id );

COMMENT ON COLUMN barcodes."user".user_id IS 'username of the user';

COMMENT ON COLUMN barcodes."user".pass IS 'bcrypt hashed password';

COMMENT ON COLUMN barcodes."user"."access" IS 'What access the user is allowed';

CREATE TABLE barcodes.pool ( 
	pool_id              bigserial  NOT NULL,
	run_id               bigint  ,
	pool                 varchar(100)  NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	created_by           bigint  NOT NULL,
	finalized            bool DEFAULT 'F' NOT NULL,
	finalized_on         timestamp  ,
	finalized_by         bigint  NOT NULL,
	CONSTRAINT idx_pool_2 UNIQUE ( pool ) ,
	CONSTRAINT pk_pool PRIMARY KEY ( pool_id ),
	CONSTRAINT fk_pool FOREIGN KEY ( run_id ) REFERENCES barcodes.run( run_id )    ,
	CONSTRAINT fk_pool_0 FOREIGN KEY ( created_by ) REFERENCES barcodes.person( person_id )    ,
	CONSTRAINT fk_pool_1 FOREIGN KEY ( finalized_by ) REFERENCES barcodes.person( person_id )    
 );

CREATE INDEX idx_pool ON barcodes.pool ( run_id );

CREATE INDEX idx_pool_0 ON barcodes.pool ( created_by );

CREATE INDEX idx_pool_1 ON barcodes.pool ( finalized_by );

COMMENT ON TABLE barcodes.pool IS 'Pool of samples, equivalent to a single lane for sequencing';

COMMENT ON COLUMN barcodes.pool.pool IS 'Name of the pool';

CREATE TABLE barcodes.project_sample_sets ( 
	project_id           bigint  NOT NULL,
	sample_set_id        bigint  NOT NULL,
	CONSTRAINT idx_project_sample_sets_1 PRIMARY KEY ( project_id, sample_set_id ),
	CONSTRAINT fk_project_sample_sets FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id )    ,
	CONSTRAINT fk_project_sample_sets_0 FOREIGN KEY ( sample_set_id ) REFERENCES barcodes.sample_set( sample_set_id )    
 );

CREATE INDEX idx_project_sample_sets ON barcodes.project_sample_sets ( project_id );

CREATE INDEX idx_project_sample_sets_0 ON barcodes.project_sample_sets ( sample_set_id );

CREATE TABLE barcodes.sample ( 
	sample_id            bigserial  NOT NULL,
	sample               varchar(100)  NOT NULL,
	barcode              varchar  ,
	sample_set_id        bigint  NOT NULL,
	sample_type          varchar  NOT NULL,
	sample_location      varchar  ,
	biomass_remaining    bool DEFAULT 'T' NOT NULL,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	created_by           bigint  NOT NULL,
	last_scanned         timestamp DEFAULT current_timestamp NOT NULL,
	last_scanned_by      bigint  NOT NULL,
	CONSTRAINT idx_samples UNIQUE ( barcode ) ,
	CONSTRAINT pk_samples PRIMARY KEY ( sample_id ),
	CONSTRAINT pk_samples_0 UNIQUE ( sample ) ,
	CONSTRAINT idx_sample UNIQUE ( sample_set_id, sample ) ,
	CONSTRAINT fk_samples FOREIGN KEY ( barcode ) REFERENCES barcodes.barcode( barcode )    ,
	CONSTRAINT fk_samples_1 FOREIGN KEY ( last_scanned_by ) REFERENCES barcodes.person( person_id )    ,
	CONSTRAINT fk_samples_2 FOREIGN KEY ( created_by ) REFERENCES barcodes.person( person_id )    ,
	CONSTRAINT fk_samples_0 FOREIGN KEY ( sample_set_id ) REFERENCES barcodes.sample_set( sample_set_id )    
 );

CREATE INDEX idx_samples_1 ON barcodes.sample ( last_scanned_by );

CREATE INDEX idx_samples_2 ON barcodes.sample ( created_by );

CREATE INDEX idx_samples_0 ON barcodes.sample ( sample_set_id );

COMMENT ON COLUMN barcodes.sample.sample IS 'External name of the sample';

COMMENT ON COLUMN barcodes.sample.sample_type IS 'The type of sample collected (stool, soil, etc)';

COMMENT ON COLUMN barcodes.sample.sample_location IS 'Physical location of sample tube';

COMMENT ON COLUMN barcodes.sample.last_scanned_by IS 'Pereson who last scanned the barcode';

CREATE TABLE barcodes.plates_samples ( 
	plate_id             varchar  NOT NULL,
	sample_id            bigint  NOT NULL,
	plate_row            smallint  NOT NULL,
	plate_col            smallint  NOT NULL,
	CONSTRAINT idx_plates_samples_0 UNIQUE ( plate_id, plate_row, plate_col ) ,
	CONSTRAINT fk_plate_samples_0 FOREIGN KEY ( plate_id ) REFERENCES barcodes.plate( plate_id )    ,
	CONSTRAINT fk_plates_samples FOREIGN KEY ( sample_id ) REFERENCES barcodes.sample( sample_id )    
 );

CREATE INDEX idx_plate_samples_1 ON barcodes.plates_samples ( plate_id );

CREATE INDEX idx_plates_samples ON barcodes.plates_samples ( sample_id );

CREATE TABLE barcodes.project_samples ( 
	sample_id            bigint  NOT NULL,
	project_id           bigint  NOT NULL,
	CONSTRAINT fk_project_sample_set_0 FOREIGN KEY ( project_id ) REFERENCES barcodes.project( project_id )    ,
	CONSTRAINT fk_project_samples FOREIGN KEY ( sample_id ) REFERENCES barcodes.sample( sample_id )    
 );

CREATE INDEX idx_project_sample_set ON barcodes.project_samples ( sample_id );

CREATE INDEX idx_project_sample_set_0 ON barcodes.project_samples ( project_id );

CREATE TABLE barcodes.protocol_settings ( 
	protocol_settings_id bigserial  NOT NULL,
	protocol_id          integer  ,
	sample_id            bigint  ,
	plate_id             varchar  ,
	created_on           timestamp DEFAULT current_timestamp NOT NULL,
	created_by           bigint  NOT NULL,
	CONSTRAINT pk_protocol_runs PRIMARY KEY ( protocol_settings_id ),
	CONSTRAINT fk_protocol_runs FOREIGN KEY ( created_by ) REFERENCES barcodes.person( person_id )    ,
	CONSTRAINT fk_protocol_runs_1 FOREIGN KEY ( plate_id ) REFERENCES barcodes.plate( plate_id )    ,
	CONSTRAINT fk_protocol_runs_2 FOREIGN KEY ( sample_id ) REFERENCES barcodes.sample( sample_id )    
 );

CREATE INDEX idx_protocol_runs ON barcodes.protocol_settings ( created_by );

CREATE INDEX idx_protocol_runs_1 ON barcodes.protocol_settings ( plate_id );

CREATE INDEX idx_protocol_runs_2 ON barcodes.protocol_settings ( sample_id );

CREATE TABLE barcodes.extraction_settings ( 
	protocol_settings_id bigint  NOT NULL,
	extractionkit_lot    varchar(40)  NOT NULL,
	extraction_robot     varchar(40)  NOT NULL,
	tm1000_8_tool        varchar(40)  NOT NULL,
	CONSTRAINT fk_extraction_settings FOREIGN KEY ( protocol_settings_id ) REFERENCES barcodes.protocol_settings( protocol_settings_id )    
 );

CREATE INDEX idx_extraction_settings ON barcodes.extraction_settings ( protocol_settings_id );

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
	CONSTRAINT fk_hardcode_settings FOREIGN KEY ( primer_lot ) REFERENCES barcodes.primer_set_lots( primer_lot )    ,
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
