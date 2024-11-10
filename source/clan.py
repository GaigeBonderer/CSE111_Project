import sqlite3
from db_init import create_tables  # CREATE handled in db_init.py
from drop_tables import (
    drop_player, drop_entity, drop_enemy, drop_weapon,
    drop_guild, drop_clan, drop_inventory, drop_equipped,
    drop_can_drop, drop_player_belongs, drop_enemy_belongs, drop_all
)

clan_details = {
    "Orc": {"BossName": "Unc", "ClanBonus": "Big club: Attack + 20"},
    "Goblin": {"BossName": "Mr.GreedyBoi", "ClanBonus": "Bandit: Speed + 30"},
    "Demon": {"BossName": "Pussifer", "ClanBonus": "Menacing: Adversary Attacks miss 1/10 of the time"},
    "Troll": {"BossName": "Redditerm", "ClanBonus": "Bridge Guardian: Defense + 25"},
    "Vampire": {"BossName": "Dracula", "ClanBonus": "Life Steal: Enity heals 1/8 damage done to adversary"},
    "Zombie": {"BossName": "ZomBot", "ClanBonus": "Hoarde: Gain +5 attack per clan member in 10m radius"},
    "Wraith": {"BossName": "Shadowmere", "ClanBonus": "Menacing: Adversary Attacks miss 1/10 of the time"},
    "Skeleton": {"BossName": "Boneclaw", "ClanBonus": "Brittle Bone: Attack * 2, Defense / 2"},
    "Golem": {"BossName": "RingSeeker", "ClanBonus": "Fleshless: Defense + 30"},
    "Dragon": {"BossName": "MegaTooth", "ClanBonus": "Hot Skin: Adversary's physical attack have a 1/4 chance to inflict burn damage"},
    "Ghost": {"BossName": "CasperTheNotSoFirendlyFeind", "ClanBonus": "Possesion: Enity has a 1/2 chance to switch clans below 1/2 health"},
    "SkinWalker": {"BossName": "TheForestKing", "ClanBonus": "Shapeshift: Enity has a 1/2 chance to switch clans below 1/2 health"},
    "FalseGod": {"BossName": "Icarus", "ClanBonus": "Bow Mortal: If enity alerted to player while player is standing Attack + 100"},
    "Mummy": {"BossName": "Apollo", "ClanBonus": "Thick Wraps: Defense + 30"},
    "Warlock": {"BossName": "Heximus", "ClanBonus": "Spell Caster: Ranged Weapon Damge + 20"},
    "Ghoul": {"BossName": "ConductorOfThePoopTrain", "ClanBonus": "Menacing: Adversary Attacks miss 1/10 of the time"},
    "Arachnid": {"BossName": "SheOfManyLegs", "ClanBonus": "Menacing: Adversary Attacks miss 1/10 of the time"},
    "Cyclops": {"BossName": "Montok", "ClanBonus": "One Eye Strength: Defense / 2, Attack * 2"},
    "Werewolf": {"BossName": "DougFromACoupleHousesDown", "ClanBonus": "Transform: Attack + 50 at night"},
    "CursedSpirit": {"BossName": "Sukuna", "ClanBonus": "Ill Intent: Attack + 20, Speed + 10"}
}

def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

# /////////////////////////////////////////////////////////////////////////////////////////

def populate_clans():
    conn = get_db_connection()
    cursor = conn.cursor()

    for clan_name, details in clan_details.items():
        boss_name = details["BossName"]
        clan_bonus = details["ClanBonus"]

        cursor.execute("""
            INSERT INTO Clan (ClanName, ClanBonus, BossName)
            VALUES (?, ?, ?)
        """, (clan_name, clan_bonus, boss_name))

    conn.commit()
    conn.close()
    print("All clans created successfully with unique values.")

# /////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":

    create_tables()

    populate_clans()

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