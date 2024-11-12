.headers on 
-- Query #11
-- Find the top five weapons with the highest stat total and the entities that weild them

SELECT 
    w.Name AS WeaponName,
    (w.Damage + w.ATKSpeed + w.Range) AS TotalStats,
    e.EntityID,
    e.Type,
    e.Attack,
    e.Defense,
    e.Level,
    e.Speed
FROM 
    Weapon AS w
JOIN 
    Equipped AS eq ON w.WeaponID = eq.WeaponID
JOIN 
    Entity AS e ON eq.EntityID = e.EntityID
ORDER BY 
    TotalStats DESC
LIMIT 5;
