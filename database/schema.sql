USE plants;
GO

-- Drop dependent tables first
IF OBJECT_ID('beta.reading', 'U') IS NOT NULL 
    DROP TABLE beta.reading;
IF OBJECT_ID('beta.plant', 'U') IS NOT NULL 
    DROP TABLE beta.plant;
IF OBJECT_ID('beta.botanist', 'U') IS NOT NULL 
    DROP TABLE beta.botanist;
IF OBJECT_ID('beta.region', 'U') IS NOT NULL 
    DROP TABLE beta.region;

-- Recreate tables
CREATE TABLE beta.botanist (
    botanist_id SMALLINT PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255)
);

CREATE TABLE beta.region (
    region_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255)
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
    region_id SMALLINT,
    FOREIGN KEY (botanist_id) REFERENCES beta.botanist(botanist_id),
    FOREIGN KEY (region_id) REFERENCES beta.region(region_id)
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

INSERT INTO beta.botanist (
    botanist_id,
    name,
    phone,
    email
)
VALUES
(1, 'Carl Linnaeus', '(146)994-1635x35992', 'carl.linnaeus@lnhm.co.uk'),
(2, 'Eliza Andrews', '(846)669-6651x75948', 'eliza.andrews@lnhm.co.uk'),
(3, 'Gertrude Jekyll', '001-481-273-3691x127', 'gertrude.jekyll@lnhm.co.uk');
GO

INSERT INTO beta.region (name) VALUES
    ('America/Sao_Paulo'),   -- ID: 1
    ('America/Los_Angeles'), -- ID: 2
    ('Africa/Lagos'),        -- ID: 3
    ('Asia/Kolkata'),        -- ID: 4
    ('America/Toronto'),     -- ID: 5
    ('Africa/Abidjan'),      -- ID: 6
    ('Europe/Berlin'),       -- ID: 7
    ('Europe/Zagreb'),       -- ID: 8
    ('Pacific/Honolulu'),    -- ID: 9
    ('America/Chicago'),     -- ID: 10
    ('Europe/Paris'),        -- ID: 11
    ('Africa/Tunis'),        -- ID: 12
    ('Asia/Jakarta'),        -- ID: 13
    ('Africa/Gaborone'),     -- ID: 14
    ('Europe/Madrid'),       -- ID: 15
    ('Asia/Tokyo'),          -- ID: 16
    ('Africa/Khartoum'),     -- ID: 17
    ('Africa/Algiers'),      -- ID: 18
    ('Europe/Kiev'),         -- ID: 19
    ('America/New_York'),    -- ID: 20
    ('Asia/Shanghai'),       -- ID: 21
    ('America/Santiago'),    -- ID: 22
    ('Africa/Dar_es_Salaam'),-- ID: 23
    ('Asia/Manila'),         -- ID: 24
    ('America/Mexico_City'), -- ID: 25
    ('Europe/Rome'),         -- ID: 26
    ('Africa/Blantyre'),     -- ID: 27
    ('America/Mexico_City'), -- ID: 28
    ('America/El_Salvador'); -- ID: 29
GO

INSERT INTO beta.plant (plant_id, name, scientific_name, origin_lat, origin_lon, origin_city, origin_country, botanist_id, region_id) VALUES
    (0, 'Epipremnum Aureum', 'Epipremnum aureum', '-19.32556', '-41.25528', 'Resplendor', 'BR', 1, 1),
    (1, 'Venus flytrap', NULL, '33.95015', '-118.03917', 'South Whittier', 'US', 3, 2),
    (2, 'Corpse flower', NULL, '7.65649', '4.92235', 'Efon-Alaaye', 'NG', 1, 3),
    (3, 'Rafflesia arnoldii', NULL, '-19.32556', '-41.25528', 'Resplendor', 'BR', 2, 1),
    (4, 'Black bat flower', NULL, '13.70167', '-89.10944', 'Ilopango', 'SV', 1, 29),
    (5, 'Pitcher plant', 'Sarracenia catesbaei', '22.88783', '84.13864', 'Jashpurnagar', 'IN', 1, 4),
    (6, 'Wollemi pine', 'Wollemia nobilis', '43.86682', '-79.2663', 'Markham', 'CA', 2, 5),
    (7, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (8, 'Bird of paradise', 'Heliconia schiedeana ''Fire and Ice''', '5.27247', '-3.59625', 'Bonoua', 'CI', 2, 6),
    (9, 'Cactus', 'Pereskia grandifolia', '50.9803', '11.32903', 'Weimar', 'DE', 3, 7),
    (10, 'Dragon tree,', NULL, '43.50891', '16.43915', 'Split', 'HR', 3, 8),
    (11, 'Asclepias Curassavica', 'Asclepias curassavica', '20.88953', '-156.47432', 'Kahului', 'US', 3, 9),
    (12, 'Brugmansia X Candida', NULL, '32.5007', '-94.74049', 'Longview', 'US', 2, 10),
    (13, 'Canna ‘Striata’', NULL, '49.68369', '8.61839', 'Bensheim', 'DE', 2, 7),
    (14, 'Colocasia Esculenta', 'Colocasia esculenta', '29.65163', '-82.32483', 'Gainesville', 'US', 3, 20),
    (15, 'Cuphea ‘David Verity’', NULL, '36.08497', '9.37082', 'Siliana', 'TN', 3, 12),
    (16, 'Euphorbia Cotinifolia', 'Euphorbia cotinifolia', '40.93121', '-73.89875', 'Yonkers', 'US', 3, 20),
    (17, 'Ipomoea Batatas', 'Ipomoea batatas', '-7.51611', '109.05389', 'Wangon', 'ID', 1, 13),
    (18, 'Manihot Esculenta ‘Variegata’', NULL, '51.30001', '13.10984', 'Oschatz', 'DE', 1, 7),
    (19, 'Musa Basjoo', 'Musa basjoo', '-21.44236', '27.46153', 'Tonota', 'BW', 3, 14),
    (20, 'Salvia Splendens', 'Salvia splendens', '41.15612', '1.10687', 'Reus', 'ES', 1, 15),
    (21, 'Anthurium', 'Anthurium andraeanum', '-29.2975', '-51.50361', 'Carlos Barbosa', 'BR', 2, 1),
    (22, 'Bird of Paradise', 'Heliconia schiedeana ''Fire and Ice''', '48.35693', '10.98461', 'Friedberg', 'DE', 3, 7),
    (23, 'Cordyline Fruticosa', 'Cordyline fruticosa', '52.53048', '13.29371', 'Charlottenburg-Nord', 'DE', 2, 7),
    (24, 'Ficus', 'Ficus carica', '43.82634', '144.09638', 'Motomachi', 'JP', 1, 16),
    (25, 'Palm Trees', NULL, '11.8659', '34.3869', 'Ar Ruseris', 'SD', 3, 17),
    (26, 'Dieffenbachia Seguine', 'Dieffenbachia seguine', '36.06386', '4.62744', 'El Achir', 'DZ', 1, 18),
    (27, 'Spathiphyllum', 'Spathiphyllum (group)', '51.67822', '33.9162', 'Hlukhiv', 'UA', 1, 19),
    (28, 'Croton', 'Codiaeum variegatum', '43.91452', '-69.96533', 'Brunswick', 'US', 1, 20),
    (29, 'Aloe Vera', 'Aloe vera', '34.75856', '136.13108', 'Ueno-ebisumachi', 'JP', 3, 16),
    (30, 'Ficus Elastica', 'Ficus elastica', '30.75545', '20.22625', 'Ajdabiya', 'LY', 1, 18),
    (31, 'Sansevieria Trifasciata', 'Sansevieria trifasciata', '23.29549', '113.82465', 'Licheng', 'CN', 3, 21),
    (32, 'Philodendron Hederaceum', 'Philodendron hederaceum', '52.47774', '10.5511', 'Gifhorn', 'DE', 3, 7),
    (33, 'Schefflera Arboricola', 'Schefflera arboricola', '28.92694', '78.23456', 'Bachhraon', 'IN', 1, 4),
    (34, 'Aglaonema Commutatum', 'Aglaonema commutatum', '41.15612', '1.10687', 'Reus', 'ES', 3, 15),
    (35, 'Monstera Deliciosa', 'Monstera deliciosa', '-32.45242', '-71.23106', 'La Ligua', 'CL', 1, 22),
    (36, 'Tacca Integrifolia', 'Tacca integrifolia', '32.54044', '-82.90375', 'Dublin', 'US', 3, 20),
    (37, 'Psychopsis Papilio', NULL, '30.21121', '74.4818', 'Malaut', 'IN', 2, 4),
    (38, 'Saintpaulia Ionantha', 'Saintpaulia ionantha', '-6.8', '39.25', 'Magomeni', 'TZ', 3, 23),
    (39, 'Gaillardia', 'Gaillardia aestivalis', '36.24624', '139.07204', 'Fujioka', 'JP', 1, 16),
    (40, 'Amaryllis', 'Hippeastrum (group)', '44.92801', '4.8951', 'Valence', 'FR', 2, 11),
    (41, 'Caladium Bicolor', 'Caladium bicolor', '22.4711', '88.1453', 'Pujali', 'IN', 1, 4),
    (42, 'Chlorophytum Comosum', 'Chlorophytum comosum ''Vittatum''', '41.57439', '24.71204', 'Smolyan', 'BG', 1, 15),
    (43, 'loan plant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (44, 'Araucaria Heterophylla', 'Araucaria heterophylla', '20.22816', '-103.5687', 'Zacoalco de Torres', 'MX', 3, 28),
    (45, 'Begonia', 'Begonia ''Art Hodes''', '33.95015', '-118.03917', 'South Whittier', 'US', 3, 2),
    (46, 'Medinilla Magnifica', 'Medinilla magnifica', '-13.7804', '34.4587', 'Salima', 'MW', 2, 27),
    (47, 'Calliandra Haematocephala', 'Calliandra haematocephala', '37.49223', '15.07041', 'Catania', 'IT', 2, 26),
    (48, 'Zamioculcas Zamiifolia', 'Zamioculcas zamiifolia', '14.14989', '121.3152', 'Calauan', 'PH', 1, 24),
    (49, 'Crassula Ovata', 'Crassula ovata', '17.94979', '-94.91386', 'Acayucan', 'MX', 2, 28),
    (50, 'Epipremnum Aureum', 'Epipremnum aureum', '-19.32556', '-41.25528', 'Resplendor', 'BR', 1, 1);
GO
