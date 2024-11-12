.headers on

-- Query #15
-- --Which clans enemies have Epic weapons equipped the most? 
SELECT c.ClanName, COUNT(*) AS LegendaryWeaponCount
FROM Clan c
JOIN EnemyBelongs eb ON c.ClanName = eb.ClanName
JOIN Enemy e ON eb.EntityID = e.EntityID
JOIN Equipped eq ON e.EntityID = eq.EntityID
JOIN Weapon w ON eq.WeaponID = w.WeaponID
WHERE w.Rank = 'Epic'
GROUP BY c.ClanName
ORDER BY LegendaryWeaponCount DESC;
