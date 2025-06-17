DROP TABLE IF EXISTS bronze.coin_master;
CREATE TABLE bronze.coin_master (
    coin_id VARCHAR(100) PRIMARY KEY,
    symbol VARCHAR(50),
    name_coin VARCHAR(150),
    last_refreshed_at TIMESTAMPTZ DEFAULT NOW()
);
DROP TABLE IF EXISTS bronze.coin_platform_contracts;
CREATE TABLE bronze.coin_platform_contracts (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(100) REFERENCES bronze.coin_master(coin_id),
    platform_id VARCHAR(100), -- จะไปเชื่อมกับตาราง asset_platforms ต่อไป
    contract_address TEXT
);
DROP TABLE IF EXISTS bronze.asset_platforms;
CREATE TABLE bronze.asset_platforms (
    platform_id VARCHAR(100) PRIMARY KEY,
    chain_identifier BIGINT,
    name_platform VARCHAR(150),
    shortname VARCHAR(50),
	native_coin_id VARCHAR(100)
);
DROP TABLE IF EXISTS bronze.coin_categories_master; 
CREATE TABLE bronze.coin_categories_master (
    category_id VARCHAR(100) PRIMARY KEY,
    name_category VARCHAR(150)
);
DROP TABLE IF EXISTS bronze.exchange_master;
CREATE TABLE bronze.exchange_master (
    exchange_id VARCHAR(100) PRIMARY KEY,
    name_exchange VARCHAR(150)
);
DROP TABLE IF EXISTS bronze.nft_collection_master;
CREATE TABLE bronze.nft_collection_master (
    nft_id VARCHAR(100) PRIMARY KEY,
    symbol VARCHAR(100),
    name_nft VARCHAR(255),
    asset_platform_id VARCHAR(100) REFERENCES bronze.asset_platforms(platform_id)
);


