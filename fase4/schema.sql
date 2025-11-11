CREATE TABLE sensores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR NOT NULL
);

CREATE TABLE leituras (
    id SERIAL PRIMARY KEY,
    valor FLOAT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sensor_id INTEGER REFERENCES sensores(id)
);

CREATE TABLE predicts (
    id SERIAL PRIMARY KEY,
    valor INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_sensores_id ON sensores (id);
CREATE INDEX ix_leituras_id ON leituras (id);
CREATE INDEX ix_predicts_id ON predicts (id);
