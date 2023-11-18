CREATE TABLE simulations(
    id SERIAL PRIMARY KEY,
    simulation_start TIMESTAMP NOT NULL,
    simulation_end TIMESTAMP,
    last_update TIMESTAMP NOT NULL,
    completion FLOAT NOT NULL
);

CREATE TABLE flying_objects (
    object_id VARCHAR(32) PRIMARY KEY,
    simulation_id INTEGER REFERENCES simulations(id),
    payload VARCHAR(200) NOT NULL,  -- Assuming hex encoded string, 100 bytes
    created_time TIMESTAMP NOT NULL,
    speed FLOAT NOT NULL
);

CREATE TABLE flying_object_states (
    id SERIAL PRIMARY KEY,
    object_id VARCHAR(32) REFERENCES flying_objects(object_id),
    simulation_id INTEGER REFERENCES simulations(id),
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    angle FLOAT,
    state_time TIMESTAMP NOT NULL,
    expire_time FLOAT NOT NULL,
    sector VARCHAR(1) NOT NULL
);

CREATE INDEX idx_flying_object_states_on_object_id_and_time
ON flying_object_states (simulation_id, object_id, state_time);

CREATE INDEX idx_flying_object_states_on_sector_and_time
ON flying_object_states (simulation_id, sector, state_time);