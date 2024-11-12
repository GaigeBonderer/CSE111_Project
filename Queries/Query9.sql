.headers on
-- Query #9
-- For the enemies in the Warlock clan, 
-- find the largest enemy attack that's smaller than the average attack among all enemies in that clan

WITH WarlockClanStats AS (
    SELECT en.Attack
    FROM Enemy e
    JOIN Entity en ON e.EntityID = en.EntityID
    JOIN EnemyBelongs eb ON e.EntityID = eb.EntityID
    WHERE eb.ClanName = 'Warlock'
),
AverageAttack AS (
    SELECT AVG(Attack) AS AvgAttack
    FROM WarlockClanStats
)

SELECT MAX(Attack) AS LargestAttackBelowAverage
FROM WarlockClanStats
WHERE Attack < (SELECT AvgAttack FROM AverageAttack);
