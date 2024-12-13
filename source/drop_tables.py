import sqlite3

# Function to establish a connection to the SQLite database
def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

# Function to drop the Player table
def drop_player():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Player")  # Drop table if it exists
    conn.commit()
    conn.close()
    print("Dropped Player table.")

# Function to drop the Entity table
def drop_entity():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Entity")
    conn.commit()
    conn.close()
    print("Dropped Entity table.")

# Function to drop the Enemy table
def drop_enemy():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Enemy")
    conn.commit()
    conn.close()
    print("Dropped Enemy table.")

# Function to drop the Weapon table
def drop_weapon():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Weapon")
    conn.commit()
    conn.close()
    print("Dropped Weapon table.")

# Function to drop the Guild table
def drop_guild():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Guild")
    conn.commit()
    conn.close()
    print("Dropped Guild table.")

# Function to drop the Clan table
def drop_clan():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Clan")
    conn.commit()
    conn.close()
    print("Dropped Clan table.")

# Function to drop the Inventory table
def drop_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Inventory")
    conn.commit()
    conn.close()
    print("Dropped Inventory table.")

# Function to drop the Equipped table
def drop_equipped():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Equipped")
    conn.commit()
    conn.close()
    print("Dropped Equipped table.")

# Function to drop the CanDrop table
def drop_can_drop():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS CanDrop")
    conn.commit()
    conn.close()
    print("Dropped CanDrop table.")

# Function to drop the PlayerBelongs table
def drop_player_belongs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS PlayerBelongs")
    conn.commit()
    conn.close()
    print("Dropped PlayerBelongs table.")

# Function to drop the EnemyBelongs table
def drop_enemy_belongs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS EnemyBelongs")
    conn.commit()
    conn.close()
    print("Dropped EnemyBelongs table.")

# Function to drop all tables in the database
def drop_all():
    drop_player()           # Drop Player table
    drop_entity()           # Drop Entity table
    drop_enemy()            # Drop Enemy table
    drop_weapon()           # Drop Weapon table
    drop_guild()            # Drop Guild table
    drop_clan()             # Drop Clan table
    drop_inventory()        # Drop Inventory table
    drop_equipped()         # Drop Equipped table
    drop_can_drop()         # Drop CanDrop table
    drop_player_belongs()   # Drop PlayerBelongs table
    drop_enemy_belongs()    # Drop EnemyBelongs table
    print("All tables dropped.")  # Confirm all tables were dropped
