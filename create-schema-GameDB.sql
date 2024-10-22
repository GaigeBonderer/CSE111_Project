CREATE TABLE Entity (
    EntityID INT AUTO_INCREMENT PRIMARY KEY,
    Attack INT NOT NULL,
    Defense INT NOT NULL,
    Level INT NOT NULL,
    Speed INT NOT NULL,
    CurrentHP INT NOT NULL,
    TotalHP INT NOT NULL
);

CREATE TABLE Player (
    EntityID INT PRIMARY KEY,
    Gender CHAR(1) NOT NULL,
    Username VARCHAR(25) NOT NULL,
    FOREIGN KEY (EntityID) REFERENCES Entity(EntityID)
);

CREATE TABLE Enemy (
    EntityID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    IsBoss BOOLEAN NOT NULL,
    FOREIGN KEY (EntityID) REFERENCES Entity(EntityID)
);

CREATE TABLE Weapon (
    WeaponID INT AUTO_INCREMENT PRIMARY KEY,
    Description VARCHAR(100),
    Rank INT NOT NULL,
    Type VARCHAR(25) NOT NULL,
    Name VARCHAR(50) NOT NULL,
    SpecialATR VARCHAR(50),
    Damage INT NOT NULL,
    ATKSpeed INT NOT NULL,
    Range INT NOT NULL
);

CREATE TABLE Guild (
    GuildName VARCHAR(50) PRIMARY KEY,
    GuildBonus INT NOT NULL,
    TotalPlayers INT NOT NULL
);

CREATE TABLE Clan (
    ClanName VARCHAR(50) PRIMARY KEY,
    ClanBonus INT NOT NULL,
    BossName VARCHAR(50) NOT NULL
);

CREATE TABLE Inventory (
    EntityID INT NOT NULL,
    WeaponID INT NOT NULL,
    PRIMARY KEY (EntityID, WeaponID),
    FOREIGN KEY (EntityID) REFERENCES Player(EntityID),
    FOREIGN KEY (WeaponID) REFERENCES Weapon(WeaponID)
);

CREATE TABLE Equipped (
    EntityID INT NOT NULL,
    WeaponID INT NOT NULL,
    PRIMARY KEY (EntityID, WeaponID),
    FOREIGN KEY (EntityID) REFERENCES Entity(EntityID),
    FOREIGN KEY (WeaponID) REFERENCES Weapon(WeaponID)
);

CREATE TABLE CanDrop (
    WeaponID INT NOT NULL,
    EntityID INT NOT NULL,
    PRIMARY KEY (WeaponID, EntityID),
    FOREIGN KEY (WeaponID) REFERENCES Weapon(WeaponID),
    FOREIGN KEY (EntityID) REFERENCES Enemy(EntityID)
);

CREATE TABLE PlayerBelongs (
    EntityID INT NOT NULL,
    GuildName VARCHAR(50) NOT NULL,
    PRIMARY KEY (EntityID, GuildName),
    FOREIGN KEY (EntityID) REFERENCES Player(EntityID),
    FOREIGN KEY (GuildName) REFERENCES Guild(GuildName)
);

CREATE TABLE EnemyBelongs (
    EntityID INT NOT NULL,
    ClanName VARCHAR(50) NOT NULL,
    PRIMARY KEY (EntityID, ClanName),
    FOREIGN KEY (EntityID) REFERENCES Enemy(EntityID),
    FOREIGN KEY (ClanName) REFERENCES Clan(ClanName)
);

