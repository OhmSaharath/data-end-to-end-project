DROP TABLE IF EXISTS bronze.data_coin_list;

CREATE TABLE bronze.data_coin_list(
	id_coin VARCHAR(50),
	symbol VARCHAR(50),
	name_coin VARCHAR(50),
	current_price NUMERIC(20,2),
	market_cap_rank INT,
	price_change_24h NUMERIC(20,2),
	last_updated TIMESTAMPTZ
);