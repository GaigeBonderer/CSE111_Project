import sqlite3
import random
from db_init import create_tables # CREATE handled in db_init.py
from drop_tables import( drop_player, drop_entity, drop_enemy, drop_weapon,
                         drop_guild, drop_clan, drop_inventory, drop_equipped,
                         drop_can_drop, drop_player_belongs, drop_enemy_belongs,
                         drop_all)

descriptor = ["Vicious", "Dark", "Evil", "Brutal", "Savage",
            "Malicious", "Sinister", "Wicked", "Corrupt", "Dreadful",
            "LightFooted", "Armored", "Capatalist", "Communist", "Crazy",
            "Rare", "Wretched", "Jacked", "Starved", "Bloody", ""]

clan_name = ["Orc", "Goblin", "Demon", "Troll", "Vampire",
            "Zombie", "Wraith", "Skeleton", "Golem", "Dragon",
            "Ghost",  "SkinWalker",  "FalseGod",  "Mummy",  "Warlock",
            "Ghoul",  "Arachnid",  "Cyclops",  "Werewolf",  "CursedSpirit"]

def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

# ////////////////////////////////////////////////////////////////////////////////////////////////

def generate_enemy_name():
    return f"{random.choice(descriptor)} {random.choice(clan_name)}"

# ////////////////////////////////////////////////////////////////////////////////////////////////

def assign_weapon_to_enemy(cursor, entity_id, level):

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
        print(f"Assigned {selected_rank} weapon (ID: {weapon_id}) to enemy (ID: {entity_id})")

        assign_drops_to_enemy(cursor, entity_id, weapon_id, level)

# ////////////////////////////////////////////////////////////////////////////////////////////////

def assign_drops_to_enemy(cursor, entity_id, equipped_weapon_id, level):
    rank_probability = ["Common", "Rare", "Epic", "Legendary", "Mystic"]
    
    if level >= 90:
        weights = [0.0, 0.1, 0.2, 0.3, 0.4]
    elif level >= 70:
        weights = [0.1, 0.2, 0.3, 0.3, 0.1]
    elif level >= 50:
        weights = [0.2, 0.3, 0.3, 0.2, 0.0]
    else:
        weights = [0.4, 0.3, 0.2, 0.1, 0.0]

    drop_weapons = {equipped_weapon_id}
    
    num_drops = random.randint(1, 9)

    while len(drop_weapons) < num_drops:
        selected_rank = random.choices(rank_probability, weights=weights, k=1)[0]
        cursor.execute("SELECT WeaponID FROM Weapon WHERE Rank = ? ORDER BY RANDOM() LIMIT 1", (selected_rank,))
        weapon = cursor.fetchone()
        if weapon:
            drop_weapons.add(weapon[0])

    for weapon_id in drop_weapons:
        cursor.execute("INSERT OR IGNORE INTO CanDrop (EntityID, WeaponID) VALUES (?, ?)", (entity_id, weapon_id))
        print(f"Assigned weapon (ID: {weapon_id}) to drop list for enemy (ID: {entity_id})")

# ////////////////////////////////////////////////////////////////////////////////////////////////

def populate_enemy():

    name = generate_enemy_name()
    
    # Input bosses maually, cooler names + specific stats
    is_boss = False

    # Generate stats
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

    health_check = random.randint(1,3)

    if health_check == 1:
        current_hp = total_hp
    elif health_check == 2:
        current_hp = random.randint(0, total_hp)
    else:
        current_hp = 0 # Many more enemies are expected to be dead than players


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

    assign_enemy_to_clan(cursor, entity_id, name)

    assign_weapon_to_enemy(cursor, entity_id, level)

    conn.commit()
    conn.close()

    print(f"Enemy '{name}' created with Level {level}, Attack {attack}, Defense {defense}, Speed {speed}, HP {total_hp}, Current HP {current_hp}, IsBoss {is_boss}")

# ////////////////////////////////////////////////////////////////////////////////////////////////

def assign_enemy_to_clan(cursor, entity_id, enemy_name):
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

# Function to get all enemies (test)
def get_all_enemies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Enemy")
    enemies = cursor.fetchall()
    conn.close()
    return enemies

# ////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":

    # Generate Enemies (Comment if dropping)

    create_tables()

    NumToGenerate = 5000

    for _ in range(NumToGenerate):
        populate_enemy()

    print("Generated " , NumToGenerate , " enemies.")

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