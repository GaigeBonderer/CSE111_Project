.headers on

-- Insert
-- Insert a player name "HackSawNani" and whos gender is Female. Make her Entity ID 10001 her type P Her Attack 200, Defense 200,
-- Level 100, Speed 200,  current HP 1000, and total hp 1000. Assign her to the KnightsOfTheBloodOathOrder guild making sure to include her in PlayerBelongs table.
-- Assign her a mystic weapon in the Equiped table. Assign her three mystic weapons in her inventory.

-- Insert 1/5: Insert into the Entity table
INSERT INTO Entity (EntityID, Type, Attack, Defense, Level, Speed, CurrentHP, TotalHP)
VALUES (10001, 'P', 200, 200, 100, 200, 1000, 1000);

-- Insert 2/5: Insert into the Player table
INSERT INTO Player (EntityID, Gender, Username)
VALUES (10001, 'F', 'HackSawNani');

-- Insert 3/5: Insert into the PlayerBelongs table under KnightsOfTheBloodOathOrder guild
INSERT INTO PlayerBelongs (EntityID, GuildName)
VALUES (10001, 'KnightsOfTheBloodOathOrder');

-- Insert 4/5: Assign her a mystic weapon in the Equipped table
INSERT INTO Equipped (EntityID, WeaponID)
SELECT 10001, WeaponID
FROM Weapon
WHERE Type = 'Mystic'
AND WeaponID NOT IN (SELECT WeaponID FROM Equipped WHERE EntityID = 10001)
ORDER BY RANDOM()
LIMIT 1;

-- Insert 5/5: Assign her 3 other mystic weapons in the Inventory table
INSERT INTO Inventory (EntityID, WeaponID)
SELECT 10001, WeaponID
FROM Weapon
WHERE Type = 'Mystic'
AND WeaponID NOT IN (SELECT WeaponID FROM Equipped WHERE EntityID = 10001)
AND WeaponID NOT IN (SELECT WeaponID FROM Inventory WHERE EntityID = 10001)
ORDER BY RANDOM()
LIMIT 3;


-- Query #22: Select HackSawNani's player data, entity data, equipped data, and inventory data

-- Query #22 1/3:
-- Print Entity data for HackSawNani
SELECT 
    p.EntityID,
    p.Username,
    p.Gender,
    e.Type,
    e.Attack,
    e.Defense,
    e.Level,
    e.Speed,
    e.CurrentHP,
    e.TotalHP
FROM 
    Player AS p
JOIN 
    Entity AS e ON p.EntityID = e.EntityID
WHERE 
    p.Username = 'HackSawNani';

-- Query #22 2/3:
-- Print Equipped weapons for HackSawNani
SELECT 
    eq.EntityID,
    w.WeaponID,
    w.Name AS WeaponName,
    w.Type AS WeaponType,
    w.Rank,
    w.Damage,
    w.ATKSpeed,
    w.Range
FROM 
    Equipped AS eq
JOIN 
    Weapon AS w ON eq.WeaponID = w.WeaponID
WHERE 
    eq.EntityID = 10001;

-- Query #22 3/3: 
-- Print Inventory data for HackSawNani
SELECT 
    inv.EntityID,
    w.WeaponID,
    w.Name AS WeaponName,
    w.Type AS WeaponType,
    w.Rank,
    w.Damage,
    w.ATKSpeed,
    w.Range
FROM 
    Inventory AS inv
JOIN 
    Weapon AS w ON inv.WeaponID = w.WeaponID
WHERE 
    inv.EntityID = 10001;