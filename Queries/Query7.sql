
-- Query #7:
-- Which clan has the maximum amount of enemies with a high level (90 or higher)?

SELECT 
    ClanName, COUNT(*) AS HighLevelEnemyCount
FROM 
    Enemy
JOIN 
    EnemyBelongs ON Enemy.EntityID = EnemyBelongs.EntityID
JOIN 
    Entity ON Enemy.EntityID = Entity.EntityID
WHERE 
    Entity.Level >= 90
GROUP BY 
    ClanName
ORDER BY 
    HighLevelEnemyCount DESC
LIMIT 1;

