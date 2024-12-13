import sqlite3

# Function to establish a connection to the database
def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

# Function to create tables in the database
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Entity table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Entity (
            EntityID INTEGER PRIMARY KEY AUTOINCREMENT,
            Type CHAR(1) NOT NULL,
            Attack INT NOT NULL,
            Defense INT NOT NULL,
            Level INT NOT NULL,
            Speed INT NOT NULL,
            CurrentHP INT NOT NULL,
            TotalHP INT NOT NULL
        )
    """)
    
    # Create Player tavble
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Player (
            EntityID INTEGER PRIMARY KEY,
            Gender CHAR(1) NOT NULL,
            Username VARCHAR(25) NOT NULL,
            FOREIGN KEY (EntityID) REFERENCES Entity(EntityID)
        )
    """)

    # Create Enemy table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Enemy (
            EntityID INTEGER PRIMARY KEY,
            Name VARCHAR(50) NOT NULL,
            IsBoss BOOLEAN NOT NULL,
            FOREIGN KEY (EntityID) REFERENCES Entity(EntityID)
        )
    """)

    # Create Weapon table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Weapon (
            WeaponID INTEGER PRIMARY KEY AUTOINCREMENT,
            Description VARCHAR(100),
            Rank VARCHAR(25) NOT NULL,
            Type VARCHAR(25) NOT NULL,
            Name VARCHAR(50) NOT NULL,
            SpecialATR VARCHAR(50),
            Damage INT NOT NULL,
            ATKSpeed INT NOT NULL,
            Range INT NOT NULL
        )
    """)

    # Create Guild table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Guild (
            GuildName VARCHAR(50) PRIMARY KEY,
            GuildBonus VARCHAR(50) NOT NULL,
            TotalPlayers INT NOT NULL
        )
    """)

    # Create Clan table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clan (
            ClanName VARCHAR(50) PRIMARY KEY,
            ClanBonus VARCHAR(50) NOT NULL,
            BossName VARCHAR(50) NOT NULL
        )
    """)

    # Create Inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Inventory (
            EntityID INT NOT NULL,
            WeaponID INT NOT NULL,
            PRIMARY KEY (EntityID, WeaponID),
            FOREIGN KEY (EntityID) REFERENCES Player(EntityID),
            FOREIGN KEY (WeaponID) REFERENCES Weapon(WeaponID)
        )
    """)

    # Create Equipped table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equipped (
            EntityID INT NOT NULL,
            WeaponID INT NOT NULL,
            PRIMARY KEY (EntityID, WeaponID),
            FOREIGN KEY (EntityID) REFERENCES Entity(EntityID),
            FOREIGN KEY (WeaponID) REFERENCES Weapon(WeaponID)
        )
    """)

    # Create CanDrop table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CanDrop (
            WeaponID INT NOT NULL,
            EntityID INT NOT NULL,
            PRIMARY KEY (WeaponID, EntityID),
            FOREIGN KEY (WeaponID) REFERENCES Weapon(WeaponID),
            FOREIGN KEY (EntityID) REFERENCES Enemy(EntityID)
        )
    """)

    # Create PlayerBelongs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PlayerBelongs (
            EntityID INT NOT NULL,
            GuildName VARCHAR(50) NOT NULL,
            PRIMARY KEY (EntityID, GuildName),
            FOREIGN KEY (EntityID) REFERENCES Player(EntityID),
            FOREIGN KEY (GuildName) REFERENCES Guild(GuildName)
        )
    """)

    # Create EnemyBelongs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EnemyBelongs (
            EntityID INT NOT NULL,
            ClanName VARCHAR(50) NOT NULL,
            PRIMARY KEY (EntityID, ClanName),
            FOREIGN KEY (EntityID) REFERENCES Enemy(EntityID),
            FOREIGN KEY (ClanName) REFERENCES Clan(ClanName)
        )
    """)

    conn.commit()  # Commit all changes to the database
    conn.close()   # Close the database connection
    print("All tables created successfully if they did not exist.")