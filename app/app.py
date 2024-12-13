from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'weapon'



def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite') # Establishes connection to database




@app.route('/')
def home():
    return render_template('login.html') # Defines route to first page to load




@app.route('/login', methods=['GET', 'POST']) # Login Route
def login():
    return render_template('login.html')




@app.route('/portal') # Routes to dashboard
def admin_page():
    return render_template('portal.html')




@app.route('/logout') # Logout Route
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))




@app.route('/create', methods=['GET', 'POST'])  # Route for the Create page
def create_page():
    if request.method == 'POST':  # Handle form submission via POST method
        table = request.form.get('table')  # Retrieve the target table from the form.

        # Establish a connection to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        if table == "Player":
            # Retrieve player-specific form data.
            username = request.form.get('username')
            gender = request.form.get('gender')

            atk = request.form.get('atk')  # Obtain Attack stat
            defe = request.form.get('defe')  # Obtain Defense stat
            lvl = request.form.get('lvl')  # Obtain Level
            spd = request.form.get('spd')  # Obtain Speed stat.
            chp = request.form.get('chp')  # Obtain Current health points
            thp = request.form.get('thp')  # Obtain Total health points

            # Insert player data into the Entity table
            cursor.execute("""
                INSERT INTO Entity (Type, Attack, Defense, Level, Speed, CurrentHP, TotalHP)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('P', atk, defe, lvl, spd, chp, thp))
            entity_id = cursor.lastrowid  # Retrieve the ID of inserted entity

            # Insert player-specific data into the Player table
            cursor.execute("""
                INSERT INTO Player (EntityID, Gender, Username)
                VALUES (?, ?, ?)
            """, (entity_id, gender, username))

        elif table == "Enemy":
            # Retrieve enemy-specific form data
            name = request.form.get('name')  # Obtain Enemy name.
            is_boss = request.form.get('isBoss')  # Obtain Whether the enemy is a boss

            atk = request.form.get('atk')  # Obtain Attack stat
            defe = request.form.get('defe')  # Obtain Defense stat
            lvl = request.form.get('lvl')  # Obtain Level
            spd = request.form.get('spd')  # Obtain Speed stat
            chp = request.form.get('chp')  # Obtain Current health ponts
            thp = request.form.get('thp')  # Obtain Total health points

            # Insert enemy data into the Entity table
            cursor.execute("""
                INSERT INTO Entity (Type, Attack, Defense, Level, Speed, CurrentHP, TotalHP)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('E', atk, defe, lvl, spd, chp, thp))
            entity_id = cursor.lastrowid  # Retrieve the ID of the inserted entity

            # Insert enemy-specific data into the Enemy table
            cursor.execute("""
                INSERT INTO Enemy (EntityID, Name, IsBoss)
                VALUES (?, ?, ?)
            """, (entity_id, name, is_boss))

        elif table == "Weapon":
            # Retrieve weapon-specific form data
            desc = request.form.get('desc')  # Obtain Weapon description
            rank = request.form.get('rank')  # Obtain Weapon rank
            type = request.form.get('type')  # Obtain Weapon type
            name = request.form.get('name')  # Obtain Weapon name
            special = request.form.get('special')  # Obtain Special attribute
            damage = request.form.get('damage')  # Obtain Damage stat
            atkspeed = request.form.get('atkspeed')  # Obtain Attack speed
            range = request.form.get('range')  # Obtain Weapon range

            # Insert weapon data into the Weapon table
            cursor.execute("""
                INSERT INTO Weapon (Description, Rank, Type, Name, SpecialATR, Damage, ATKSpeed, Range)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (desc, rank, type, name, special, damage, atkspeed, range))

        elif table == "Guild":
            # Retrieve guild-specific form data
            guild_name = request.form.get('guildName')  # Obtain Guild name
            guild_bonus = request.form.get('guildBonus')  # Obtain Guild bonus attribute

            # Insert guild data into Guild table
            cursor.execute("""
                INSERT INTO Guild (GuildName, GuildBonus, TotalPlayers)
                VALUES (?, ?, ?)
            """, (guild_name, guild_bonus, 0))  # Initial total players set to 0

        elif table == "Clan":
            # Retrieve clan-specific form data
            clan_name = request.form.get('clanName')  # Obtain Clan name
            clan_bonus = request.form.get('clanBonus')  # Obtain Clan bonus attribute
            boss_name = request.form.get('bossName')  # Obtain Name of the clan's boss

            # Insert clan data into the Clan table
            cursor.execute("""
                INSERT INTO Clan (ClanName, ClanBonus, BossName)
                VALUES (?, ?, ?)
            """, (clan_name, clan_bonus, boss_name))

        # Commit all the database transactions to save changes
        conn.commit()
        conn.close()  # Close the database connection.
        return redirect(url_for('create_page'))

    return render_template('create.html')







@app.route('/delete', methods=['GET', 'POST'])
def delete_page():

    if request.method == 'POST':
        # Retrieve action type, entity ID, and table name from the form
        action = request.form.get('action')
        entity_id = request.form.get('entityID')
        table_name = request.form.get('tableName')

        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Handle deletion of a player
        if action == "delete_player":
            entity_id = request.form.get('entityID')

            # Fetch the player's guild association, if any
            cursor.execute("""
                SELECT GuildName FROM PlayerBelongs WHERE EntityID = ?
            """, (entity_id,))
            guild_name = cursor.fetchone()

            # Remove player-guild association
            cursor.execute("DELETE FROM PlayerBelongs WHERE EntityID = ?", (entity_id,))

            # Decrease guild player count if player belongs to a guild
            if guild_name:
                cursor.execute("""
                    UPDATE Guild
                    SET TotalPlayers = TotalPlayers - 1
                    WHERE GuildName = ?
                """, (guild_name[0],))

            # Remove player's equipped items, inventory, and the player entry
            cursor.execute("DELETE FROM Equipped WHERE EntityID = ?", (entity_id,))
            cursor.execute("DELETE FROM Inventory WHERE EntityID = ?", (entity_id,))
            cursor.execute("DELETE FROM Player WHERE EntityID = ?", (entity_id,))
            cursor.execute("DELETE FROM Entity WHERE EntityID = ?", (entity_id,))

        # Handle deletion of an enemy
        elif action == "delete_enemy":
            entity_id = request.form.get('entityID')

            # Remove enemy-clan association, Can Drop entires, and the enemy entry
            cursor.execute("DELETE FROM EnemyBelongs WHERE EntityID = ?", (entity_id,))
            cursor.execute("DELETE FROM CanDrop WHERE EntityID = ?", (entity_id,))
            cursor.execute("DELETE FROM Equipped WHERE EntityID = ?", (entity_id,))
            cursor.execute("DELETE FROM Enemy WHERE EntityID = ?", (entity_id,))
            cursor.execute("DELETE FROM Entity WHERE EntityID = ?", (entity_id,))
            print(f"Enemy with EntityID {entity_id} and all related entries deleted.")

        # Handle deletion of a clan
        elif action == "delete_clan":
            clan_name = request.form.get('clanName')

            # Remove the clan and all associated enemy entries
            cursor.execute("DELETE FROM Clan WHERE ClanName = ?", (clan_name,))
            cursor.execute("DELETE FROM EnemyBelongs WHERE ClanName = ?", (clan_name,))
            print(f"Clan '{clan_name}' and related entries deleted.")

        # Handle deletion of a guild
        elif action == "delete_guild":
            guild_name = request.form.get('guildName')

            # Remove the guild and all associated player entries
            cursor.execute("DELETE FROM Guild WHERE GuildName = ?", (guild_name,))
            cursor.execute("DELETE FROM PlayerBelongs WHERE GuildName = ?", (guild_name,))
            print(f"Guild '{guild_name}' and related entries deleted.")

        # Handle deletion of a weapon
        elif action == "delete_weapon":
            weapon_id = request.form.get('weaponID')

            # Remove the weapon and all references in inventory, equipped, and droppable items
            cursor.execute("DELETE FROM Weapon WHERE WeaponID = ?", (weapon_id,))
            cursor.execute("DELETE FROM Inventory WHERE WeaponID = ?", (weapon_id,))
            cursor.execute("DELETE FROM Equipped WHERE WeaponID = ?", (weapon_id,))
            cursor.execute("DELETE FROM CanDrop WHERE WeaponID = ?", (weapon_id,))
            print(f"Weapon with WeaponID {weapon_id} and related entries deleted.")

        # Commit all changes to the database and close the connection
        conn.commit()
        conn.close()

    # Render the deletion page template
    return render_template('delete.html')







@app.route('/update', methods=['GET', 'POST'])
def update_page():
    # Handle updates via POST request
    if request.method == 'POST':
        action = request.form.get('action')  # Get the action type
        conn = get_db_connection()  # Establish database connection
        cursor = conn.cursor()

        if action == "update_player":
            entity_id = request.form.get('entityID')  # Get the player ID
            
            # Attributes for the Entity table
            atk = request.form.get('atk')
            defe = request.form.get('defe')
            lvl = request.form.get('lvl')
            spd = request.form.get('spd')
            chp = request.form.get('chp')
            thp = request.form.get('thp')
            
            # Attributes for the Player table
            username = request.form.get('username')
            gender = request.form.get('gender')

            # Prepare dynamic update query for Entity table
            entity_update_fields = []
            entity_update_values = []
            if atk:
                entity_update_fields.append("Attack = ?")
                entity_update_values.append(atk)
            if defe:
                entity_update_fields.append("Defense = ?")
                entity_update_values.append(defe)
            if lvl:
                entity_update_fields.append("Level = ?")
                entity_update_values.append(lvl)
            if spd:
                entity_update_fields.append("Speed = ?")
                entity_update_values.append(spd)
            if chp:
                entity_update_fields.append("CurrentHP = ?")
                entity_update_values.append(chp)
            if thp:
                entity_update_fields.append("TotalHP = ?")
                entity_update_values.append(thp)
            if entity_update_fields:
                entity_update_values.append(entity_id)
                entity_update_query = f"""
                    UPDATE Entity
                    SET {', '.join(entity_update_fields)}
                    WHERE EntityID = ?
                """
                cursor.execute(entity_update_query, tuple(entity_update_values))

            # Prepare dynamic update query for Player table
            player_update_fields = []
            player_update_values = []
            if username:
                player_update_fields.append("Username = ?")
                player_update_values.append(username)
            if gender:
                player_update_fields.append("Gender = ?")
                player_update_values.append(gender)
            if player_update_fields:
                player_update_values.append(entity_id)
                player_update_query = f"""
                    UPDATE Player
                    SET {', '.join(player_update_fields)}
                    WHERE EntityID = ?
                """
                cursor.execute(player_update_query, tuple(player_update_values))

            conn.commit()  # Commit changes to the database

        elif action == "update_enemy":
            entity_id = request.form.get('entityID')  # Get the enemy ID
            
            # Attributes for the Entity table
            atk = request.form.get('atk')
            defe = request.form.get('defe')
            lvl = request.form.get('lvl')
            spd = request.form.get('spd')
            chp = request.form.get('chp')
            thp = request.form.get('thp')
            
            # Attributes for the Enemy table
            name = request.form.get('name')
            is_boss = request.form.get('isBoss')

            # Prepare dynamic update query for Entity table
            entity_update_fields = []
            entity_update_values = []
            if atk:
                entity_update_fields.append("Attack = ?")
                entity_update_values.append(atk)
            if defe:
                entity_update_fields.append("Defense = ?")
                entity_update_values.append(defe)
            if lvl:
                entity_update_fields.append("Level = ?")
                entity_update_values.append(lvl)
            if spd:
                entity_update_fields.append("Speed = ?")
                entity_update_values.append(spd)
            if chp:
                entity_update_fields.append("CurrentHP = ?")
                entity_update_values.append(chp)
            if thp:
                entity_update_fields.append("TotalHP = ?")
                entity_update_values.append(thp)
            if entity_update_fields:
                entity_update_values.append(entity_id)
                entity_update_query = f"""
                    UPDATE Entity
                    SET {', '.join(entity_update_fields)}
                    WHERE EntityID = ?
                """
                cursor.execute(entity_update_query, tuple(entity_update_values))

            # Prepare dynamic update query for Enemy table
            enemy_update_fields = []
            enemy_update_values = []
            if name:
                enemy_update_fields.append("Name = ?")
                enemy_update_values.append(name)
            if is_boss:
                enemy_update_fields.append("IsBoss = ?")
                enemy_update_values.append(is_boss)
            if enemy_update_fields:
                enemy_update_values.append(entity_id)
                enemy_update_query = f"""
                    UPDATE Enemy
                    SET {', '.join(enemy_update_fields)}
                    WHERE EntityID = ?
                """
                cursor.execute(enemy_update_query, tuple(enemy_update_values))

            conn.commit()  # Commit changes to the database

        elif action == "assign_player_guild":
            entity_id = request.form.get('entityID')  # Get player ID
            new_guild_name = request.form.get('guildName')  # New guild assignment

            # Check current guild association for the player
            cursor.execute("""
                SELECT GuildName
                FROM PlayerBelongs
                WHERE EntityID = ?
            """, (entity_id,))
            current_guild = cursor.fetchone()

            # Remove from current guild if assigned
            if current_guild:
                previous_guild_name = current_guild[0]
                cursor.execute("""
                    UPDATE Guild
                    SET TotalPlayers = TotalPlayers - 1
                    WHERE GuildName = ?
                """, (previous_guild_name,))
                cursor.execute("""
                    DELETE FROM PlayerBelongs
                    WHERE EntityID = ? AND GuildName = ?
                """, (entity_id, previous_guild_name))

            # Assign to new guild
            cursor.execute("""
                INSERT OR REPLACE INTO PlayerBelongs (EntityID, GuildName)
                VALUES (?, ?)
            """, (entity_id, new_guild_name))
            cursor.execute("""
                UPDATE Guild
                SET TotalPlayers = TotalPlayers + 1
                WHERE GuildName = ?
            """, (new_guild_name,))

        elif action == "assign_enemy_clan":
            entity_id = request.form.get('entityID')  # Get enemy ID
            new_clan_name = request.form.get('clanName')  # New clan assignment

            # Check current clan association for the enemy
            cursor.execute("""
                SELECT ClanName
                FROM EnemyBelongs
                WHERE EntityID = ?
            """, (entity_id,))
            current_clan = cursor.fetchone()

            # Remove from current clan if different
            if current_clan:
                current_clan_name = current_clan[0]
                if current_clan_name != new_clan_name:
                    cursor.execute("""
                        DELETE FROM EnemyBelongs
                        WHERE EntityID = ? AND ClanName = ?
                    """, (entity_id, current_clan_name))

            # Assign to new clan
            cursor.execute("""
                INSERT OR REPLACE INTO EnemyBelongs (EntityID, ClanName)
                VALUES (?, ?)
            """, (entity_id, new_clan_name))

            conn.commit()  # Commit changes to the database

        elif action == "update_weapon":
            weaponID = request.form.get('weaponID')  # Get weapon ID

            # Weapon attributes
            desc = request.form.get('desc')
            rank = request.form.get('rank')
            type = request.form.get('type')
            name = request.form.get('name')
            special = request.form.get('special')
            damage = request.form.get('damage')
            atkspeed = request.form.get('atkspeed')
            range = request.form.get('range')

            # Prepare dynamic update query for Weapon table
            update_fields = []
            update_values = []
            if desc:
                update_fields.append("Description = ?")
                update_values.append(desc)
            if rank:
                update_fields.append("Rank = ?")
                update_values.append(rank)
            if type:
                update_fields.append("Type = ?")
                update_values.append(type)
            if name:
                update_fields.append("Name = ?")
                update_values.append(name)
            if special:
                update_fields.append("SpecialATR = ?")
                update_values.append(special)
            if damage:
                update_fields.append("Damage = ?")
                update_values.append(damage)
            if atkspeed:
                update_fields.append("ATKSpeed = ?")
                update_values.append(atkspeed)
            if range:
                update_fields.append("Range = ?")
                update_values.append(range)

            # Execute update if fields exist
            if update_fields:
                update_values.append(weaponID)
                update_query = f"""
                    UPDATE Weapon
                    SET {', '.join(update_fields)}
                    WHERE WeaponID = ?
                """
                cursor.execute(update_query, tuple(update_values))
                conn.commit()  # Commit changes to the database

        elif action == "update_guild":
            # Retrieve guild details from the form
            old_guild_name = request.form.get('oldGuildName')
            new_guild_name = request.form.get('newGuildName')
            guild_bonus = request.form.get('guildBonus')
            total_players = request.form.get('totalPlayers')

            # Build dynamic update query for the Guild table
            update_guild_query = "UPDATE Guild SET "
            update_values = []
            update_fields = []

            if new_guild_name:
                update_fields.append("GuildName = ?")
                update_values.append(new_guild_name)
            if guild_bonus:
                update_fields.append("GuildBonus = ?")
                update_values.append(guild_bonus)
            if total_players:
                update_fields.append("TotalPlayers = ?")
                update_values.append(total_players)

            if update_fields:
                update_guild_query += ", ".join(update_fields) + " WHERE GuildName = ?"
                update_values.append(old_guild_name)

                # Execute the Guild update query
                cursor.execute(update_guild_query, update_values)
                print(f"Guild '{old_guild_name}' updated successfully.")

            # Update PlayerBelongs table if the guild name was changed
            if new_guild_name:
                cursor.execute("""
                    UPDATE PlayerBelongs
                    SET GuildName = ?
                    WHERE GuildName = ?
                """, (new_guild_name, old_guild_name))
                print(f"PlayerBelongs table updated to new GuildName '{new_guild_name}'.")

            conn.commit()

        elif action == "update_clan":
            # Retrieve clan details from the form
            old_clan_name = request.form.get('oldClanName')
            new_clan_name = request.form.get('newClanName')
            clan_bonus = request.form.get('clanBonus')
            boss_name = request.form.get('bossName')

            # Build dynamic update query for the Clan table
            update_clan_query = "UPDATE Clan SET "
            update_values = []
            update_fields = []

            if new_clan_name:
                update_fields.append("ClanName = ?")
                update_values.append(new_clan_name)
            if clan_bonus:
                update_fields.append("ClanBonus = ?")
                update_values.append(clan_bonus)
            if boss_name:
                update_fields.append("BossName = ?")
                update_values.append(boss_name)

            if update_fields:
                update_clan_query += ", ".join(update_fields) + " WHERE ClanName = ?"
                update_values.append(old_clan_name)

                # Execute the Clan update query
                cursor.execute(update_clan_query, update_values)
                print(f"Clan '{old_clan_name}' updated successfully.")

            # Update EnemyBelongs table if the clan name was changed
            if new_clan_name:
                cursor.execute("""
                    UPDATE EnemyBelongs
                    SET ClanName = ?
                    WHERE ClanName = ?
                """, (new_clan_name, old_clan_name))
                print(f"EnemyBelongs table updated to new ClanName '{new_clan_name}'.")

            conn.commit()

        elif action == "assign_weapon_equipped":
            # Retrieve entity and weapon IDs
            entity_id = request.form.get('entityID')
            weapon_id = request.form.get('weaponID')

            # Validate existence of Entity and Weapon
            cursor.execute("SELECT EntityID FROM Entity WHERE EntityID = ?", (entity_id,))
            entity_exists = cursor.fetchone()
            cursor.execute("SELECT WeaponID FROM Weapon WHERE WeaponID = ?", (weapon_id,))
            weapon_exists = cursor.fetchone()

            if not entity_exists:
                conn.close()
                return render_template('read.html', message=f"Entity with ID {entity_id} does not exist.", column_names=None, data=None)

            if not weapon_exists:
                conn.close()
                return render_template('read.html', message=f"Weapon with ID {weapon_id} does not exist.", column_names=None, data=None)

            # Check if the weapon is already equipped
            cursor.execute("SELECT * FROM Equipped WHERE WeaponID = ?", (weapon_id,))
            already_equipped = cursor.fetchone()
            if already_equipped:
                conn.close()
                return render_template('read.html', message=f"Weapon with ID {weapon_id} is already equipped by another entity.", column_names=None, data=None)

            # Remove any currently equipped weapon for the entity
            cursor.execute("SELECT WeaponID FROM Equipped WHERE EntityID = ?", (entity_id,))
            currently_equipped = cursor.fetchone()
            if currently_equipped:
                cursor.execute("DELETE FROM Equipped WHERE EntityID = ?", (entity_id,))

            # Assign the new weapon to the entity
            cursor.execute("""
                INSERT INTO Equipped (EntityID, WeaponID)
                VALUES (?, ?)
            """, (entity_id, weapon_id))

            conn.commit()
            conn.close()
            return render_template('read.html', message=f"Weapon with ID {weapon_id} successfully equipped to Entity with ID {entity_id}.", column_names=None, data=None)

        elif action == "assign_weapon_inventory":
            # Retrieve entity and weapon IDs
            entity_id = request.form.get('entityID')
            weapon_id = request.form.get('weaponID')

            # Check if weapon is already in the inventory
            cursor.execute("""
                SELECT 1 FROM Inventory
                WHERE EntityID = ? AND WeaponID = ?
            """, (entity_id, weapon_id))
            result = cursor.fetchone()

            if result:
                message = f"Weapon ID {weapon_id} is already in the inventory of Entity ID {entity_id}."
            else:
                # Add weapon to inventory
                cursor.execute("""
                    INSERT INTO Inventory (EntityID, WeaponID)
                    VALUES (?, ?)
                """, (entity_id, weapon_id))
                conn.commit()
                message = f"Weapon ID {weapon_id} successfully added to the inventory of Entity ID {entity_id}."

            conn.close()
            return render_template('read.html', message=message)

        elif action == "assign_weapon_candrop":
            # Retrieve entity and weapon IDs
            entity_id = request.form.get('entityID')
            weapon_id = request.form.get('weaponID')

            # Check if weapon is already in the CanDrop list
            cursor.execute("""
                SELECT 1 FROM CanDrop
                WHERE EntityID = ? AND WeaponID = ?
            """, (entity_id, weapon_id))
            result = cursor.fetchone()

            if result:
                message = f"Weapon ID {weapon_id} is already in the CanDrop list for Entity ID {entity_id}."
            else:
                # Add weapon to CanDrop list
                cursor.execute("""
                    INSERT INTO CanDrop (EntityID, WeaponID)
                    VALUES (?, ?)
                """, (entity_id, weapon_id))
                conn.commit()
                message = f"Weapon ID {weapon_id} successfully added to the CanDrop list for Entity ID {entity_id}."

            conn.close()
            return render_template('read.html', message=message)

        # Commit and close the database connection
        conn.commit()
        conn.close()
        return redirect(url_for('update_page'))

    # Render the update page for GET requests
    return render_template('update.html')




@app.route('/read', methods=['GET', 'POST'])
def read_page():
    # Initialize variables for column names and data
    column_names = []
    data = []

    if request.method == 'POST':
        # Get the action type from the form
        action = request.form.get('action')

        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        if action == "all_players":
            # Fetch all players and their corresponding entity attributes
            cursor.execute("""
                SELECT 
                    p.EntityID AS 'Entity ID',
                    p.Username AS 'Username',
                    p.Gender AS 'Gender',
                    e.Level AS 'Level',
                    e.Attack AS 'Attack',
                    e.Defense AS 'Defense',
                    e.Speed AS 'Speed',
                    e.CurrentHP AS 'Current HP',
                    e.TotalHP AS 'Total HP'
                FROM 
                    Player p
                INNER JOIN 
                    Entity e 
                ON 
                    p.EntityID = e.EntityID
                ORDER BY 
                    p.EntityID ASC
            """)
            # Retrieve column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            conn.close()
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "all_enemies":
            # Fetch all enemies and their corresponding entity attributes
            cursor.execute("""
                SELECT 
                    e.EntityID AS 'Entity ID',
                    en.Name AS 'Name',
                    e.Level AS 'Level',
                    e.Attack AS 'Attack',
                    e.Defense AS 'Defense',
                    e.Speed AS 'Speed',
                    e.CurrentHP AS 'Current HP',
                    e.TotalHP AS 'Total HP',
                    en.IsBoss AS 'Is Boss'
                FROM 
                    Enemy en
                INNER JOIN 
                    Entity e 
                ON 
                    en.EntityID = e.EntityID
                ORDER BY 
                    e.EntityID ASC
            """)
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            conn.close()
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "all_guilds":
            # Fetch all guilds with their attributes
            cursor.execute("""
                SELECT 
                    GuildName AS 'Guild Name',
                    GuildBonus AS 'Guild Bonus',
                    TotalPlayers AS 'Total Players'
                FROM 
                    Guild
                ORDER BY 
                    TotalPlayers DESC
            """)
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            conn.close()
            return render_template('read.html', column_names=column_names, data=data)
        
        elif action == "all_clans":
            # Fetch all clans with their attributes
            cursor.execute("""
                SELECT 
                    ClanName AS 'Clan Name',
                    ClanBonus AS 'Clan Bonus',
                    BossName AS 'Boss Name'
                FROM 
                    Clan
                ORDER BY 
                    ClanName ASC
            """)
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            conn.close()
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "all_weapons":
            # Fetch all weapons and their attributes
            cursor.execute("""
                SELECT 
                    WeaponID AS 'Weapon ID',
                    Name AS 'Name',
                    Type AS 'Type',
                    Rank AS 'Rank',
                    Damage AS 'Damage',
                    ATKSpeed AS 'Attack Speed',
                    Range AS 'Range',
                    SpecialATR AS 'Special Attribute',
                    Description AS 'Description'
                FROM 
                    Weapon
                ORDER BY 
                    WeaponID ASC
            """)
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            conn.close()
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "guild_members":
            # Fetch all members of a specific guild
            guild_name = request.form.get('guildName')
            cursor.execute("""
                SELECT 
                    pb.GuildName AS 'Guild Name',
                    p.EntityID AS 'Entity ID',
                    e.Level AS 'Level',
                    e.Attack AS 'Attack',
                    e.Defense AS 'Defense',
                    e.Speed AS 'Speed',
                    e.CurrentHP AS 'Current HP',
                    e.TotalHP AS 'Total HP',
                    p.Username AS 'Username',
                    p.Gender AS 'Gender'
                FROM 
                    PlayerBelongs pb
                INNER JOIN 
                    Player p ON pb.EntityID = p.EntityID
                INNER JOIN 
                    Entity e ON p.EntityID = e.EntityID
                WHERE 
                    pb.GuildName = ?
                ORDER BY 
                    e.Level DESC
            """, (guild_name,))
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            conn.close()
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "clan_members":
            # Fetch all members of a specific clan
            clan_name = request.form.get('clanName')
            cursor.execute("""
                SELECT 
                    c.ClanName AS 'Clan Name',
                    e.Level AS 'Level',
                    e.Attack AS 'Attack',
                    e.Defense AS 'Defense',
                    e.Speed AS 'Speed',
                    e.CurrentHP AS 'Current HP',
                    e.TotalHP AS 'Total HP',
                    en.Name AS 'Enemy Name',
                    en.IsBoss AS 'Is Boss'
                FROM 
                    Clan c
                INNER JOIN 
                    EnemyBelongs eb ON c.ClanName = eb.ClanName
                INNER JOIN 
                    Enemy en ON eb.EntityID = en.EntityID
                INNER JOIN 
                    Entity e ON en.EntityID = e.EntityID
                WHERE 
                    c.ClanName = ?
                ORDER BY 
                    e.Level DESC
            """, (clan_name,))
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            conn.close()
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "specific_entity":
            # Retrieve entity ID from the form
            entity_id = request.form.get('entityID')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Determine the entity type (Player or Enemy)
            cursor.execute("SELECT Type FROM Entity WHERE EntityID = ?", (entity_id,))
            result = cursor.fetchone()
            entity_type = result[0]

            if entity_type == 'P':  # Entity is a Player
                cursor.execute("""
                    SELECT 
                        e.EntityID AS 'Entity ID',
                        p.Username AS 'Username',
                        e.Level AS 'Level',
                        e.Attack AS 'Attack',
                        e.Defense AS 'Defense',
                        e.Speed AS 'Speed',
                        e.CurrentHP AS 'Current HP',
                        e.TotalHP AS 'Total HP',
                        p.Gender AS 'Gender'
                    FROM 
                        Entity e
                    INNER JOIN 
                        Player p ON e.EntityID = p.EntityID
                    WHERE 
                        e.EntityID = ?
                """, (entity_id,))
            elif entity_type == 'E':  # Entity is an Enemy
                cursor.execute("""
                    SELECT 
                        e.EntityID AS 'Entity ID',
                        en.Name AS 'Enemy Name',
                        e.Level AS 'Level',
                        e.Attack AS 'Attack',
                        e.Defense AS 'Defense',
                        e.Speed AS 'Speed',
                        e.CurrentHP AS 'Current HP',
                        e.TotalHP AS 'Total HP',
                        en.IsBoss AS 'Is Boss'
                    FROM 
                        Entity e
                    INNER JOIN 
                        Enemy en ON e.EntityID = en.EntityID
                    WHERE 
                        e.EntityID = ?
                """, (entity_id,))
            else:
                # Handle unexpected entity type
                return render_template('read.html', column_names=[], data=[], error=f"Unexpected entity type for ID {entity_id}.")

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with entity data
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "specific_weapon":
            # Retrieve weapon ID from the form
            weapon_id = request.form.get('weaponID')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch specific weapon details
            cursor.execute("""
                SELECT 
                    WeaponID AS 'Weapon ID',
                    Name AS 'Weapon Name',
                    Type AS 'Type',
                    Rank AS 'Rank',
                    Description AS 'Description',
                    SpecialATR AS 'Special Attribute',
                    Damage AS 'Damage',
                    ATKSpeed AS 'Attack Speed',
                    Range AS 'Range'
                FROM 
                    Weapon
                WHERE 
                    WeaponID = ?
            """, (weapon_id,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with weapon data
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "specific_guild":
            # Retrieve guild name from the form
            guild_name = request.form.get('guildName')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch specific guild details
            cursor.execute("""
                SELECT 
                    GuildName AS 'Guild Name',
                    GuildBonus AS 'Guild Bonus',
                    TotalPlayers AS 'Total Players'
                FROM 
                    Guild
                WHERE 
                    GuildName = ?
            """, (guild_name,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with guild data
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "specific_clan":
            # Retrieve clan name from the form
            clan_name = request.form.get('clanName')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch specific clan details
            cursor.execute("""
                SELECT 
                    ClanName AS 'Clan Name',
                    ClanBonus AS 'Clan Bonus',
                    BossName AS 'Boss Name'
                FROM 
                    Clan
                WHERE 
                    ClanName = ?
            """, (clan_name,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with clan data
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "player_inventory":
            # Retrieve player entity ID from the form
            entity_id = request.form.get('entityID')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch player's inventory details
            cursor.execute("""
                SELECT 
                    p.Username AS 'Player Name',
                    w.Name AS 'Weapon Name',
                    w.Description AS 'Description',
                    w.Rank AS 'Rarity',
                    w.Type AS 'Type',
                    w.SpecialATR AS 'Special Attribute',
                    w.Damage AS 'Damage',
                    w.ATKSpeed AS 'Attack Speed',
                    w.Range AS 'Range'
                FROM 
                    Inventory i
                INNER JOIN 
                    Weapon w ON i.WeaponID = w.WeaponID
                INNER JOIN 
                    Player p ON i.EntityID = p.EntityID
                WHERE 
                    i.EntityID = ?
                ORDER BY 
                    w.Rank ASC
            """, (entity_id,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with inventory data
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "enemy_can_drop":
            # Retrieve enemy entity ID from the form
            entity_id = request.form.get('entityID')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch weapons the enemy can drop
            cursor.execute("""
                SELECT 
                    e.Name AS 'Enemy Name',
                    w.Name AS 'Weapon Name',
                    w.Description AS 'Description',
                    w.Rank AS 'Rarity',
                    w.Type AS 'Type',
                    w.SpecialATR AS 'Special Attribute',
                    w.Damage AS 'Damage',
                    w.ATKSpeed AS 'Attack Speed',
                    w.Range AS 'Range'
                FROM 
                    CanDrop c
                INNER JOIN 
                    Weapon w ON c.WeaponID = w.WeaponID
                INNER JOIN 
                    Enemy e ON c.EntityID = e.EntityID
                WHERE 
                    c.EntityID = ?
                ORDER BY 
                    w.Rank ASC
            """, (entity_id,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with drop data
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "entity_equipped_weapon":
            # Retrieve entity ID from the form
            entity_id = request.form.get('entityID')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch equipped weapon details for the entity
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN p.EntityID IS NOT NULL THEN p.Username
                        WHEN e.EntityID IS NOT NULL THEN e.Name
                        ELSE 'Unknown'
                    END AS 'Entity Name',
                    CASE 
                        WHEN p.EntityID IS NOT NULL THEN 'Player'
                        WHEN e.EntityID IS NOT NULL THEN 'Enemy'
                        ELSE 'Unknown'
                    END AS 'Entity Type',
                    w.Name AS 'Weapon Name',
                    w.Description AS 'Description',
                    w.Rank AS 'Rarity',
                    w.Type AS 'Type',
                    w.SpecialATR AS 'Special Attribute',
                    w.Damage AS 'Damage',
                    w.ATKSpeed AS 'Attack Speed',
                    w.Range AS 'Range'
                FROM 
                    Equipped eq
                INNER JOIN 
                    Weapon w ON eq.WeaponID = w.WeaponID
                LEFT JOIN 
                    Player p ON eq.EntityID = p.EntityID
                LEFT JOIN 
                    Enemy e ON eq.EntityID = e.EntityID
                WHERE 
                    eq.EntityID = ?
            """, (entity_id,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with equipped weapon data
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "weapon_type_avg":
            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch average stats for weapons of type "Common"
            cursor.execute("""
                SELECT 
                    Type AS 'Weapon Type',
                    ROUND(AVG(Damage), 1) AS 'Average Damage',
                    ROUND(AVG(ATKSpeed), 1) AS 'Average Attack Speed',
                    ROUND(AVG(Range), 1) AS 'Average Range',
                    ROUND((AVG(Damage) + AVG(ATKSpeed) + AVG(Range)), 1) AS 'Average Total'
                FROM 
                    Weapon
                WHERE 
                    Rank = 'Common'
                GROUP BY 
                    Type
                ORDER BY 
                    ROUND((AVG(Damage) + AVG(ATKSpeed) + AVG(Range)), 1) ASC
            """)

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with average weapon stats
            return render_template('read.html', column_names=column_names, data=data)

        return render_template('read.html', data=data)

    return render_template('read.html', column_names=column_names, data=data)



if __name__ == '__main__':
    app.run(debug=True)
