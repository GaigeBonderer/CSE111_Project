import sqlite3

def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

def drop_player():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Player")
    conn.commit()
    conn.close()
    print("Dropped Player table.")

def drop_entity():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Entity")
    conn.commit()
    conn.close()
    print("Dropped Entity table.")

def drop_enemy():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Enemy")
    conn.commit()
    conn.close()
    print("Dropped Enemy table.")

def drop_weapon():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Weapon")
    conn.commit()
    conn.close()
    print("Dropped Weapon table.")

def drop_guild():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Guild")
    conn.commit()
    conn.close()
    print("Dropped Guild table.")

def drop_clan():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Clan")
    conn.commit()
    conn.close()
    print("Dropped Clan table.")

def drop_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Inventory")
    conn.commit()
    conn.close()
    print("Dropped Inventory table.")

def drop_equipped():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Equipped")
    conn.commit()
    conn.close()
    print("Dropped Equipped table.")

def drop_can_drop():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS CanDrop")
    conn.commit()
    conn.close()
    print("Dropped CanDrop table.")

def drop_player_belongs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS PlayerBelongs")
    conn.commit()
    conn.close()
    print("Dropped PlayerBelongs table.")

def drop_enemy_belongs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS EnemyBelongs")
    conn.commit()
    conn.close()
    print("Dropped EnemyBelongs table.")

def drop_all():
    drop_player()
    drop_entity()
    drop_enemy()
    drop_weapon()
    drop_guild()
    drop_clan()
    drop_inventory()
    drop_equipped()
    drop_can_drop()
    drop_player_belongs()
    drop_enemy_belongs()
    print("All tables dropped.")