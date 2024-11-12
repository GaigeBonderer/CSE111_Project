.headers on

-- PRAGMA table_info(Player);

------------------------------------------------------------------------------------------------------------------
-- Query #1:
-- Which player characters have a level of 50 or greater and are part of the MysticPhoenixHunters?

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
    AND Guild.GuildName = 'MysticPhoenixHunters'; 
