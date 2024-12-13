import sqlite3
import random
from db_init import create_tables  # Handles table creation
from drop_tables import (          # Handles table dropping
    drop_player, drop_entity, drop_enemy, drop_weapon,
    drop_guild, drop_clan, drop_inventory, drop_equipped,
    drop_can_drop, drop_player_belongs, drop_enemy_belongs,
    drop_all
)

# Enemy descriptors and clan names
descriptor = ["Vicious", "Dark", "Evil", "Brutal", "Savage", "Malicious", "Sinister", "Wicked", "Corrupt", "Dreadful",
              "LightFooted", "Armored", "Capatalist", "Communist", "Crazy", "Rare", "Wretched", "Jacked", "Starved", "Bloody", ""]
clan_name = ["Orc", "Goblin", "Demon", "Troll", "Vampire", "Zombie", "Wraith", "Skeleton", "Golem", "Dragon",
             "Ghost", "SkinWalker", "FalseGod", "Mummy", "Warlock", "Ghoul", "Arachnid", "Cyclops", "Werewolf", "CursedSpirit"]

def get_db_connection():
    #Establish and return a connection to the SQLite database
    return sqlite3.connect('../GameDB.sqlite')

# ////////////////////////////////////////////////////////////////////////////////////////////////

def generate_enemy_name():
    #Generate a random name for an enemy using descriptors and clan names.
    return f"{random.choice(descriptor)} {random.choice(clan_name)}"

# ////////////////////////////////////////////////////////////////////////////////////////////////

def assign_weapon_to_enemy(cursor, entity_id, level):
    #Assign a weapon to an enemy based on its level
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

    # Fetch a random weapon of the selected rank
    cursor.execute("SELECT WeaponID FROM Weapon WHERE Rank = ? ORDER BY RANDOM() LIMIT 1", (selected_rank,))
    weapon = cursor.fetchone()
    if weapon:
        weapon_id = weapon[0]
        cursor.execute("INSERT INTO Equipped (EntityID, WeaponID) VALUES (?, ?)", (entity_id, weapon_id))
        print(f"Assigned {selected_rank} weapon (ID: {weapon_id}) to enemy (ID: {entity_id})")

        # Assign additional drops
        assign_drops_to_enemy(cursor, entity_id, weapon_id, level)

# ////////////////////////////////////////////////////////////////////////////////////////////////

def assign_drops_to_enemy(cursor, entity_id, equipped_weapon_id, level):
    #Assign weapons to an enemy's drop list based on its level.
    rank_probability = ["Common", "Rare", "Epic", "Legendary", "Mystic"]

    if level >= 90:
        weights = [0.0, 0.1, 0.2, 0.3, 0.4]
    elif level >= 70:
        weights = [0.1, 0.2, 0.3, 0.3, 0.1]
    elif level >= 50:
        weights = [0.2, 0.3, 0.3, 0.2, 0.0]
    else:
        weights = [0.4, 0.3, 0.2, 0.1, 0.0]

    drop_weapons = {equipped_weapon_id}  # Include equipped weapon in drop list
    num_drops = random.randint(1, 9)    # Random number of drops

    while len(drop_weapons) < num_drops:
        selected_rank = random.choices(rank_probability, weights=weights, k=1)[0]
        cursor.execute("SELECT WeaponID FROM Weapon WHERE Rank = ? ORDER BY RANDOM() LIMIT 1", (selected_rank,))
        weapon = cursor.fetchone()
        if weapon:
            drop_weapons.add(weapon[0])

    # Insert weapons into the CanDrop table
    for weapon_id in drop_weapons:
        cursor.execute("INSERT OR IGNORE INTO CanDrop (EntityID, WeaponID) VALUES (?, ?)", (entity_id, weapon_id))
        print(f"Assigned weapon (ID: {weapon_id}) to drop list for enemy (ID: {entity_id})")

# ////////////////////////////////////////////////////////////////////////////////////////////////

def populate_enemy():
    #Generate and insert a random enemy into the database
    name = generate_enemy_name()
    is_boss = False  # Default enemy type

    # Generate random stats
    level_weight = random.randint(1, 100)
    if level_weight > 90:
        level_init = random.randint(75, 95)
    elif level_weight > 70:
        level_init = random.randint(50, 75)
    else:
        level_init = random.randint(5, 50)
    level = level_init - (level_init % 5)

    attack = random.randint(level, level * 2)
    defense = random.randint(level, level * 2)
    speed = random.randint(level, level * 2)
    total_hp = random.randint(min(100, 99 + level), max(100, level * 10))

    # Determine current HP
    health_check = random.randint(1, 3)
    if health_check == 1:
        current_hp = total_hp
    elif health_check == 2:
        current_hp = random.randint(0, total_hp)
    else:
        current_hp = 0  # More enemies are expected to be dead

    # Insert enemy into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Entity (Type, Attack, Defense, Level, Speed, CurrentHP, TotalHP) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('E', attack, defense, level, speed, current_hp, total_hp))

    entity_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO Enemy (EntityID, Name, IsBoss) 
        VALUES (?, ?, ?)
    """, (entity_id, name, is_boss))

    # Assign enemy to a clan and equip weapons
    assign_enemy_to_clan(cursor, entity_id, name)
    assign_weapon_to_enemy(cursor, entity_id, level)

    conn.commit()
    conn.close()

    print(f"Enemy '{name}' created with Level {level}, Attack {attack}, Defense {defense}, Speed {speed}, HP {total_hp}, Current HP {current_hp}, IsBoss {is_boss}")

# ////////////////////////////////////////////////////////////////////////////////////////////////

def assign_enemy_to_clan(cursor, entity_id, enemy_name):
    #Assign an enemy to a clan based on its name.
    clan = next((clan for clan in clan_name if clan in enemy_name), None)
    if clan:
        cursor.execute("""
            INSERT INTO EnemyBelongs (EntityID, ClanName)
            VALUES (?, ?)
        """, (entity_id, clan))
        print(f"Assigned '{enemy_name}' to clan '{clan}'")
    else:
        print(f"Could not assign clan for '{enemy_name}'")

# ////////////////////////////////////////////////////////////////////////////////////////////////

def get_all_enemies():
    #Fetch all enemies from the database (for testing).
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Enemy")
    enemies = cursor.fetchall()
    conn.close()
    return enemies

# ////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    create_tables()  # Ensure tables exist before populating
    NumToGenerate = 5000  # Number of enemies to generate
    for _ in range(NumToGenerate):
        populate_enemy()
    print("Generated", NumToGenerate, "enemies.")


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