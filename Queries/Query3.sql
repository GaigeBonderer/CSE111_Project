
-- Query #3:
-- Find 10 players that have the lowest hp
SELECT Player.EntityID, Player.Username, Player.Gender, Entity.CurrentHP, Entity.TotalHP
FROM Player
JOIN Entity ON Player.EntityID = Entity.EntityID
ORDER BY Entity.CurrentHP ASC
LIMIT 10;