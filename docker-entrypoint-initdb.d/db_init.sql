CREATE TABLE IF NOT EXISTS configurations
(
    id serial PRIMARY KEY,
    loaded_on TIMESTAMP DEFAULT current_timestamp,
    file_name VARCHAR(256),
    cfg BYTEA 
);

CREATE TABLE IF NOT EXISTS users
(
    id serial PRIMARY KEY,
    username VARCHAR(32) UNIQUE,
    password VARCHAR(32),
    bound_cfg_id integer REFERENCES configurations(id) ON DELETE RESTRICT 
);

CREATE TABLE IF NOT EXISTS users_configurations
(
    user_id integer REFERENCES users(id) ON DELETE CASCADE,
    cfg_id integer REFERENCES configurations(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, cfg_id)
);
