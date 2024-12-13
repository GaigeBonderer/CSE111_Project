import sqlite3
from drop_tables import (
    drop_player, drop_entity, drop_enemy, drop_weapon,
    drop_guild, drop_clan, drop_inventory, drop_equipped,
    drop_can_drop, drop_player_belongs, drop_enemy_belongs,
    drop_all
)
import random
from db_init import create_tables  # Handles table creation
from guild import populate_guild  # Populates a single guild
from clan import populate_clans   # Populates all clans
from player import populate_player  # Populates a single player
from enemy import populate_enemy    # Populates a single enemy
from weapon import populate_weapon  # Populates a single weapon

# Function to populate multiple guilds
def populate_all_guilds():
    print("Populating Guilds...")
    num_guilds = 100  # Number of guilds to create
    for _ in range(num_guilds):
        populate_guild()

# Function to populate all clans
def populate_all_clans():
    print("Populating Clans...")
    populate_clans()  # Populate predefined clans

# Function to populate multiple players
def populate_all_players():
    print("Populating Players...")
    existing_usernames = set()  # Track existing usernames to ensure uniqueness
    num_players = 5000  # Number of players to create
    for _ in range(num_players):
        populate_player(gender=random.choice(['M', 'F']), existing_usernames=existing_usernames)

# Function to populate multiple enemies
def populate_all_enemies():
    print("Populating Enemies...")
    num_enemies = 5000  # Number of enemies to create
    for _ in range(num_enemies):
        populate_enemy()

# Function to populate multiple weapons
def populate_all_weapons():
    print("Populating Weapons...")
    num_weapons = 10000  # Number of weapons to create
    for _ in range(num_weapons):
        populate_weapon()

if __name__ == "__main__":
    # Create necessary tables in the database
    create_tables()

    # Populate database tables with data
    populate_all_guilds()
    populate_all_clans()
    populate_all_weapons()
    populate_all_players()
    populate_all_enemies()

    print("Database populated successfully!")


    # ////////////////////////////////////////////////

    # Drop Tables

    # drop_all()
