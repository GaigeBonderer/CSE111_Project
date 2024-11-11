--5 player queries 
--5 weapon queries
--5 enemy queries 
--5 random

-- PRAGMA table_info(Player);

------------------------------------------------------------------------------------------------------------------
-- Query #1:
-- Which player characters have a level of 50 or greater?
SELECT 
    Player.EntityID, Player.Username, Player.Gender, Entity.Level
FROM 
    Player
JOIN Entity ON Player.EntityID = Entity.EntityID
WHERE 
    Entity.Level >= 50;

