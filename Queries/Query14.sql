.headers on

-- Query #14
--Which guilds players have legendary weapons equipped the most? 

SELECT g.GuildName, COUNT(*) AS LegendaryWeaponCount
FROM Guild AS g
JOIN PlayerBelongs AS pb ON g.GuildName = pb.GuildName
JOIN Equipped AS e ON pb.EntityID = e.EntityID
JOIN Weapon AS w ON e.WeaponID = w.WeaponID
WHERE w.Rank = 'Legendary'
GROUP BY g.GuildName
ORDER BY LegendaryWeaponCount DESC;
