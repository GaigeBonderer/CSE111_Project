import sqlite3
import random
from db_init import create_tables  # CREATE handled in db_init.py
from drop_tables import (
    drop_player, drop_entity, drop_enemy, drop_weapon,
    drop_guild, drop_clan, drop_inventory, drop_equipped,
    drop_can_drop, drop_player_belongs, drop_enemy_belongs, drop_all
)

Firsts = ["KnightsOfThe", "Iron", "Golden", "Dark", "Mystic",
             "Ancient", "Laughing", "Crimson", "Silent", "CloaksOfThe"]

Middles = ["Sword", "Hammer", "Wolf", "Dragon", "Phoenix",
            "Eagle", "Lion", "Coffin", "BloodOath", "Legion"]

Lasts = ["Order", "Guardians", "Seekers", "Alliance", "Brotherhood",
             "Covenant", "Guild", "Syndicate", "Gankers", "Hunters"]


guild_bonuses = [
    "Warriors: Attack + 15", "Knights: Defense + 15", "Jack Rabbits: Speed + 15", "Vampires: Health Regen + 1 / s",
    "Gankers: Damage to players + 15%", "Assasins: Critical Chance + 10%", "Looters: Luck + 15", "Crafters: Crafting experience + 15%",
    "Vipers: Poison chance + 10%", "Dragons: Burn chance + 10%"
]

def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

# /////////////////////////////////////////////////////////////////////////////////////////////

def generate_guild_name():
    return f"{random.choice(Firsts)}{random.choice(Middles)}{random.choice(Lasts)}"

# /////////////////////////////////////////////////////////////////////////////////////////////

def populate_guild():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Generate a unique guild name
    while True:
        guild_name = generate_guild_name()
        cursor.execute("SELECT GuildName FROM Guild WHERE GuildName = ?", (guild_name,))
        if cursor.fetchone() is None:
            break

    guild_bonus = random.choice(guild_bonuses)
    total_players = 0  # Defaulted to 0

    cursor.execute("""
        INSERT INTO Guild (GuildName, GuildBonus, TotalPlayers)
        VALUES (?, ?, ?)
    """, (guild_name, guild_bonus, total_players))

    conn.commit()
    conn.close()

    print(f"Guild '{guild_name}' created with Bonus '{guild_bonus}' and Total Players '{total_players}'")

# /////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":


    create_tables()

    NumToGenerate = 250 
    for _ in range(NumToGenerate):
        populate_guild()

    print("Generated", NumToGenerate, "guilds.")

# ////////////////////////////////////////////////////////////////////////////

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
