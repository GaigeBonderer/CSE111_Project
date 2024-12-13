import sqlite3
import random
from db_init import create_tables  # Handles table creation
from drop_tables import (          # Handles table dropping
    drop_player, drop_entity, drop_enemy, drop_weapon,
    drop_guild, drop_clan, drop_inventory, drop_equipped,
    drop_can_drop, drop_player_belongs, drop_enemy_belongs, drop_all
)

# Lists to construct random guild names
Firsts = ["KnightsOfThe", "Iron", "Golden", "Dark", "Mystic",
          "Ancient", "Laughing", "Crimson", "Silent", "CloaksOfThe"]
Middles = ["Sword", "Hammer", "Wolf", "Dragon", "Phoenix",
           "Eagle", "Lion", "Coffin", "BloodOath", "Legion"]
Lasts = ["Order", "Guardians", "Seekers", "Alliance", "Brotherhood",
         "Covenant", "Guild", "Syndicate", "Gankers", "Hunters"]

# List of random guild bonuses
guild_bonuses = [
    "Warriors: Attack + 15", "Knights: Defense + 15", "Jack Rabbits: Speed + 15", "Vampires: Health Regen + 1 / s",
    "Gankers: Damage to players + 15%", "Assassins: Critical Chance + 10%", "Looters: Luck + 15", "Crafters: Crafting experience + 15%",
    "Vipers: Poison chance + 10%", "Dragons: Burn chance + 10%"
]

def get_db_connection():
    #Establish and return a connection to the SQLite database
    return sqlite3.connect('../GameDB.sqlite')

# /////////////////////////////////////////////////////////////////////////////////////////////

def generate_guild_name():
    #Generate a random guild name by combining elements from name parts
    return f"{random.choice(Firsts)}{random.choice(Middles)}{random.choice(Lasts)}"

# /////////////////////////////////////////////////////////////////////////////////////////////

def populate_guild():
    #Generate and insert a random guild into the Guild table
    conn = get_db_connection()
    cursor = conn.cursor()

    # Generate a unique guild name
    while True:
        guild_name = generate_guild_name()
        cursor.execute("SELECT GuildName FROM Guild WHERE GuildName = ?", (guild_name,))
        if cursor.fetchone() is None:  # Ensure the guild name is unique
            break

    # Select a random bonus for the guild
    guild_bonus = random.choice(guild_bonuses)
    total_players = 0  # Initialize player count to zero

    # Insert the guild into the database
    cursor.execute("""
        INSERT INTO Guild (GuildName, GuildBonus, TotalPlayers)
        VALUES (?, ?, ?)
    """, (guild_name, guild_bonus, total_players))

    conn.commit()  # Commit changes
    conn.close()   # Close the connection

    print(f"Guild '{guild_name}' created with Bonus '{guild_bonus}' and Total Players '{total_players}'")

# /////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    # Create tables in the database if not already present
    create_tables()

    # Generate the specified number of guilds
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
