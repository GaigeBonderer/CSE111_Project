.headers on
-- Query #12
--Which weapon types have the weakest stats in terms of attack and attack speed?

SELECT Type, AVG(Damage) AS AvgDamage, AVG(ATKSpeed) AS AvgATKSpeed
FROM Weapon
GROUP BY Type
ORDER BY AvgDamage ASC, AvgATKSpeed ASC
LIMIT 5;
