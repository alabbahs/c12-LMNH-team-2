USE plants;
GO

IF OBJECT_ID('beta.reading', 'U') IS NOT NULL 
    DROP TABLE beta.reading;
IF OBJECT_ID('beta.continents', 'U') IS NOT NULL 
    DROP TABLE beta.continents;
IF OBJECT_ID('beta.plant', 'U') IS NOT NULL 
    DROP TABLE beta.plant;
IF OBJECT_ID('beta.botanist', 'U') IS NOT NULL 
    DROP TABLE beta.botanist;

CREATE TABLE beta.botanist (
    botanist_id SMALLINT PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255)
);

CREATE TABLE beta.plant (
    plant_id SMALLINT PRIMARY KEY,
    name VARCHAR(255),
    scientific_name VARCHAR(255),
    origin_lat VARCHAR(50),
    origin_lon VARCHAR(50),
    origin_city VARCHAR(255),
    origin_country VARCHAR(255),
    botanist_id SMALLINT,
    FOREIGN KEY (botanist_id) REFERENCES beta.botanist(botanist_id)
);

CREATE TABLE beta.continents (
    continent_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    plant_id SMALLINT,
    FOREIGN KEY (plant_id) REFERENCES beta.plant(plant_id)
);

CREATE TABLE beta.reading (
    reading_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    last_watered DATE,
    soil_moisture FLOAT,
    temperature FLOAT,
    recording_taken DATETIME,
    plant_id SMALLINT,
    FOREIGN KEY (plant_id) REFERENCES beta.plant(plant_id)
);
GO
