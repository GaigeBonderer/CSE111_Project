import sqlite3
import random
from db_init import create_tables  # Handles database table creation
from drop_tables import (          # Handles dropping database tables
    drop_player, drop_entity, drop_enemy, drop_weapon,
    drop_guild, drop_clan, drop_inventory, drop_equipped,
    drop_can_drop, drop_player_belongs, drop_enemy_belongs,
    drop_all
)

# Weapon types, ranks, and attributes for generating random weapons
weapon_types = ["Sword", "Spear", "Bow", "Dagger", "Mace",
                "Musket", "Axe", "Hammer", "Claymore", "Flail"]

weapon_ranks = ["Common", "Rare", "Epic", "Legendary", "Mystic"]

descriptors = ["Shadow", "Blood", "Storm", "Frost", "Inferno",
               "Thunder", "Ancient", "Divine", "Dark", "Eternal",
               "Ginourmous", "Tiny", "Icarus's", "All Knowing", "Infinite",
               "Steel", "Ice Giant", "Glory", "False God", "Demon"]

main_names = ["Slayer", "Piercer", "Breaker", "Defender", "Hunter",
              "Warden", "Bane", "Rage", "Crusher", "Ripper",
              "Slaying", "Gutting", "Cutting", "Ripping", "Omnipotent",
              "Dripper", "Dripping", "Crushing", "Defending", "Hunting"]

weapon_attributes = [
    "Poisoned Edge: 1/8 chance to poison per hit",
    "Bone Breaker: 1/8 chance to cripple foe per hit",
    "Dragon Enchanted: 1/8 chance to ignite foe per hit",
    "Golem's Favor: 1/8 chance to generate 250 gold per hit",
    "Icarus's Blessing: 1/8 chance to heal player 25 hp per hit"
]

def get_db_connection():
    #Establish and return a connection to the SQLite database
    return sqlite3.connect('../GameDB.sqlite')

# ///////////////////////////////////////////////////////////////////////////////////////////

def generate_weapon_stats(weapon_type, rank):
    #Generate weapon stats (damage, attack speed, range) based on type and rank
    # Multipliers for weapon stats based on rank
    rank_multipliers = {
        "Common": 1,
        "Rare": 2,
        "Epic": 3,
        "Legendary": 4.5,
        "Mystic": 6
    }

    # Base stat ranges for each weapon type
    type_stats = {
        "Sword": {"Damage": (10, 20), "ATKSpeed": (15, 20), "Range": (1, 2)},
        "Spear": {"Damage": (12, 22), "ATKSpeed": (10, 15), "Range": (3, 4)},
        "Bow": {"Damage": (8, 16), "ATKSpeed": (12, 17), "Range": (8, 12)},
        "Dagger": {"Damage": (6, 12), "ATKSpeed": (20, 25), "Range": (1, 1)},
        "Mace": {"Damage": (15, 25), "ATKSpeed": (8, 12), "Range": (1, 2)},
        "Musket": {"Damage": (18, 28), "ATKSpeed": (7, 10), "Range": (10, 15)},
        "Axe": {"Damage": (14, 24), "ATKSpeed": (10, 15), "Range": (1, 2)},
        "Hammer": {"Damage": (20, 30), "ATKSpeed": (5, 10), "Range": (1, 2)},
        "Claymore": {"Damage": (25, 35), "ATKSpeed": (5, 8), "Range": (2, 3)},
        "Flail": {"Damage": (12, 18), "ATKSpeed": (8, 12), "Range": (1, 2)}
    }

    base_stats = type_stats[weapon_type]
    multiplier = rank_multipliers[rank]

    # Calculate stats using random values within base ranges, scaled by rank multiplier
    damage = int(random.randint(*base_stats["Damage"]) * multiplier)
    atk_speed = int(random.randint(*base_stats["ATKSpeed"]) * multiplier)
    range_stat = int(random.randint(*base_stats["Range"]) * multiplier)

    return damage, atk_speed, range_stat

# ///////////////////////////////////////////////////////////////////////////////////////////

def populate_weapon():
    #Generate and insert a random weapon into the database
    conn = get_db_connection()
    cursor = conn.cursor()

    weapon_type = random.choice(weapon_types)  # Randomly select a weapon type

    # Determine weapon rank based on probability
    rank_prob = random.randint(0, 100)
    if rank_prob < 40:
        rank = "Common"
    elif rank_prob < 70:
        rank = "Rare"
    elif rank_prob < 90:
        rank = "Epic"
    elif rank_prob < 100:
        rank = "Legendary"
    else:
        rank = "Mystic"

    descriptor = random.choice(descriptors)  # Random descriptor
    main_name = random.choice(main_names)    # Random main name
    name = f"{rank} {descriptor} {main_name} {weapon_type}"  # Generate weapon name

    # Generate weapon stats
    damage, atk_speed, range_stat = generate_weapon_stats(weapon_type, rank)

    # Assign a description based on rank
    if rank == "Common":
        description = "Common weapon used by peasants."
    elif rank == "Rare":
        description = "Well-forged weapon, adequate for the battlefield."
    elif rank == "Epic":
        description = "Master-forged weapon, used by commanders and great warriors."
    elif rank == "Legendary":
        description = "You should gift this weapon to the king; it was once used by a warrior of legend."
    else:
        description = "You should not have this... it once belonged to a god."

    # Determine special attribute based on rank
    atr_prob = random.randint(0, 100)
    if rank in ["Common", "Rare"]:
        special_atr = "None"
    elif rank == "Epic" and atr_prob > 90:
        special_atr = random.choice(weapon_attributes)
    elif rank == "Legendary" and atr_prob >= 40:
        special_atr = random.choice(weapon_attributes)
    elif rank == "Mystic":
        special_atr = random.choice(weapon_attributes)
    else:
        special_atr = "None"

    # Insert the weapon into the database
    cursor.execute("""
        INSERT INTO Weapon (Description, Rank, Type, Name, SpecialATR, Damage, ATKSpeed, Range)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (description, rank, weapon_type, name, special_atr, damage, atk_speed, range_stat))

    conn.commit()
    conn.close()

    print(f"Weapon '{name}' created with Type '{weapon_type}', Rank '{rank}', Damage '{damage}', ATKSpeed '{atk_speed}', Range '{range_stat}'")

# ///////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    create_tables()  # Ensure database tables exist

    NumToGenerate = 10000  # Number of weapons to generate
    for _ in range(NumToGenerate):
        populate_weapon()

    print("Generated", NumToGenerate, "weapons.")


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
