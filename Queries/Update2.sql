.headers on

-- Update #2:
-- Update all players with "Assasin" in their name over level 50 to have their Entity speed stat raised by 20

UPDATE Entity
SET Speed = Speed + 20
WHERE EntityID IN (
    SELECT P.EntityID
    FROM Player P
    JOIN Entity E ON P.EntityID = E.EntityID
    WHERE E.Level > 50 AND P.Username LIKE '%Assassin%'
);