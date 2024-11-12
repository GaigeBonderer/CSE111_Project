.headers on

-- Query #19
--find a weapon with the furthest range

SELECT *
FROM Weapon
WHERE Range = (SELECT MAX(Range) FROM Weapon);
