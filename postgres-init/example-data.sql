INSERT INTO service_a.pokemons
(name, type, hp, attack, defense, speed, generation, created_at, updated_at)
VALUES
('Bulbasaur', ARRAY['Grass','Poison'], 45, 49, 49, 45, 1, NOW(), NOW()),
('Charmander', ARRAY['Fire'], 39, 52, 43, 65, 1, NOW(), NOW()),
('Squirtle', ARRAY['Water'], 44, 48, 65, 43, 1, NOW(), NOW()),
('Pikachu', ARRAY['Electric'], 35, 55, 40, 90, 1, NOW(), NOW()),
('Jigglypuff', ARRAY['Normal','Fairy'], 115, 45, 20, 20, 1, NOW(), NOW()),
('Meowth', ARRAY['Normal'], 40, 45, 35, 90, 1, NOW(), NOW()),
('Machop', ARRAY['Fighting'], 70, 80, 50, 35, 1, NOW(), NOW()),
('Gastly', ARRAY['Ghost','Poison'], 30, 35, 30, 80, 1, NOW(), NOW()),
('Eevee', ARRAY['Normal'], 55, 55, 50, 55, 1, NOW(), NOW()),
( 'Mewtwo', ARRAY['Psychic'], 106, 110, 90, 130, 1, NOW(), NOW());

INSERT INTO service_b.trainers (name, age, region) VALUES
('Ash Ketchum', 10, 'Kanto'),
('Misty', 12, 'Kanto'),
('Brock', 15, 'Kanto'),
('Gary Oak', 10, 'Kanto'),
('Cynthia', 20, 'Sinnoh');