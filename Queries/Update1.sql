.headers on

-- Update #1:
-- Update all enemies in Orc clan so that their Entity attack stat is raised by 20

UPDATE Entity
SET Attack = Attack + 20
WHERE EntityID IN (
    SELECT E.EntityID
    FROM Enemy E
    JOIN EnemyBelongs EB ON E.EntityID = EB.EntityID
    JOIN Clan C ON EB.ClanName = C.ClanName
    WHERE C.ClanName = 'Orc'
);