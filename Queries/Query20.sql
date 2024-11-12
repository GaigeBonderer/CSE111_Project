.headers on
-- Query #20
-- Find the total number of players, enemies, and weapons
SELECT 
    (SELECT COUNT(*) FROM Player) AS TotalPlayers,
    (SELECT COUNT(*) FROM Enemy) AS TotalEnemies,
    (SELECT COUNT(*) FROM Weapon) AS TotalWeapons;
