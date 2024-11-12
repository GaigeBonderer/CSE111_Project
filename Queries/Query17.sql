.headers on
--Query #17
-- Count and list the enemy descriptors in alphabetical order

SELECT 
    SUBSTR(Name, 1, INSTR(Name, ' ') - 1) AS Descriptor,
    COUNT(*) AS Count
FROM 
    Enemy
GROUP BY 
    Descriptor
ORDER BY 
    Descriptor ASC;
