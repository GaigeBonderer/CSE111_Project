
-- Query #3:
-- Find 10 Assasin players that have the lowest current hp

SELECT 
    Player.EntityID, Player.Username, Player.Gender, Entity.CurrentHP, Entity.TotalHP
FROM 
    Player
JOIN 
    Entity ON Player.EntityID = Entity.EntityID
WHERE 
    Player.Username LIKE '%Assassin%'
ORDER BY Entity.CurrentHP ASC
LIMIT 10;
