
-- Query #5
-- show me the top ten players with the highest stat total that have a mystic weapon equipped 


-- SELECT p.Username, 
--        (e.Attack + e.Defense + e.Speed + e.Level + e.CurrentHP + e.TotalHP) AS StatTotal,
--        w.Name AS WeaponName
-- FROM 
--     Player p
-- JOIN 
--     Entity e ON p.EntityID = e.EntityID
-- JOIN 
--     Equipped eq ON e.EntityID = eq.EntityID
-- JOIN 
--     Weapon w ON eq.WeaponID = w.WeaponID
-- WHERE 
--     w.Name LIKE '%Mystic%'
-- ORDER BY 
--     StatTotal DESC
-- LIMIT 10;
