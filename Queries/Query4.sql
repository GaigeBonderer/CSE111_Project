--PRAGMA table_info(Enemy);

-- Query #4
-- We want to a group of strong players that are capable of fighting an enemy boss.
-- Find 5 strong players that are the same level as the enemy character, Troll.

SELECT 
    Player.EntityID, Player.Username, Entity.Level
FROM 
    Player
JOIN 
    Entity ON Player.EntityID = Entity.EntityID
WHERE Entity.Level = (
    SELECT 
        Entity.Level
    FROM 
        Enemy
    JOIN 
        Entity ON Enemy.EntityID = Entity.EntityID
    WHERE 
        Enemy.Name = ' Troll'
)
LIMIT 5;

-- SELECT Entity.Level
-- FROM Enemy
-- JOIN Entity ON Enemy.EntityID = Entity.EntityID
-- WHERE Enemy.Name = 'Dark Dragon';