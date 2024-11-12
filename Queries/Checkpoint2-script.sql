.headers on 
-- Query #1:
-- Which player characters have a level of 50 or greater and are part of the AncientLionGuild?

SELECT 
    Player.EntityID, Player.Username, Player.Gender, Entity.Level
FROM 
    Player
JOIN 
    Entity ON Player.EntityID = Entity.EntityID
JOIN 
    PlayerBelongs ON Player.EntityID = PlayerBelongs.EntityID
JOIN 
    Guild ON PlayerBelongs.GuildName = Guild.GuildName
WHERE 
    Entity.Level >= 50 
    AND Guild.GuildName = 'AncientLionGuild'; 

-- Query #2:
-- Which player characters are Warriors or Hunters that use a dagger for a weapon?

SELECT p.*
FROM Player p
JOIN Equipped e ON p.EntityID = e.EntityID
JOIN Weapon w ON e.WeaponID = w.WeaponID
WHERE (p.Username LIKE '%Warrior%' OR p.Username LIKE '%Hunter%')
  AND w.Type = 'Dagger';

-- Query #3:
-- Find 10 Assasin players that have the lowest current hp

SELECT 
    Player.EntityID, Player.Username, Player.Gender, Entity.CurrentHP, Entity.TotalHP
FROM 
    Player
JOIN 
    Entity ON Player.EntityID = Entity.EntityID
WHERE 
    Player.Username LIKE '%Assassin%'
ORDER BY Entity.CurrentHP ASC
LIMIT 10;

-- Query #4
-- We want to a group of strong players that are capable of fighting an enemy boss.
-- Find 5 strong players that are the same level as the enemy character, Troll.

SELECT 
    Player.EntityID, Player.Username, Entity.Level
FROM 
    Player
JOIN 
    Entity ON Player.EntityID = Entity.EntityID
WHERE Entity.Level = (
    SELECT 
        Entity.Level
    FROM 
        Enemy
    JOIN 
        Entity ON Enemy.EntityID = Entity.EntityID
    WHERE 
        Enemy.Name = ' Troll'
)
LIMIT 5;

-- Query #5
-- Find the top ten players with the highest stat total that have a mystic weapon equipped 


SELECT p.Username, 
       (e.Attack + e.Defense + e.Speed + e.Level + e.CurrentHP + e.TotalHP) AS StatTotal,
       w.Name AS WeaponName
FROM 
    Player p
JOIN 
    Entity e ON p.EntityID = e.EntityID
JOIN 
    Equipped eq ON e.EntityID = eq.EntityID
JOIN 
    Weapon w ON eq.WeaponID = w.WeaponID
WHERE 
    w.Name LIKE '%Mystic%'
ORDER BY 
    StatTotal DESC
LIMIT 10;

-- Query #6:
-- Find the strongest enemy characters (lvl 95) that have the clan bonus to life steal
SELECT 
    e.Name AS EnemyName, en.Level, en.Attack, en.Defense, en.Speed, c.ClanBonus
FROM 
    Enemy e
JOIN 
    Entity en ON e.EntityID = en.EntityID
JOIN 
    EnemyBelongs eb ON e.EntityID = eb.EntityID
JOIN 
    Clan c ON eb.ClanName = c.ClanName
WHERE 
    en.Level = 95 AND c.ClanBonus LIKE '%life steal%';

-- Query #7:
-- Which clan has the maximum amount of enemies with a high level (90 or higher)?

SELECT 
    ClanName, COUNT(*) AS HighLevelEnemyCount
FROM 
    Enemy
JOIN 
    EnemyBelongs ON Enemy.EntityID = EnemyBelongs.EntityID
JOIN 
    Entity ON Enemy.EntityID = Entity.EntityID
WHERE 
    Entity.Level >= 90
GROUP BY 
    ClanName
ORDER BY 
    HighLevelEnemyCount DESC
LIMIT 1;


-- Query #8
-- How many Evil and Malicious enemies are not from the Demon or Ghoul clan? 
SELECT 
    COUNT(*) AS EvilMaliciousEnemyCount
FROM 
    Enemy
JOIN 
    EnemyBelongs ON Enemy.EntityID = EnemyBelongs.EntityID
WHERE 
    (Enemy.Name LIKE '%Evil%' OR Enemy.Name LIKE '%Malicious%')
    AND EnemyBelongs.ClanName NOT IN ('Demon', 'Ghoul');


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


-- Query #10: 
-- What's the most common weapon rank used by both enemies and players? 
SELECT 
    w.Rank, COUNT(w.Rank) AS RankCount
FROM 
    Weapon w
JOIN 
    Equipped e ON w.WeaponID = e.WeaponID
JOIN 
    Entity en ON e.EntityID = en.EntityID
WHERE 
    en.Type IN ('P', 'E')  -- 'P' denotes players and 'E' denotes enemies
GROUP BY 
    w.Rank
ORDER BY 
    RankCount DESC
LIMIT 1;

-- Query #11
-- Find the top five weapons with the highest stat total and the entities that weild them

SELECT 
    w.Name AS WeaponName,
    (w.Damage + w.ATKSpeed + w.Range) AS TotalStats,
    e.EntityID,
    e.Type,
    e.Attack,
    e.Defense,
    e.Level,
    e.Speed
FROM 
    Weapon AS w
JOIN 
    Equipped AS eq ON w.WeaponID = eq.WeaponID
JOIN 
    Entity AS e ON eq.EntityID = e.EntityID
ORDER BY 
    TotalStats DESC
LIMIT 5;


-- Query #12
--Which weapon types have the weakest stats in terms of attack and attack speed?

SELECT Type, AVG(Damage) AS AvgDamage, AVG(ATKSpeed) AS AvgATKSpeed
FROM Weapon
GROUP BY Type
ORDER BY AvgDamage ASC, AvgATKSpeed ASC
LIMIT 5;


-- Query #13
-- What percentage of legendary weapons have a special attribute that is not "None"? 

SELECT 
    (CAST(SUM(CASE WHEN SpecialATR IS NOT NULL AND SpecialATR != 'None' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 AS PercentageWithSpecialAttribute
FROM 
    Weapon
WHERE 
    Rank = 'Legendary';

-- Query #14
--Which guilds players have legendary weapons equipped the most? 

SELECT g.GuildName, COUNT(*) AS LegendaryWeaponCount
FROM Guild AS g
JOIN PlayerBelongs AS pb ON g.GuildName = pb.GuildName
JOIN Equipped AS e ON pb.EntityID = e.EntityID
JOIN Weapon AS w ON e.WeaponID = w.WeaponID
WHERE w.Rank = 'Legendary'
GROUP BY g.GuildName
ORDER BY LegendaryWeaponCount DESC;

-- Query #15
--Which clans enemies have Epic weapons equipped the most? 
SELECT c.ClanName, COUNT(*) AS LegendaryWeaponCount
FROM Clan c
JOIN EnemyBelongs eb ON c.ClanName = eb.ClanName
JOIN Enemy e ON eb.EntityID = e.EntityID
JOIN Equipped eq ON e.EntityID = eq.EntityID
JOIN Weapon w ON eq.WeaponID = w.WeaponID
WHERE w.Rank = 'Epic'
GROUP BY c.ClanName
ORDER BY LegendaryWeaponCount DESC;


-- Query #16
-- What's the percentage of all players and enemies who possess a mystic (rank) weapon? 
WITH MysticEntities AS (
    SELECT EntityID
    FROM Inventory i
    JOIN Weapon w ON i.WeaponID = w.WeaponID
    WHERE w.Rank = 'Mystic'
    
    UNION
    
    SELECT EntityID
    FROM CanDrop c
    JOIN Weapon w ON c.WeaponID = w.WeaponID
    WHERE w.Rank = 'Mystic'
),
TotalEntities AS (
    SELECT COUNT(*) AS TotalPlayers FROM Player
    UNION ALL
    SELECT COUNT(*) AS TotalEnemies FROM Enemy
)

SELECT 
    (COUNT(DISTINCT MysticEntities.EntityID) * 100.0) / 
    (SELECT SUM(TotalPlayers) FROM TotalEntities) AS MysticWeaponPercentage
FROM MysticEntities;


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


-- Query #18  
-- Count and list all the number of weapons and their types
SELECT Rank, COUNT(*) AS WeaponCount
FROM Weapon
GROUP BY Rank
ORDER BY WeaponCount DESC;

-- Query #19
-- Find a weapon with the furthest range

SELECT *
FROM Weapon
WHERE Range = (SELECT MAX(Range) FROM Weapon);

-- Query #20
-- Find the total number of players, enemies, and weapons
SELECT 
    (SELECT COUNT(*) FROM Player) AS TotalPlayers,
    (SELECT COUNT(*) FROM Enemy) AS TotalEnemies,
    (SELECT COUNT(*) FROM Weapon) AS TotalWeapons;
