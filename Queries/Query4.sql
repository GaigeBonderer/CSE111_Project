--PRAGMA table_info(Enemy);

-- Query #4
-- We want to a group of strong players that are capable of fighting an enemy boss.
-- Find 5 strong players that are the same level as the enemy character, (insert enemy name here)

-- SELECT Player.EntityID, Player.Username, Entity.Level
-- FROM Player
-- JOIN Entity ON Player.EntityID = Entity.EntityID
-- WHERE Entity.Level = (
--     SELECT Level
--     FROM Enemy
--     JOIN Entity ON Enemy.EntityID = Entity.EntityID
--     WHERE Enemy.EntityID = ?
-- )
-- LIMIT 5;
