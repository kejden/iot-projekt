CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS readings (
    time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    station_id INTEGER,
    station_name TEXT,
    temperature REAL,
    humidity REAL,
    light_level INTEGER
);

SELECT create_hypertable('readings', 'time', if_not_exists => TRUE);
