
-- Query #2:
-- Which player characters are Warriors or Hunters?
SELECT * 
FROM Player
WHERE Username LIKE '%Warrior%' OR Username LIKE '%Hunter%';