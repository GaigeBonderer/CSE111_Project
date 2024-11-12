.headers on

-- Query #18  

-- count and list all the number of weapons and their types
SELECT Rank, COUNT(*) AS WeaponCount
FROM Weapon
GROUP BY Rank
ORDER BY WeaponCount DESC;