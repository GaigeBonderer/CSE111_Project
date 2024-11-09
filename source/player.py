import sqlite3
import random
from db_init import create_tables # CREATE handled in db_init.py


#For username Generation

descriptor = ["Swift", "Brave", "Clever", "Mystic", "Bold",
               "Ancient", "Fierce", "Mighty", "Silent", "Radiant",
               "Hairy", "Evil", "Stealthy", "Big", "Strong",
               "Courageous", "Scandalous", "Noob", "Pro", "Stinky",]

main_name = ["Warrior", "Mage", "Hunter", "Knight", "Rogue",
          "Druid", "Assassin", "Paladin", "Sorcerer", "Guardian",
          "69_", "Dragon", "Ganker", "Slayer", "Skull",
          "Tony", "Savage", "****", "Bender", "Vegetable",]



def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

# ////////////////////////////////////////////////////////////////////////////////////////

def generate_unique_username(existing_usernames):
    base_username = f"{random.choice(descriptor)}{random.choice(main_name)}"
    
    # add number is username taken
    name_num = 1
    username = base_username
    while username in existing_usernames:
        name_num += 1
        username = f"{base_username}{name_num}"
    
    # Add the new username to the set of existing usernames
    existing_usernames.add(username)
    return username

# ////////////////////////////////////////////////////////////////////////////////////////

def populate_player(gender, existing_usernames):

    username = generate_unique_username(existing_usernames)

    level_handicap = random.randint(0, 99) # added to make lower levels more common
    level_initial = random.randint(1, 100) #Initial Level 1 to 100

    if level_initial - level_handicap > 0:
        level = level_initial - level_handicap 
    elif level_handicap - level_initial >0:
        level = level_handicap - level_initial
    else:
        level = level_initial = random.randint(1, 100) # When level_handicap = level_initial

    attack = random.randint(level, level * 2) # minimum stat = to level, gain 1 point per stat per level
    defense = random.randint(level, level * 2)
    speed = random.randint(level, level* 2)
    total_hp = random.randint(min(100, 99 + level), max(100, level * 10)) # Min 100 Max 1000
    current_hp = random.randint(0, total_hp) # if 0 dead

    conn = get_db_connection()
    cursor = conn.cursor()
    

    cursor.execute("""
        INSERT INTO Entity (Attack, Defense, Level, Speed, CurrentHP, TotalHP) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (attack, defense, level, speed, current_hp, total_hp))

    entity_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO Player (EntityID, Gender, Username) 
        VALUES (?, ?, ?)
    """, (entity_id, gender, username))

    conn.commit()
    conn.close()

    print(f"Player '{username}' created with Level {level}, Attack {attack}, Defense {defense}, Speed {speed}, HP {total_hp}")

# ////////////////////////////////////////////////////////////////////////////////////////

def drop_player_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Player")
    conn.commit()
    conn.close()
    print("Dropped Player table.")

# ////////////////////////////////////////////////////////////////////////////////////////


def drop_entity_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Entity")
    conn.commit()
    conn.close()
    print("Dropped Entity table.")

# ////////////////////////////////////////////////////////////////////////////////////////

# Get all players (test)
def get_all_players():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Player")
    players = cursor.fetchall()
    conn.close()
    return players

# ////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":

    existing_usernames = set()

    # Generate players (Comment if dropping)

    create_tables()

    for _ in range(1000):
        populate_player(gender=random.choice(['M', 'F']), existing_usernames=existing_usernames)

    print("Generated 1000 players in the database.")

    # Drop table (Uncomment)
    # drop_player_table()
    # drop_entity_table()

