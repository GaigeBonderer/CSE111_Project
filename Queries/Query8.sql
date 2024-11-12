.headers on
-- Query #8
-- How many Evil and Malicious enemies are not from the Demon or Ghoul clan? 
SELECT 
    COUNT(*) AS EvilMaliciousEnemyCount
FROM 
    Enemy
JOIN 
    EnemyBelongs ON Enemy.EntityID = EnemyBelongs.EntityID
WHERE 
    (Enemy.Name LIKE '%Evil%' OR Enemy.Name LIKE '%Malicious%')
    AND EnemyBelongs.ClanName NOT IN ('Demon', 'Ghoul');
