
-- Query #5
--What's the minimum amount of players that are female and a mage? 

SELECT COUNT(*) AS FemaleMageCount
FROM Player
WHERE Gender = 'F' AND Username LIKE '%Mage%';
