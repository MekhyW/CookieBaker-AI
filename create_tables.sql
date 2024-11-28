DROP TABLE IF EXISTS client_commands;
CREATE TABLE client_commands (
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    client_commands JSONB NOT NULL
);

DROP TABLE IF EXISTS logs;
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    chat_id VARCHAR(255) NOT NULL,
    log_type VARCHAR(255) NOT NULL,
    log_data JSONB NOT NULL
);