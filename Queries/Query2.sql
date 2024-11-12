
-- Query #2:
-- Which player characters are Warriors or Hunters that use a dagger for a weapon?

--old query: 
-- SELECT * 
-- FROM Player
-- WHERE Username LIKE '%Warrior%' OR Username LIKE '%Hunter%';


--new query to test: 
-- SELECT p.*
-- FROM Player p
-- JOIN Equipped e ON p.EntityID = e.EntityID
-- JOIN Weapon w ON e.WeaponID = w.WeaponID
-- WHERE (p.Username LIKE '%Warrior%' OR p.Username LIKE '%Hunter%')
--   AND w.Type = 'Dagger';

-- alternative
-- SELECT p.*
-- FROM Player p
-- JOIN Equipped e ON p.EntityID = e.EntityID
-- JOIN Weapon w ON e.WeaponID = w.WeaponID
-- WHERE (p.Username LIKE '%Warrior%' OR p.Username LIKE '%Hunter%')
--   AND LOWER(w.Type) = 'Dagger';

-- checks that daggers is in the DB
-- SELECT * FROM Weapon
-- WHERE LOWER(Type) = 'dagger';
