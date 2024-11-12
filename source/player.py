import sqlite3
import random
from db_init import create_tables # CREATE handled in db_init.py
from drop_tables import( drop_player, drop_entity, drop_enemy, drop_weapon,
                         drop_guild, drop_clan, drop_inventory, drop_equipped,
                         drop_can_drop, drop_player_belongs, drop_enemy_belongs,
                         drop_all)


#For username Generation

descriptor = ["Swift", "BeerBellied", "Clever", "Mystic", "Bold",
               "Ancient", "Fierce", "Mighty", "Silent", "Radiant",
               "Hairy", "Evil", "Stealthy", "Big", "Strong",
               "Courageous", "Scandalous", "Noob", "Pro", "Stinky",]

main_name = ["Warrior", "Mage", "Hunter", "Knight", "Rogue",
          "Druid", "Assassin", "Paladin", "Sorcerer", "Guardian",
          "69_", "Dragon", "Ganker", "Slayer", "Skull",
          "Tony", "Savage", "NoNo", "Bender", "Vegetable",]



def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

# ////////////////////////////////////////////////////////////////////////////////////////

def assign_weapon_to_player(cursor, entity_id, level):

    if level >= 90:
        rank_probability = ["Mystic", "Legendary", "Epic", "Rare", "Common"]
        weights = [0.3, 0.4, 0.2, 0.1, 0.0]
    elif level >= 70:
        rank_probability = ["Legendary", "Epic", "Rare", "Common"]
        weights = [0.2, 0.4, 0.3, 0.1]
    elif level >= 50:
        rank_probability = ["Epic", "Rare", "Common"]
        weights = [0.2, 0.5, 0.3]
    else:
        rank_probability = ["Rare", "Common"]
        weights = [0.3, 0.7]
    
    selected_rank = random.choices(rank_probability, weights=weights, k=1)[0]
    
    cursor.execute("SELECT WeaponID FROM Weapon WHERE Rank = ? ORDER BY RANDOM() LIMIT 1", (selected_rank,))
    weapon = cursor.fetchone()
    if weapon:
        weapon_id = weapon[0]
        
        cursor.execute("INSERT INTO Equipped (EntityID, WeaponID) VALUES (?, ?)", (entity_id, weapon_id))
        print(f"Assigned {selected_rank} weapon (ID: {weapon_id}) to player (ID: {entity_id})")

    populate_inventory(cursor, entity_id, selected_rank, level)

# ////////////////////////////////////////////////////////////////////////////////////////

def populate_inventory(cursor, entity_id, rank, level):
    if level >= 90:
        rank_weights = {
            "Common": [0.0, 0.1, 0.3, 0.4, 0.2],
            "Rare": [0.1, 0.2, 0.3, 0.3, 0.1],
            "Epic": [0.0, 0.1, 0.2, 0.4, 0.3],
            "Legendary": [0.0, 0.0, 0.1, 0.3, 0.6],
            "Mystic": [0.0, 0.0, 0.1, 0.3, 0.6]
        }
    elif level >= 70:
        rank_weights = {
            "Common": [0.1, 0.3, 0.4, 0.2, 0.0],
            "Rare": [0.1, 0.3, 0.3, 0.2, 0.1],
            "Epic": [0.1, 0.2, 0.3, 0.3, 0.1],
            "Legendary": [0.0, 0.1, 0.3, 0.4, 0.2],
            "Mystic": [0.0, 0.1, 0.2, 0.3, 0.4]
        }
    elif level >= 50:
        rank_weights = {
            "Common": [0.3, 0.4, 0.2, 0.1, 0.0],
            "Rare": [0.2, 0.4, 0.3, 0.1, 0.0],
            "Epic": [0.1, 0.3, 0.4, 0.2, 0.0],
            "Legendary": [0.1, 0.2, 0.3, 0.3, 0.1],
            "Mystic": [0.0, 0.1, 0.2, 0.3, 0.4]
        }
    else:
        rank_weights = {
            "Common": [0.5, 0.4, 0.1, 0.0, 0.0],
            "Rare": [0.4, 0.3, 0.2, 0.1, 0.0],
            "Epic": [0.3, 0.3, 0.3, 0.1, 0.0],
            "Legendary": [0.2, 0.3, 0.2, 0.2, 0.1],
            "Mystic": [0.1, 0.2, 0.3, 0.2, 0.2]
        }

    ranks_for_inventory = ["Common", "Rare", "Epic", "Legendary", "Mystic"]
    weights = rank_weights[rank]
    
    num_items = random.randint(1, 5)

    for _ in range(num_items):
        selected_rank = random.choices(ranks_for_inventory, weights=weights, k=1)[0]
        cursor.execute("SELECT WeaponID FROM Weapon WHERE Rank = ? ORDER BY RANDOM() LIMIT 1", (selected_rank,))
        weapon = cursor.fetchone()
        if weapon:
            weapon_id = weapon[0]
            cursor.execute("INSERT OR IGNORE INTO Inventory (EntityID, WeaponID) VALUES (?, ?)", (entity_id, weapon_id))
            print(f"Added {selected_rank} weapon (ID: {weapon_id}) to inventory for player (ID: {entity_id})")

# ////////////////////////////////////////////////////////////////////////////////////////

def generate_unique_username(existing_usernames):
    base_username = f"{random.choice(descriptor)}{random.choice(main_name)}"
    
    # add number if username taken
    name_num = 1
    username = base_username
    while username in existing_usernames:
        name_num += 1
        username = f"{base_username}{name_num}"
    
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

    full_health_check = random.randint(1,2)

    if full_health_check == 1: # Makes most players have full hp
        current_hp = total_hp
    else:
        current_hp = random.randint(0, total_hp) # if 0 dead

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Entity (Type, Attack, Defense, Level, Speed, CurrentHP, TotalHP) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('P', attack, defense, level, speed, current_hp, total_hp))
    entity_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO Player (EntityID, Gender, Username) 
        VALUES (?, ?, ?)
    """, (entity_id, gender, username))

    cursor.execute("SELECT GuildName FROM Guild ORDER BY RANDOM() LIMIT 1")
    guild_name = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO PlayerBelongs (EntityID, GuildName) 
        VALUES (?, ?)
    """, (entity_id, guild_name))

    cursor.execute("""
        UPDATE Guild 
        SET TotalPlayers = TotalPlayers + 1 
        WHERE GuildName = ?
    """, (guild_name,))

    assign_weapon_to_player(cursor, entity_id, level)

    conn.commit()
    conn.close()

    print(f"Player '{username}' created with Level {level}, Attack {attack}, Defense {defense}, Speed {speed}, HP {total_hp}, Current HP {current_hp}, Guild '{guild_name}'")

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

    NumToGenerate = 5000

    for _ in range(NumToGenerate):
        populate_player(gender=random.choice(['M', 'F']), existing_usernames=existing_usernames)

    print("Generated " , NumToGenerate , " players.")

    # ////////////////////////////////////////////////////

    # Drop tables (Uncomment as needed)
    # drop_player()
    # drop_entity()
    # drop_enemy()
    # drop_weapon()
    # drop_guild()
    # drop_clan()
    # drop_inventory()
    # drop_equipped()
    # drop_can_drop()
    # drop_player_belongs()
    # drop_enemy_belongs()
    # drop_all()

