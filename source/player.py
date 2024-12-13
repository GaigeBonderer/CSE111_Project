import sqlite3
import random
from db_init import create_tables  # Handles table creation
from drop_tables import (          # Handles table dropping
    drop_player, drop_entity, drop_enemy, drop_weapon,
    drop_guild, drop_clan, drop_inventory, drop_equipped,
    drop_can_drop, drop_player_belongs, drop_enemy_belongs, drop_all
)

# Username generation components
descriptor = ["Swift", "BeerBellied", "Clever", "Mystic", "Bold", "Ancient", "Fierce", "Mighty", "Silent", "Radiant",
              "Hairy", "Evil", "Stealthy", "Big", "Strong", "Courageous", "Scandalous", "Noob", "Pro", "Stinky"]
main_name = ["Warrior", "Mage", "Hunter", "Knight", "Rogue", "Druid", "Assassin", "Paladin", "Sorcerer", "Guardian",
             "69_", "Dragon", "Ganker", "Slayer", "Skull", "Tony", "Savage", "NoNo", "Bender", "Vegetable"]

def get_db_connection():
    #Establish and return a connection to the SQLite database
    return sqlite3.connect('../GameDB.sqlite')

# ////////////////////////////////////////////////////////////////////////////////////////

def assign_weapon_to_player(cursor, entity_id, level):
    #Assign a weapon to a player based on their level
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

    # Select a random weapon rank
    selected_rank = random.choices(rank_probability, weights=weights, k=1)[0]
    cursor.execute("SELECT WeaponID FROM Weapon WHERE Rank = ? ORDER BY RANDOM() LIMIT 1", (selected_rank,))
    weapon = cursor.fetchone()
    if weapon:
        weapon_id = weapon[0]
        cursor.execute("INSERT INTO Equipped (EntityID, WeaponID) VALUES (?, ?)", (entity_id, weapon_id))
        print(f"Assigned {selected_rank} weapon (ID: {weapon_id}) to player (ID: {entity_id})")

    # Populate the player's inventory
    populate_inventory(cursor, entity_id, selected_rank, level)

# ////////////////////////////////////////////////////////////////////////////////////////

def populate_inventory(cursor, entity_id, rank, level):
    #Populate a player's inventory based on their rank and level
    # Define rank weights based on the player's level
    if level >= 90:
        rank_weights = {"Common": [0.0, 0.1, 0.3, 0.4, 0.2], "Rare": [0.1, 0.2, 0.3, 0.3, 0.1], "Epic": [0.0, 0.1, 0.2, 0.4, 0.3],
                        "Legendary": [0.0, 0.0, 0.1, 0.3, 0.6], "Mystic": [0.0, 0.0, 0.1, 0.3, 0.6]}
    elif level >= 70:
        rank_weights = {"Common": [0.1, 0.3, 0.4, 0.2, 0.0], "Rare": [0.1, 0.3, 0.3, 0.2, 0.1], "Epic": [0.1, 0.2, 0.3, 0.3, 0.1],
                        "Legendary": [0.0, 0.1, 0.3, 0.4, 0.2], "Mystic": [0.0, 0.1, 0.2, 0.3, 0.4]}
    elif level >= 50:
        rank_weights = {"Common": [0.3, 0.4, 0.2, 0.1, 0.0], "Rare": [0.2, 0.4, 0.3, 0.1, 0.0], "Epic": [0.1, 0.3, 0.4, 0.2, 0.0],
                        "Legendary": [0.1, 0.2, 0.3, 0.3, 0.1], "Mystic": [0.0, 0.1, 0.2, 0.3, 0.4]}
    else:
        rank_weights = {"Common": [0.5, 0.4, 0.1, 0.0, 0.0], "Rare": [0.4, 0.3, 0.2, 0.1, 0.0], "Epic": [0.3, 0.3, 0.3, 0.1, 0.0],
                        "Legendary": [0.2, 0.3, 0.2, 0.2, 0.1], "Mystic": [0.1, 0.2, 0.3, 0.2, 0.2]}

    ranks_for_inventory = ["Common", "Rare", "Epic", "Legendary", "Mystic"]
    weights = rank_weights[rank]
    num_items = random.randint(1, 5)  # Number of items to add to inventory

    # Add random weapons to the inventory
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
    #Generate a unique username by appending a number if necessary
    base_username = f"{random.choice(descriptor)}{random.choice(main_name)}"
    name_num = 1
    username = base_username
    while username in existing_usernames:
        name_num += 1
        username = f"{base_username}{name_num}"
    existing_usernames.add(username)
    return username

# ////////////////////////////////////////////////////////////////////////////////////////

def populate_player(gender, existing_usernames):
    #Create and populate a player with attributes, weapons, and guild membership
    username = generate_unique_username(existing_usernames)

    # Generate random level and stats
    level_handicap = random.randint(0, 99)
    level_initial = random.randint(1, 100)
    level = max(1, abs(level_initial - level_handicap))

    attack = random.randint(level, level * 2)
    defense = random.randint(level, level * 2)
    speed = random.randint(level, level * 2)
    total_hp = random.randint(min(100, 99 + level), max(100, level * 10))
    current_hp = total_hp if random.randint(1, 2) == 1 else random.randint(0, total_hp)

    # Insert player and stats into database
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

    # Assign player to a random guild
    cursor.execute("SELECT GuildName FROM Guild ORDER BY RANDOM() LIMIT 1")
    guild_name = cursor.fetchone()[0]
    cursor.execute("INSERT INTO PlayerBelongs (EntityID, GuildName) VALUES (?, ?)", (entity_id, guild_name))
    cursor.execute("UPDATE Guild SET TotalPlayers = TotalPlayers + 1 WHERE GuildName = ?", (guild_name,))

    # Assign a weapon and populate inventory
    assign_weapon_to_player(cursor, entity_id, level)

    conn.commit()
    conn.close()

    print(f"Player '{username}' created with Level {level}, Attack {attack}, Defense {defense}, Speed {speed}, HP {total_hp}, Current HP {current_hp}, Guild '{guild_name}'")

# ////////////////////////////////////////////////////////////////////////////////////////

def get_all_players():
    #Fetch all players from the database (for testing)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Player")
    players = cursor.fetchall()
    conn.close()
    return players

# ////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    existing_usernames = set()  # Track unique usernames

    # Create tables and populate players
    create_tables()

    NumToGenerate = 5000  # Number of players to generate
    for _ in range(NumToGenerate):
        populate_player(gender=random.choice(['M', 'F']), existing_usernames=existing_usernames)

    print("Generated", NumToGenerate, "players.")


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

