create table if not exists user_interactions_raw (
    interaction_id integer,
    user_id integer,
    product_id integer,
    action varchar(500),
    timestamp timestamp,
	CONSTRAINT pk_interaction_user_product PRIMARY KEY (interaction_id,user_id, product_id)
);

CREATE INDEX user_interactions_per_day ON user_interactions_raw (timestamp);

\copy user_interactions_raw FROM '/Library/PostgreSQL/16/bin/Database/sample.csv' DELIMITER ',' CSV HEADER;
