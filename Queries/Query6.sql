.headers on
-- Query #6:
-- Find the strongest enemy characters (lvl 95) that have the clan bonus to life steal
SELECT 
    e.Name AS EnemyName, en.Level, en.Attack, en.Defense, en.Speed, c.ClanBonus
FROM 
    Enemy e
JOIN 
    Entity en ON e.EntityID = en.EntityID
JOIN 
    EnemyBelongs eb ON e.EntityID = eb.EntityID
JOIN 
    Clan c ON eb.ClanName = c.ClanName
WHERE 
    en.Level = 95 AND c.ClanBonus LIKE '%life steal%';
