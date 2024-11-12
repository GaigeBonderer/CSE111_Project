.headers on

-- Deletion
-- Delete All FalsGod Enemies that are below level 15,
--  ensure that their entrie(s) in EnemyBelongs, Equiped,
--  and CanDrop are deleted as well

-- Deletion 1/5: Delete from EnemyBelongs
DELETE FROM EnemyBelongs
WHERE EntityID IN (
    SELECT e.EntityID
    FROM Enemy e
    JOIN Entity ent ON e.EntityID = ent.EntityID
    WHERE e.Name LIKE '%FalseGod%' AND ent.Level < 15
);

-- Deletion 2/5: Delete from Equipped
DELETE FROM Equipped
WHERE EntityID IN (
    SELECT e.EntityID
    FROM Enemy e
    JOIN Entity ent ON e.EntityID = ent.EntityID
    WHERE e.Name LIKE '%FalseGod%' AND ent.Level < 15
);

-- Deletion 3/5: Delete from CanDrop
DELETE FROM CanDrop
WHERE EntityID IN (
    SELECT e.EntityID
    FROM Enemy e
    JOIN Entity ent ON e.EntityID = ent.EntityID
    WHERE e.Name LIKE '%FalseGod%' AND ent.Level < 15
);

-- Deletion 4/5: Delete the Enemy
DELETE FROM Enemy
WHERE EntityID IN (
    SELECT e.EntityID
    FROM Enemy e
    JOIN Entity ent ON e.EntityID = ent.EntityID
    WHERE e.Name LIKE '%FalseGod%' AND ent.Level < 15
);

-- Deletion 5/5: Delete from the Entity table where Name is 'FalsGod' and Level is below 15
DELETE FROM Entity
WHERE EntityID IN (
    SELECT e.EntityID
    FROM Enemy e
    JOIN Entity ent ON e.EntityID = ent.EntityID
    WHERE e.Name LIKE '%FalseGod%' AND ent.Level < 15
);

-- Query #21
-- Proof of Deletion: Select all FalseGod Enemies below Level 15

SELECT e.EntityID, e.Name, ent.Level
FROM Enemy e
JOIN Entity ent ON e.EntityID = ent.EntityID
WHERE e.Name LIKE '%FalseGod%' AND ent.Level < 20;