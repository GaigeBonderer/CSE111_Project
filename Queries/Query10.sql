.headers on
-- Query #10: 
-- What's the most common weapon rank used by both enemies and players? 
SELECT 
    w.Rank, COUNT(w.Rank) AS RankCount
FROM 
    Weapon w
JOIN 
    Equipped e ON w.WeaponID = e.WeaponID
JOIN 
    Entity en ON e.EntityID = en.EntityID
WHERE 
    en.Type IN ('P', 'E')  -- 'P' denotes players and 'E' denotes enemies
GROUP BY 
    w.Rank
ORDER BY 
    RankCount DESC
LIMIT 1;
