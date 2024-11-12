.headers on
-- Query #13
-- What percentage of legendary weapons have a special attribute that is not "None"? 

SELECT 
    (CAST(SUM(CASE WHEN SpecialATR IS NOT NULL AND SpecialATR != 'None' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 AS PercentageWithSpecialAttribute
FROM 
    Weapon
WHERE 
    Rank = 'Legendary';
