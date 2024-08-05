DROP TABLE IF EXISTS reading;
DROP TABLE IF EXISTS continents;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS botanist;

CREATE TABLE botanist (
    botanist_id SMALLINT PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255)
);

CREATE TABLE plant (
    plant_id SMALLINT PRIMARY KEY,
    name VARCHAR(255),
    scientific_name VARCHAR(255),
    origin_lat VARCHAR(50),
    origin_lon VARCHAR(50),
    origin_city VARCHAR(255),
    origin_initials VARCHAR(10),
    origin_country VARCHAR(255),
    botanist_id SMALLINT,
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id)
);

CREATE TABLE continents (
    continent_id SMALLINT PRIMARY KEY,
    name VARCHAR(255),
    plant_id SMALLINT,
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);

CREATE TABLE reading (
    reading_id BIGINT PRIMARY KEY,
    last_watered DATE,
    soil_moisture FLOAT,
    temperature FLOAT,
    recording_taken TIMESTAMP,
    plant_id SMALLINT,
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);
