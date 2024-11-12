.headers on
-- Query 16
-- What's the percentage of all players and enemies who possess a mystic (rank) weapon? 
WITH MysticEntities AS (
    SELECT EntityID
    FROM Inventory i
    JOIN Weapon w ON i.WeaponID = w.WeaponID
    WHERE w.Rank = 'Mystic'
    
    UNION
    
    SELECT EntityID
    FROM CanDrop c
    JOIN Weapon w ON c.WeaponID = w.WeaponID
    WHERE w.Rank = 'Mystic'
),
TotalEntities AS (
    SELECT COUNT(*) AS TotalPlayers FROM Player
    UNION ALL
    SELECT COUNT(*) AS TotalEnemies FROM Enemy
)

SELECT 
    (COUNT(DISTINCT MysticEntities.EntityID) * 100.0) / 
    (SELECT SUM(TotalPlayers) FROM TotalEntities) AS MysticWeaponPercentage
FROM MysticEntities;
