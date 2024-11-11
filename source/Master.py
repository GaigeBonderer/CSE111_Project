import sqlite3
from drop_tables import( drop_player, drop_entity, drop_enemy, drop_weapon,
                         drop_guild, drop_clan, drop_inventory, drop_equipped,
                         drop_can_drop, drop_player_belongs, drop_enemy_belongs,
                         drop_all)
import random
from db_init import create_tables
from guild import populate_guild  # Assuming this function creates and populates the guilds
from clan import populate_clans   # Assuming this function creates and populates the clans
from player import populate_player  # Assuming this function populates individual players
from enemy import populate_enemy   # Assuming this function populates individual enemies

def populate_all_guilds():
    print("Populating Guilds...")
    num_guilds = 100
    for _ in range(num_guilds):
        populate_guild()

def populate_all_clans():
    print("Populating Clans...")
    populate_clans()

def populate_all_players():
    print("Populating Players...")
    existing_usernames = set()
    num_players = 5000
    for _ in range(num_players):
        populate_player(gender=random.choice(['M', 'F']), existing_usernames=existing_usernames)

def populate_all_enemies():
    print("Populating Enemies...")
    num_enemies = 5000
    for _ in range(num_enemies):
        populate_enemy()

if __name__ == "__main__":

    create_tables()

    populate_all_guilds()
    populate_all_clans()
    populate_all_players()
    populate_all_enemies()

    print("Database populated successfully!")

    # ////////////////////////////////////////////////

    # Drop Tables

    # drop_all()
