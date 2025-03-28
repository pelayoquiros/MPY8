
CREATE DATABASE IF NOT EXISTS deportes_db;
USE deportes_db;

CREATE TABLE IF NOT EXISTS match_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    season VARCHAR(10),
    date DATE,
    home_team VARCHAR(50),
    away_team VARCHAR(50),
    home_score INT,
    away_score INT
);

CREATE TABLE IF NOT EXISTS player_rankings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(100),
    team VARCHAR(50),
    position VARCHAR(20),
    rating FLOAT
);

-- Insertar datos de muestra para resultados de partidos
INSERT INTO match_results (season, date, home_team, away_team, home_score, away_score) VALUES
('2022-2023', '2023-01-01', 'Barcelona', 'Real Madrid', 3, 2),
('2022-2023', '2023-01-08', 'Atletico Madrid', 'Sevilla', 1, 1),
('2022-2023', '2023-01-15', 'Valencia', 'Villarreal', 0, 2);

-- Insertar datos de muestra para rankings de jugadores
INSERT INTO player_rankings (player_name, team, position, rating) VALUES
('Lionel Messi', 'PSG', 'Delantero', 92.5),
('Cristiano Ronaldo', 'Al Nassr', 'Delantero', 91.0),
('Kevin De Bruyne', 'Manchester City', 'Centrocampista', 90.5),
('Virgil van Dijk', 'Liverpool', 'Defensa', 89.5),
('Thibaut Courtois', 'Real Madrid', 'Portero', 90.0);